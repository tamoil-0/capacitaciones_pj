import os
import sys
from typing import List, Tuple, Dict
from datetime import datetime

import cv2
import numpy as np

import customtkinter as ctk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib import colors

# ============================================================
#  CONFIGURACIÓN DE POPPLER PARA EJECUTABLE
# ============================================================
# Detectar si estamos corriendo como ejecutable o como script
if getattr(sys, 'frozen', False):
    # Ejecutable (.exe) - poppler debe estar en la misma carpeta
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Script .py - poppler en carpeta del proyecto
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a poppler
POPPLER_PATH = os.path.join(BASE_DIR, "poppler", "Library", "bin")

# Verificar que poppler existe
if not os.path.exists(POPPLER_PATH):
    print(f"[WARNING] Poppler no encontrado en: {POPPLER_PATH}")
    print(f"[WARNING] Buscando en directorio base: {BASE_DIR}")
    POPPLER_PATH = None
else:
    print(f"[INFO] Poppler encontrado en: {POPPLER_PATH}")

# ============================================================
#  INTEGRACIÓN CON API LARAVEL
# ============================================================
print("[DEBUG] Intentando importar api_client...")
try:
    from api_client import api_client, get_eventos, get_inscritos, validar_dni_inscrito
    API_DISPONIBLE = True
    print("[SUCCESS] ✓ API Client importado correctamente")
    print(f"[INFO] API_DISPONIBLE = {API_DISPONIBLE}")
except ImportError as e:
    print(f"[ERROR] ✗ No se pudo importar api_client: {e}")
    print("[WARNING] El sistema funcionará en modo OFFLINE (sin integración Laravel)")
    API_DISPONIBLE = False
    print(f"[INFO] API_DISPONIBLE = {API_DISPONIBLE}")

# ============================================================
#  CONFIGURACIÓN DE CARPETA DE RESULTADOS Y GABARITO
# ============================================================
# Ruta absoluta para que funcione tanto como script como ejecutable
if getattr(sys, 'frozen', False):
    # Si es ejecutable, usar ruta fija de XAMPP
    OUTPUT_FOLDER = r"C:\xampp82\htdocs\capacitaciones_pj\backend\public\resultados_omr"
else:
    # Si es script, usar ruta relativa desde el archivo
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "backend", "public", "resultados_omr")

# Gabarito global (respuestas correctas)
GABARITO = {}  # {1: 'A', 2: 'B', ...}
PUNTAJES = {}  # {1: 1.0, 2: 1.5, ...}  # Puntaje por pregunta

def cv2_imwrite_unicode(filename, img):
    """
    Guarda imágenes con cv2 soportando rutas Unicode en Windows.
    cv2.imwrite() falla con caracteres especiales como acentos.
    
    Args:
        filename: Ruta completa del archivo (puede contener Unicode)
        img: Imagen numpy array (BGR)
        
    Returns:
        bool: True si se guardó correctamente, False si falló
    """
    try:
        # Codificar la imagen como PNG en memoria
        is_success, buffer = cv2.imencode(".png", img)
        if is_success:
            # Guardar usando Python nativo que sí soporta Unicode
            buffer.tofile(filename)
            return True
        return False
    except Exception as e:
        print(f"[ERROR] cv2_imwrite_unicode falló: {e}")
        return False

def ensure_output_folder():
    """Crea la carpeta de resultados si no existe."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    return OUTPUT_FOLDER

def ensure_event_folder(evento_nombre: str, fecha_hora: str = None):
    """
    Crea estructura de carpetas por evento:
    resultados_omr/{NombreEvento}_{fecha}_{hora}/
        ├── evidencias/  (reportes individuales - solo imagen con círculos)
        └── reporte_completo/  (hojas completas con datos, tabla y footer)
    
    Args:
        evento_nombre: Nombre del evento
        fecha_hora: Fecha y hora opcional, si no se provee usa timestamp actual
    
    Returns:
        tuple: (carpeta_evento, carpeta_evidencias, carpeta_hojas)
    """
    if fecha_hora is None:
        fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Sanitizar nombre del evento
    evento_safe = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' 
                         for c in evento_nombre)
    evento_safe = evento_safe.strip().replace(' ', '_')
    
    carpeta_evento = os.path.join(OUTPUT_FOLDER, f"{evento_safe}_{fecha_hora}")
    carpeta_evidencias = os.path.join(carpeta_evento, "evidencias")
    carpeta_hojas = os.path.join(carpeta_evento, "reporte_completo")
    
    os.makedirs(carpeta_evidencias, exist_ok=True)
    os.makedirs(carpeta_hojas, exist_ok=True)
    
    return carpeta_evento, carpeta_evidencias, carpeta_hojas

def cargar_gabarito(filepath: str) -> bool:
    """
    Carga el archivo de gabarito con respuestas correctas y puntajes.
    Formato del archivo .txt:
        1:a:2
        2:b:1.5
        3:c:2
        ...
    
    Formato: pregunta:respuesta:puntaje
    
    Returns:
        bool: True si se cargó correctamente
    """
    global GABARITO, PUNTAJES
    
    try:
        GABARITO.clear()
        PUNTAJES.clear()
        
        lineas_validas = 0
        lineas_error = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for num_linea, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Nuevo formato: pregunta:respuesta:puntaje
                parts = line.split(':')
                if len(parts) >= 2:
                    try:
                        pregunta = int(parts[0])
                        respuesta = parts[1].strip().upper()
                        puntaje = float(parts[2]) if len(parts) >= 3 else 1.0
                        
                        GABARITO[pregunta] = respuesta
                        PUNTAJES[pregunta] = puntaje
                        lineas_validas += 1
                    except (ValueError, IndexError) as e:
                        lineas_error += 1
                        print(f"[WARNING] Línea {num_linea} con error: {line} - {e}")
                else:
                    lineas_error += 1
                    print(f"[WARNING] Línea {num_linea} formato incorrecto: {line}")
        
        if lineas_validas > 0:
            print(f"[respuestas] ✓ Cargadas {lineas_validas} respuestas correctas")
            if lineas_error > 0:
                print(f"[respuestas] ⚠ {lineas_error} líneas con errores fueron ignoradas")
            return True
        else:
            print(f"[ERROR] No se pudo cargar ninguna respuesta válida")
            return False
    
    except Exception as e:
        print(f"[ERROR] No se pudo cargar respuestas: {e}")
        return False

# ============================================================
#  OMR - PASO 1: RECORTE DE LA HOJA (6 CUADRADOS NEGROS)
# ============================================================

def load_all_pages_as_images(path: str) -> List[np.ndarray]:
    """
    Si es PDF: convierte TODAS las páginas a imágenes (BGR).
    Si es JPG/PNG: carga la imagen única.
    Devuelve una lista de imágenes BGR (compatible con OpenCV).
    """
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        # Usar poppler_path si está disponible
        if POPPLER_PATH:
            pages = convert_from_path(path, dpi=300, poppler_path=POPPLER_PATH)
        else:
            pages = convert_from_path(path, dpi=300)
        
        if len(pages) == 0:
            raise RuntimeError("No se pudo leer ninguna página del PDF.")
        images = []
        for pil_img in pages:
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            images.append(img)
        return images
    else:
        img = cv2.imread(path)
        if img is None:
            raise RuntimeError(f"No se pudo leer la imagen: {path}")
        return [img]


def detectar_cuadrados_negros(img: np.ndarray, debug: bool = False
                              ) -> List[Tuple[int, int, int, int]]:
    """
    Detecta los 6 cuadrados negros de referencia en la hoja.
    Disposición: 2 columnas x 3 filas de cuadrados negros sólidos.
    - 2 arriba (izq y der)
    - 2 en el medio (alineados verticalmente)
    - 2 abajo (alineados verticalmente)
    
    EXCLUYE el QR code y otros elementos.
    Devuelve una lista de bounding boxes (x, y, w, h).
    """
    H, W = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    img_area = H * W
    candidates = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area <= 0:
            continue

        # Los cuadrados de referencia son relativamente grandes
        # Ajustar rango: entre 0.0003 y 0.005 del área total
        if area < img_area * 0.0003 or area > img_area * 0.005:
            continue

        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

        # Debe tener 4 vértices (cuadrado)
        if len(approx) != 4:
            continue

        x, y, w, h = cv2.boundingRect(approx)

        # Verificar aspect ratio (debe ser cuadrado, tolerancia 0.7-1.3)
        aspect_ratio = float(w) / float(h)
        if not (0.7 <= aspect_ratio <= 1.3):
            continue

        # Verificar que esté COMPLETAMENTE lleno (cuadrado sólido negro)
        # Extraer la región del thresh y calcular el porcentaje de negro
        roi = thresh[y:y+h, x:x+w]
        if roi.size == 0:
            continue
        filled_ratio = cv2.countNonZero(roi) / float(w * h)

        # Los cuadrados de referencia deben estar muy llenos (>80%)
        if filled_ratio < 0.80:
            continue

        # EXCLUIR zona del QR (esquina inferior derecha, aprox x>60% y y>75%)
        center_x = x + w / 2
        center_y = y + h / 2
        if center_x > W * 0.60 and center_y > H * 0.75:
            # Verificar si es muy grande para ser QR (QR es más grande)
            if area > img_area * 0.002:
                continue

        candidates.append((x, y, w, h, area, filled_ratio))

    if debug:
        print(f"[DEBUG] Candidatos encontrados: {len(candidates)}")
        for c in candidates:
            print(f"  -> x={c[0]}, y={c[1]}, w={c[2]}, h={c[3]}, area={c[4]:.0f}, fill={c[5]:.2f}")

    # Si tenemos muchos candidatos, filtrar por tamaño similar
    # Los 6 cuadrados de referencia deberían tener tamaño similar
    if len(candidates) > 6:
        # Ordenar por área
        candidates.sort(key=lambda c: c[4], reverse=True)
        
        # Buscar grupo de 6 con tamaños similares
        # Tomar los más grandes primero
        areas = [c[4] for c in candidates]
        
        # Calcular la mediana de las 6 áreas más grandes
        top_areas = sorted(areas[:min(10, len(areas))], reverse=True)
        if len(top_areas) >= 6:
            median_area = top_areas[2]  # Tomar el 3ro más grande como referencia
            
            # Filtrar candidatos cuya área esté dentro del 50% de la mediana
            filtered = [c for c in candidates 
                       if median_area * 0.5 <= c[4] <= median_area * 1.5]
            
            if len(filtered) >= 6:
                candidates = filtered

    # Tomar los 6 mejores candidatos (por área)
    candidates.sort(key=lambda c: c[4], reverse=True)
    top6 = [(c[0], c[1], c[2], c[3]) for c in candidates[:6]]

    if len(top6) < 6:
        print(f"[WARN] Solo se detectaron {len(top6)} cuadrados de referencia.")
    
    if debug:
        debug_img = img.copy()
        for i, (x, y, w, h) in enumerate(top6):
            cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 0, 255), 3)
            cv2.putText(debug_img, str(i+1), (x+5, y+25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imwrite("debug_cuadrados.png", debug_img)
        print("[DEBUG] Guardado debug_cuadrados.png")

    return top6


def recortar_area_interna(img: np.ndarray,
                          markers: List[Tuple[int, int, int, int]]
                          ) -> np.ndarray:
    """
    A partir de la lista de bounding boxes de los marcadores,
    calcula un rectángulo grande y recorta esa zona del original.
    """
    if not markers:
        raise RuntimeError("No hay marcadores para recortar el área interna.")

    xs = [x for (x, y, w, h) in markers]
    ys = [y for (x, y, w, h) in markers]
    xs2 = [x + w for (x, y, w, h) in markers]
    ys2 = [y + h for (x, y, w, h) in markers]

    min_x = max(min(xs), 0)
    min_y = max(min(ys), 0)
    max_x = min(max(xs2), img.shape[1])
    max_y = min(max(ys2), img.shape[0])

    padding = 10
    min_x += padding
    min_y += padding
    max_x -= padding
    max_y -= padding

    recorte = img[min_y:max_y, min_x:max_x]
    return recorte


def pipeline_recorte(img: np.ndarray) -> np.ndarray:
    """
    Ejecuta el paso de recorte sobre una imagen y devuelve la imagen recortada (BGR).
    """
    markers = detectar_cuadrados_negros(img, debug=True)

    if len(markers) == 0:
        raise RuntimeError("No se detectaron marcadores. Ajusta los umbrales.")

    recorte = recortar_area_interna(img, markers)
    return recorte


# ============================================================
#  OMR - PASO 2: DETECCIÓN DE RESPUESTAS Y DNI EN EL RECORTE
# ============================================================

def omr_sobre_recorte(recorte_bgr: np.ndarray):
    """
    Aplica la lógica OMR sobre la imagen recortada.
    Devuelve:
        - img_procesada (BGR)
        - dict_respuestas: {pregunta:int -> {"marcadas":[índices], "texto":str}}
        - dni_result_list: lista de chars (dígitos, '-', 'X')
        - dni_str: string concatenado
    """

    img = recorte_bgr.copy()
    H, W = img.shape[:2]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255,
                          cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # ========= CONFIG GENERAL =========
    TOP_Y0 = 0.12
    TOP_Y1 = 0.585
    BOT_Y0 = 0.56
    BOT_Y1 = 0.75

    ANS_X0 = 0.13
    ANS_X1 = 0.66

    COLS = 3
    OPTIONS = 4

    CIRCLE_RADIUS = 25
    SHIFT_Y_GLOBAL = -60

    SHIFT_X_COL1 = -15
    SHIFT_X_COL2 = +77
    SHIFT_X_COL3 = +177

    CIRCLE_MARGIN_X = 40
    CIRCLE_GAP_X = 65

    NUM_SHIFT_X = -35
    NUM_SHIFT_Y = -15

    # ---------- CONFIG DNI ----------
    DNI_COLS = 8
    DNI_DIGITS = 10

    DNI_Y0_FRAC = 0.575
    DNI_Y1_FRAC = 0.995
    DNI_X0_FRAC = 0.55
    DNI_X1_FRAC = 0.935

    DNI_SHIFT_Y = -27
    DNI_CIRCLE_RADIUS = 25
    DNI_NUM_SHIFT_X = -12
    DNI_NUM_SHIFT_Y = +12

    # ======== FUNCIONES AUX =========
    def frac_y(a, H_):
        return int(a * H_)

    def frac_x(a, W_):
        return int(a * W_)

    # ======== CÁLCULO ZONAS RESPUESTAS ========
    Y0_TOP = frac_y(TOP_Y0, H)
    Y1_TOP = frac_y(TOP_Y1, H)
    Y0_BOT = frac_y(BOT_Y0, H)
    Y1_BOT = frac_y(BOT_Y1, H)

    X0 = frac_x(ANS_X0, W)
    X1 = frac_x(ANS_X1, W)

    col_width = (X1 - X0) // COLS

    COL1_X1 = X0
    COL2_X1 = X0 + col_width
    COL3_X1 = X0 + 2 * col_width

    row_h_top = (Y1_TOP - Y0_TOP) // 10
    row_h_bot = 85

    # ======== ZONA DNI ========
    Y0_DNI = frac_y(DNI_Y0_FRAC, H)
    Y1_DNI = frac_y(DNI_Y1_FRAC, H)
    X0_DNI = frac_x(DNI_X0_FRAC, W)
    X1_DNI = frac_x(DNI_X1_FRAC, W)

    dni_col_width = (X1_DNI - X0_DNI) // DNI_COLS
    dni_row_h = (Y1_DNI - Y0_DNI) // DNI_DIGITS

    # ======== DETECCIÓN RESPUESTAS ========
    respuestas: Dict[int, Dict] = {}
    letras = ["A", "B", "C", "D"]

    def draw_question_template(q_num, y_center, x_block_start, shift_x_extra):
        nonlocal img, th

        y_center_local = y_center + SHIFT_Y_GLOBAL

        num_x = x_block_start + NUM_SHIFT_X + shift_x_extra
        num_y = y_center_local + NUM_SHIFT_Y
        cv2.putText(
            img,
            str(q_num),
            (num_x, num_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        base_x = x_block_start + CIRCLE_MARGIN_X + shift_x_extra
        UMBRAL_MARCADO = 0.50

        marcadas = []

        # Detectar qué opciones están marcadas
        for k in range(OPTIONS):
            cx = base_x + k * CIRCLE_GAP_X
            cy = y_center_local

            mask = np.zeros_like(th)
            cv2.circle(mask, (cx, cy), CIRCLE_RADIUS, 255, -1)

            zona = cv2.bitwise_and(th, th, mask=mask)

            total_pix = cv2.countNonZero(mask)
            negros = cv2.countNonZero(zona)
            porcentaje = negros / float(total_pix + 1)

            if porcentaje >= UMBRAL_MARCADO:
                marcadas.append(k)

        # Determinar respuesta y estado
        if len(marcadas) == 0:
            texto = None  # Sin marcar
            estado = "sin_marcar"
        elif len(marcadas) == 1:
            texto = letras[marcadas[0]]
            # Verificar si es correcta según gabarito
            if GABARITO and q_num in GABARITO:
                if texto == GABARITO[q_num]:
                    estado = "correcta"
                else:
                    estado = "incorrecta"
            else:
                estado = "marcada"  # Sin gabarito, solo marcada
        else:
            texto = None  # Duplicado = inválido
            estado = "multiple"

        # Dibujar círculos con colores según estado
        for k in range(OPTIONS):
            cx = base_x + k * CIRCLE_GAP_X
            cy = y_center_local

            if k in marcadas:
                # CÍRCULO MARCADO
                if len(marcadas) > 1:
                    # MÚLTIPLE: ROJO
                    color = (0, 0, 255)
                    thickness = 4
                elif estado == "correcta":
                    # CORRECTA: VERDE
                    color = (0, 255, 0)
                    thickness = 4
                elif estado == "incorrecta":
                    # INCORRECTA: ROJO
                    color = (0, 0, 255)
                    thickness = 4
                else:
                    # SIN GABARITO: VERDE (marcado)
                    color = (0, 255, 0)
                    thickness = 3
            else:
                # CÍRCULO NO MARCADO: AZUL
                color = (255, 0, 0)  # Azul en BGR
                thickness = 2

            cv2.circle(img, (cx, cy), CIRCLE_RADIUS, color, thickness)

        # Guardamos info de esta pregunta
        respuestas[q_num] = {
            "marcadas": marcadas,
            "texto": texto,
            "estado": estado
        }

    # ---- DIBUJAR / DETECTAR ARRIBA: 1–8,16–23,24–30 ----
    for i in range(8):
        y1 = Y0_TOP + i * row_h_top
        y2 = Y0_TOP + (i + 1) * row_h_top
        y_center = (y1 + y2) // 2

        q = 1 + i
        draw_question_template(q, y_center, COL1_X1, SHIFT_X_COL1)

        q = 16 + i
        draw_question_template(q, y_center, COL2_X1, SHIFT_X_COL2)

        if i < 7:
            q = 24 + i
            draw_question_template(q, y_center, COL3_X1, SHIFT_X_COL3)

    # ---- DIBUJAR / DETECTAR ABAJO: 9–15 ----
    for i in range(7):
        y1 = Y0_BOT + i * row_h_bot
        y2 = Y0_BOT + (i + 1) * row_h_bot
        y_center = (y1 + y2) // 2

        q = 9 + i
        draw_question_template(q, y_center, COL1_X1, SHIFT_X_COL1)

    # ======== DETECCIÓN DNI ========
    def draw_dni_column(col_index, x_block_start):
        nonlocal img, th
        UMBRAL_MARCADO_DNI = 0.50

        x0 = x_block_start + dni_col_width * col_index
        cx_center = x0 + dni_col_width // 2

        digit_marked = []

        for d in range(DNI_DIGITS):
            y1 = Y0_DNI + d * dni_row_h
            y2 = Y0_DNI + (d + 1) * dni_row_h
            cy_center = (y1 + y2) // 2 + DNI_SHIFT_Y

            num_x = cx_center + DNI_NUM_SHIFT_X
            num_y = cy_center + DNI_NUM_SHIFT_Y
            cv2.putText(
                img,
                str(d),
                (num_x, num_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                1
            )

            mask = np.zeros_like(th)
            cv2.circle(mask, (cx_center, cy_center), DNI_CIRCLE_RADIUS, 255, -1)

            zona = cv2.bitwise_and(th, th, mask=mask)

            total_pix = cv2.countNonZero(mask)
            negros = cv2.countNonZero(zona)
            porcentaje = negros / float(total_pix + 1)

            if porcentaje >= UMBRAL_MARCADO_DNI:
                color = (0, 255, 0)
                digit_marked.append(d)
            else:
                color = (0, 0, 255)

            cv2.circle(img, (cx_center, cy_center),
                       DNI_CIRCLE_RADIUS, color, 2)

        if len(digit_marked) == 1:
            return str(digit_marked[0]), digit_marked
        elif len(digit_marked) == 0:
            return "-", []
        else:
            return "X", digit_marked

    dni_result = []
    dni_raw_details = []

    for col in range(DNI_COLS):
        dig, marked_list = draw_dni_column(col, X0_DNI)
        dni_result.append(dig)
        dni_raw_details.append(marked_list)

    dni_str = "".join(dni_result)

    return img, respuestas, dni_result, dni_str


# ============================================================
#  GENERACIÓN DE PDF DE RESULTADO - DISEÑO PROFESIONAL
# ============================================================

def dibujar_encabezado_profesional(c, page_width, page_height, dni_str, 
                                   nombre_completo=None, evento_nombre=None):
    """
    Dibuja encabezado profesional con logo (paleta azul corporativa).
    """
    margin = 1 * cm

    # ========== FONDO ELEGANTE SUAVE ==========
    # Banda superior azul para que el logo resalte
    c.setFillColor(colors.HexColor("#1565C0"))  # Azul corporativo
    c.rect(0, page_height - 3.5*cm, page_width, 3.5*cm, fill=True, stroke=False)

    # Banda decorativa azul oscuro inferior
    c.setFillColor(colors.HexColor("#0D47A1"))  # Azul oscuro
    c.rect(0, page_height - 3.7*cm, page_width, 0.2*cm, fill=True, stroke=False)
    
    # ========== LOGO INSTITUCIONAL ==========
    # Buscar logo en múltiples ubicaciones
    if getattr(sys, 'frozen', False):
        # Ejecutable: buscar en el mismo directorio del .exe
        logo_path = os.path.join(os.path.dirname(sys.executable), "pj.jpg")
    else:
        # Script: buscar en el directorio del script
        logo_path = os.path.join(os.path.dirname(__file__), "pj.jpg")
    
    logo_size = 2.5 * cm
    logo_x = margin + 0.3*cm
    logo_y = page_height - 3*cm
    
    # Intentar cargar el logo
    if os.path.exists(logo_path):
        try:
            c.drawImage(logo_path, logo_x, logo_y, 
                       width=logo_size, height=logo_size, 
                       preserveAspectRatio=True, mask='auto')
            print(f"[INFO] Logo cargado desde: {logo_path}")
        except Exception as e:
            print(f"[WARN] No se pudo cargar logo: {e}")
    else:
        print(f"[WARN] Logo no encontrado en: {logo_path}")
    
    # ========== TÍTULO PRINCIPAL ==========
    text_start_x = logo_x + logo_size + 0.8*cm
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(text_start_x, page_height - 1.4*cm,
                "SISTEMA DE ASISTENCIA Y")
    c.drawString(text_start_x, page_height - 2.0*cm,
                "CALIFICACIÓN DE EXÁMENES")

    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#BBDEFB"))  # Azul muy claro
    c.drawString(text_start_x, page_height - 2.6*cm,
                "Evaluación y Calificación Automática")
    
    # ========== FECHA DE CALIFICACIÓN (SUPERIOR DERECHA) ==========
    fecha_str = datetime.now().strftime("%d/%m/%Y")
    hora_str = datetime.now().strftime("%H:%M:%S")
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(page_width - margin - 0.3*cm, page_height - 0.8*cm, "Fecha de Calificación")
    
    c.setFont("Helvetica", 10)
    c.drawRightString(page_width - margin - 0.3*cm, page_height - 1.4*cm, fecha_str)
    c.setFont("Helvetica", 8)
    c.drawRightString(page_width - margin - 0.3*cm, page_height - 2*cm, hora_str)
    
    # ========== SECCIÓN: DATOS DEL POSTULANTE ==========
    info_y = page_height - 4.5*cm
    
    # Título de sección
    c.setFillColor(colors.HexColor("#2C3E50"))  # Azul oscuro
    c.rect(margin, info_y, page_width - 2*margin, 0.8*cm, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 0.3*cm, info_y + 0.25*cm, "DATOS DEL POSTULANTE")
    
    # Fondo de datos
    info_y -= 0.8*cm
    c.setFillColor(colors.HexColor("#F8F9FA"))  # Gris muy claro
    c.rect(margin, info_y - 2*cm, page_width - 2*margin, 2*cm, fill=True, stroke=False)
    
    # Bordes decorativos
    c.setStrokeColor(colors.HexColor("#0D47A1"))
    c.setLineWidth(2)
    c.rect(margin, info_y - 2*cm, page_width - 2*margin, 2*cm, fill=False, stroke=True)
    
    # Contenido de datos - Columna Izquierda
    data_x = margin + 0.5*cm
    data_y = info_y - 0.6*cm
    
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(data_x, data_y, "DNI:")
    c.setFont("Helvetica", 10)
    c.drawString(data_x + 2*cm, data_y, dni_str)
    
    if nombre_completo:
        data_y -= 0.6*cm
        c.setFont("Helvetica-Bold", 10)
        c.drawString(data_x, data_y, "Nombres:")
        c.setFont("Helvetica", 10)
        c.drawString(data_x + 2*cm, data_y, nombre_completo[:45])  # Limitar longitud
    
    if evento_nombre:
        data_y -= 0.6*cm
        c.setFont("Helvetica-Bold", 10)
        c.drawString(data_x, data_y, "Evento:")
        c.setFont("Helvetica", 9)
        c.drawString(data_x + 2*cm, data_y, evento_nombre[:50])  # Limitar longitud
    
    return info_y - 2.3*cm  # Retorna posición Y donde termina el encabezado


def dibujar_pie_pagina_profesional(c, page_width, page_height):
    """
    Dibuja footer profesional institucional elegante.
    """
    margin = 1 * cm
    footer_y = 1.8 * cm
    
    # Banda decorativa superior
    c.setStrokeColor(colors.HexColor("#1565C0"))  # Azul
    c.setLineWidth(2)
    c.line(margin, footer_y + 0.4*cm, page_width - margin, footer_y + 0.4*cm)

    # Fondo del footer
    c.setFillColor(colors.HexColor("#F8F9FA"))  # Gris muy claro
    c.rect(0, 0, page_width, footer_y + 0.3*cm, fill=True, stroke=False)

    # Texto principal del footer
    c.setFillColor(colors.HexColor("#2C3E50"))  # Azul oscuro
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(page_width/2, footer_y,
                       "Sistema de Asistencia y Calificación de Exámenes")

    # Línea decorativa
    c.setStrokeColor(colors.HexColor("#0D47A1"))
    c.setLineWidth(0.5)
    line_center = page_width / 2
    c.line(line_center - 4*cm, footer_y - 0.3*cm,
           line_center + 4*cm, footer_y - 0.3*cm)

    # Texto secundario
    c.setFillColor(colors.HexColor("#666666"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(page_width/2, footer_y - 0.7*cm,
                       "Plataforma de evaluación y registro de asistencia")
    
    c.setFont("Helvetica-Oblique", 6)
    c.setFillColor(colors.HexColor("#999999"))
    c.drawCentredString(page_width/2, footer_y - 1.1*cm, 
                       "Documento generado automáticamente - Prohibida su alteración")


def dibujar_tabla_respuestas_elegante(c, respuestas, x_start, y_start, col_width):
    """
    Dibuja tabla de respuestas con diseño elegante, colores y estado aprobado/desaprobado.
    Optimizada para mostrar 30 preguntas en una sola página.
    """
    # Configuración de la tabla más compacta
    row_height = 0.48 * cm  # Reducido para que quepan 30 filas
    col_num_width = 0.7 * cm
    col_marcada_width = 1.0 * cm
    col_correcta_width = 1.0 * cm
    col_puntaje_width = 1.0 * cm
    col_estado_width = col_width - col_num_width - col_marcada_width - col_correcta_width - col_puntaje_width - 0.2*cm
    
    # Calcular estadísticas
    correctas = 0
    incorrectas = 0
    sin_marcar = 0
    multiples = 0
    puntaje_obtenido = 0
    puntaje_maximo = 0
    
    for q in range(1, 31):
        info = respuestas.get(q, {})
        estado = info.get("estado", "sin_marcar")
        # Obtener puntaje del gabarito global
        pts = PUNTAJES.get(q, 2) if PUNTAJES else 2
        puntaje_maximo += pts
        
        if estado == "correcta":
            correctas += 1
            puntaje_obtenido += pts
        elif estado == "incorrecta":
            incorrectas += 1
        elif estado == "multiple":
            multiples += 1
        else:
            sin_marcar += 1
    
    # ========== CUADRO DE ESTADO: APROBADO/DESAPROBADO ==========
    y_pos = y_start
    
    # Calcular porcentaje
    porcentaje = (puntaje_obtenido / puntaje_maximo * 100) if puntaje_maximo > 0 else 0
    # Aprobado si puntaje >= 20 (no porcentaje, sino puntaje absoluto)
    aprobado = puntaje_obtenido >= 20
    
    # Cuadro más compacto de estado
    estado_box_height = 1.8 * cm  # Reducido
    
    if aprobado:
        c.setFillColor(colors.HexColor("#27AE60"))  # Verde elegante
        estado_texto = "APROBADO"
        icono = "✓"
    else:
        c.setFillColor(colors.HexColor("#E74C3C"))  # Rojo elegante
        estado_texto = "DESAPROBADO"
        icono = "✗"
    
    c.roundRect(x_start, y_pos - estado_box_height, col_width, estado_box_height, 
                8, fill=True, stroke=False)
    
    # Borde blanco interior
    c.setStrokeColor(colors.white)
    c.setLineWidth(3)
    c.roundRect(x_start + 0.1*cm, y_pos - estado_box_height + 0.1*cm, 
                col_width - 0.2*cm, estado_box_height - 0.2*cm, 
                6, fill=False, stroke=True)
    
    # Contenido del cuadro de estado más compacto
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)  # Reducido
    c.drawCentredString(x_start + col_width/2, y_pos - 0.65*cm, f"{icono} {estado_texto}")
    
    c.setFont("Helvetica-Bold", 13)  # Reducido
    c.drawCentredString(x_start + col_width/2, y_pos - 1.1*cm, 
                       f"{puntaje_obtenido:.1f} / {puntaje_maximo} pts")
    
    c.setFont("Helvetica", 9)  # Reducido
    c.drawCentredString(x_start + col_width/2, y_pos - 1.45*cm, 
                       f"Porcentaje: {porcentaje:.1f}%")
    
    y_pos -= estado_box_height + 0.3*cm  # Menos espacio
    
    # ========== RESUMEN ESTADÍSTICO MÁS COMPACTO ==========
    stats_y = y_pos
    
    # Fondo de estadísticas más pequeño
    c.setFillColor(colors.HexColor("#ECF0F1"))  # Gris claro
    c.roundRect(x_start, stats_y - 0.9*cm, col_width, 0.9*cm, 4, fill=True, stroke=False)
    
    # Grid de estadísticas más compacto
    stat_width = col_width / 3
    stats_data = [
        ("✓ Correctas", correctas, "#27AE60"),
        ("✗ Incorrectas", incorrectas, "#E74C3C"),
        ("○ Sin marcar", sin_marcar, "#3498DB")
    ]
    
    for i, (label, valor, color) in enumerate(stats_data):
        stat_x = x_start + i * stat_width
        
        c.setFillColor(colors.HexColor(color))
        c.setFont("Helvetica-Bold", 12)  # Reducido
        c.drawCentredString(stat_x + stat_width/2, stats_y - 0.35*cm, str(valor))
        
        c.setFont("Helvetica", 6)  # Reducido
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.drawCentredString(stat_x + stat_width/2, stats_y - 0.65*cm, label)
    
    y_pos -= 1.1*cm  # Menos espacio
    
    # ========== TABLA DE RESPUESTAS DETALLADAS ==========
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.setFont("Helvetica-Bold", 8)  # Reducido
    c.drawString(x_start, y_pos, "DETALLE DE RESPUESTAS:")
    y_pos -= 0.45*cm  # Menos espacio
    
    # Encabezado de tabla con múltiples columnas
    header_y = y_pos
    c.setFillColor(colors.HexColor("#34495E"))  # Azul gris oscuro
    c.rect(x_start, header_y - row_height, col_width, row_height, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6)  # Fuente más pequeña
    
    col_x = x_start
    c.drawCentredString(col_x + col_num_width/2, header_y - row_height + 0.15*cm, "Nº")
    col_x += col_num_width
    
    c.drawCentredString(col_x + col_marcada_width/2, header_y - row_height + 0.15*cm, "Marcó")
    col_x += col_marcada_width
    
    c.drawCentredString(col_x + col_correcta_width/2, header_y - row_height + 0.15*cm, "Correcta")
    col_x += col_correcta_width
    
    c.drawCentredString(col_x + col_puntaje_width/2, header_y - row_height + 0.15*cm, "Pts")
    col_x += col_puntaje_width
    
    c.drawCentredString(col_x + col_estado_width/2, header_y - row_height + 0.15*cm, "Estado")
    
    y_pos -= row_height
    
    # Filas de preguntas con toda la información
    for q in range(1, 31):
        info = respuestas.get(q, {})
        respuesta_marcada = info.get("texto", "-")
        estado = info.get("estado", "sin_marcar")
        
        # Obtener respuesta correcta del gabarito
        respuesta_correcta = "-"
        puntaje_pregunta = 2  # Por defecto
        
        if GABARITO and q in GABARITO:
            # GABARITO[q] es un string directamente (ej: "a")
            respuesta_correcta = str(GABARITO[q]).upper()
            # PUNTAJES es un dict separado con los puntajes
            puntaje_pregunta = PUNTAJES.get(q, 2) if PUNTAJES else 2
        
        # Color de fondo según estado
        if estado == "correcta":
            c.setFillColor(colors.HexColor("#D5F4E6"))  # Verde muy claro
        elif estado == "incorrecta" or estado == "multiple":
            c.setFillColor(colors.HexColor("#FADBD8"))  # Rojo muy claro
        else:
            if q % 2 == 0:
                c.setFillColor(colors.HexColor("#F8F9FA"))  # Gris muy claro
            else:
                c.setFillColor(colors.white)
        
        c.rect(x_start, y_pos - row_height, col_width, row_height, fill=True, stroke=False)
        
        # Bordes de celda
        c.setStrokeColor(colors.HexColor("#DEE2E6"))
        c.setLineWidth(0.3)
        c.rect(x_start, y_pos - row_height, col_width, row_height, fill=False, stroke=True)
        
        col_x = x_start
        
        # Número de pregunta
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(col_x + col_num_width/2, y_pos - row_height + 0.15*cm, str(q))
        col_x += col_num_width
        
        # Respuesta marcada
        c.setFont("Helvetica-Bold", 7)
        if respuesta_marcada == "-" or respuesta_marcada is None:
            c.setFillColor(colors.grey)
            c.drawCentredString(col_x + col_marcada_width/2, y_pos - row_height + 0.15*cm, "-")
        else:
            c.setFillColor(colors.HexColor("#2C3E50"))
            c.drawCentredString(col_x + col_marcada_width/2, y_pos - row_height + 0.15*cm, 
                               str(respuesta_marcada).upper())
        col_x += col_marcada_width
        
        # Respuesta correcta
        c.setFont("Helvetica-Bold", 7)
        if respuesta_correcta == "-":
            c.setFillColor(colors.grey)
        else:
            c.setFillColor(colors.HexColor("#27AE60"))  # Verde
        c.drawCentredString(col_x + col_correcta_width/2, y_pos - row_height + 0.15*cm, 
                           respuesta_correcta)
        col_x += col_correcta_width
        
        # Puntaje obtenido
        c.setFont("Helvetica", 7)
        if estado == "correcta":
            c.setFillColor(colors.HexColor("#27AE60"))  # Verde
            puntaje_texto = f"+{puntaje_pregunta}"
        else:
            c.setFillColor(colors.HexColor("#95A5A6"))  # Gris
            puntaje_texto = "0"
        c.drawCentredString(col_x + col_puntaje_width/2, y_pos - row_height + 0.2*cm, 
                           puntaje_texto)
        col_x += col_puntaje_width
        
        # Estado con icono
        c.setFont("Helvetica-Bold", 7)
        if estado == "correcta":
            c.setFillColor(colors.HexColor("#27AE60"))
            estado_texto = "✓"
        elif estado == "incorrecta":
            c.setFillColor(colors.HexColor("#E74C3C"))
            estado_texto = "✗"
        elif estado == "multiple":
            c.setFillColor(colors.HexColor("#E74C3C"))
            estado_texto = "✗✗"
        else:
            c.setFillColor(colors.HexColor("#3498DB"))
            estado_texto = "○"
        
        c.drawCentredString(col_x + col_estado_width/2, y_pos - row_height + 0.2*cm, estado_texto)
        
        y_pos -= row_height
    
    return y_pos


# ============================================================
#  GENERACIÓN DE PDF INDIVIDUAL
# ============================================================

def generar_pdf_resultado(dni_str: str, recorte_bgr: np.ndarray, 
                          img_procesada_bgr: np.ndarray, 
                          respuestas: Dict, output_folder: str,
                          nombre_completo: str = None,
                          evento_nombre: str = None,
                          generar_hoja_completa: bool = True,
                          imagen_completa: np.ndarray = None) -> Tuple[str, str]:
    """
    Genera PDFs profesionales con diseño elegante (paleta azul corporativa).
    
    Genera 2 PDFs:
    1. EVIDENCIA: Solo imagen recortada con círculos de colores
    2. HOJA COMPLETA: Diseño profesional con encabezado, tabla, footer, etc.
    
    Args:
        dni_str: DNI del evaluado
        recorte_bgr: Imagen recortada
        img_procesada_bgr: Imagen con círculos de colores
        respuestas: Dict con respuestas detectadas
        output_folder: Carpeta de salida
        nombre_completo: Nombre y apellidos del evaluado
        evento_nombre: Nombre del evento
        generar_hoja_completa: Si genera el PDF completo
        imagen_completa: Imagen original sin procesar
    
    Returns:
        tuple: (pdf_evidencia_path, pdf_hoja_completa_path)
    """
    # Sanitizar DNI para nombre de archivo
    dni_filename = dni_str.replace("-", "_").replace("X", "x")
    if not dni_filename or dni_filename == "________":
        dni_filename = f"sin_dni_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # ========== PDF 1: EVIDENCIA - SOLO IMAGEN RECORTADA CON CÍRCULOS ==========
    pdf_evidencia_path = os.path.join(output_folder, f"{dni_filename}_evidencia.pdf")
    
    counter = 1
    base_path = pdf_evidencia_path
    while os.path.exists(pdf_evidencia_path):
        name, ext = os.path.splitext(base_path)
        pdf_evidencia_path = f"{name}_{counter}{ext}"
        counter += 1
    
    c = canvas.Canvas(pdf_evidencia_path, pagesize=A4)
    page_width, page_height = A4
    margin = 1 * cm
    
    # Encabezado simple azul
    c.setFillColor(colors.HexColor("#0D47A1"))
    c.rect(0, page_height - 1.5*cm, page_width, 1.5*cm, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    texto = f"EVIDENCIA - DNI: {dni_str}"
    if nombre_completo:
        texto += f" - {nombre_completo}"
    c.drawCentredString(page_width/2, page_height - 0.9*cm, texto)
    
    # SOLO LA IMAGEN RECORTADA CON CÍRCULOS
    temp_img_path = os.path.join(output_folder, "_temp_evidencia.png")
    
    # Asegurar que la carpeta existe antes de guardar
    os.makedirs(output_folder, exist_ok=True)
    
    # Guardar imagen usando función que soporta Unicode
    resultado = cv2_imwrite_unicode(temp_img_path, img_procesada_bgr)
    
    if not resultado or not os.path.exists(temp_img_path):
        print(f"[ERROR] No se pudo guardar la imagen temporal con Unicode: {temp_img_path}")
        print(f"[DEBUG] Intentando método alternativo con cv2.imwrite()...")
        # Fallback: intentar con cv2.imwrite directo (por si acaso)
        try:
            resultado = cv2.imwrite(temp_img_path, img_procesada_bgr)
            if not resultado or not os.path.exists(temp_img_path):
                raise IOError("cv2.imwrite también falló")
        except Exception as e:
            print(f"[ERROR CRÍTICO] Imposible guardar imagen temporal: {e}")
            raise IOError(f"No se pudo guardar la imagen en: {temp_img_path}")
    
    img_h, img_w = img_procesada_bgr.shape[:2]
    max_width = page_width - 2*margin
    max_height = page_height - 3*cm
    
    scale = min(max_width / img_w, max_height / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    
    img_x = (page_width - draw_w) / 2
    img_y = (page_height - 2*cm - draw_h) / 2
    
    c.drawImage(temp_img_path, img_x, img_y, width=draw_w, height=draw_h)
    
    try:
        os.remove(temp_img_path)
    except:
        pass
    
    # Footer simple
    c.setFillColor(colors.grey)
    c.setFont("Helvetica", 7)
    c.drawCentredString(page_width/2, 1*cm,
                       "Imagen recortada con corrección - Sistema de Asistencia y Calificación de Exámenes")
    
    c.save()
    
    # ========== PDF 2: HOJA COMPLETA - DISEÑO PROFESIONAL COMPLETO ==========
    pdf_hoja_path = None
    
    if generar_hoja_completa and imagen_completa is not None:
        pdf_hoja_path = os.path.join(output_folder, f"{dni_filename}_hoja_completa.pdf")
        
        counter = 1
        base_path = pdf_hoja_path
        while os.path.exists(pdf_hoja_path):
            name, ext = os.path.splitext(base_path)
            pdf_hoja_path = f"{name}_{counter}{ext}"
            counter += 1
        
        c2 = canvas.Canvas(pdf_hoja_path, pagesize=A4)
        
        # DISEÑO PROFESIONAL COMPLETO
        # Dibujar encabezado profesional
        content_start_y = dibujar_encabezado_profesional(c2, page_width, page_height, 
                                                         dni_str, nombre_completo, evento_nombre)
        
        # Dibujar pie de página profesional
        dibujar_pie_pagina_profesional(c2, page_width, page_height)
        
        # ÁREA DE CONTENIDO
        content_bottom = 2.5 * cm
        content_height = content_start_y - content_bottom
        
        # Dividir en 2 columnas
        col_width = (page_width - 3 * margin) / 2
        left_col_x = margin
        right_col_x = margin + col_width + margin
        
        # COLUMNA IZQUIERDA: IMAGEN COMPLETA ORIGINAL
        temp_completa_path = os.path.join(output_folder, "_temp_completa.png")
        
        # Asegurar que la carpeta existe antes de guardar
        os.makedirs(output_folder, exist_ok=True)
        
        # Guardar imagen usando función que soporta Unicode
        resultado = cv2_imwrite_unicode(temp_completa_path, imagen_completa)
        
        if not resultado or not os.path.exists(temp_completa_path):
            print(f"[ERROR] No se pudo guardar la imagen completa con Unicode: {temp_completa_path}")
            print(f"[DEBUG] Intentando método alternativo con cv2.imwrite()...")
            # Fallback: intentar con cv2.imwrite directo (por si acaso)
            try:
                resultado = cv2.imwrite(temp_completa_path, imagen_completa)
                if not resultado or not os.path.exists(temp_completa_path):
                    raise IOError("cv2.imwrite también falló")
            except Exception as e:
                print(f"[ERROR CRÍTICO] Imposible guardar imagen completa temporal: {e}")
                raise IOError(f"No se pudo guardar la imagen en: {temp_completa_path}")
        
        img_h, img_w = imagen_completa.shape[:2]
        max_img_width = col_width - 0.5*cm
        max_img_height = content_height - 1*cm
        
        scale = min(max_img_width / img_w, max_img_height / img_h)
        draw_width = img_w * scale
        draw_height = img_h * scale
        
        # Marco para la imagen
        img_y = content_start_y - draw_height - 0.5*cm
        c2.setStrokeColor(colors.HexColor("#0D47A1"))
        c2.setLineWidth(2)
        c2.rect(left_col_x, img_y, draw_width, draw_height, fill=False, stroke=True)
        
        c2.drawImage(temp_completa_path, left_col_x, img_y, width=draw_width, height=draw_height)
        
        try:
            os.remove(temp_completa_path)
        except:
            pass
        
        # COLUMNA DERECHA: TABLA DE RESPUESTAS ELEGANTE
        dibujar_tabla_respuestas_elegante(c2, respuestas, right_col_x, content_start_y, col_width)
        
        c2.save()
    
    return pdf_evidencia_path, pdf_hoja_path


# ============================================================
#  PROCESAMIENTO POR LOTES (MÚLTIPLES PÁGINAS)
# ============================================================

def procesar_documento_completo(path: str, progress_callback=None,
                                evento_id=None, inscritos_dict=None,
                                evento_nombre=None) -> List[Dict]:
    """
    Procesa un documento PDF/imagen con múltiples páginas.
    Cada página se considera una hoja de respuestas separada.
    
    INTEGRACIÓN LARAVEL:
    - Si evento_id e inscritos_dict son provistos, valida DNIs
    - Solo procesa hojas con DNI inscrito
    - Envía resultados a la API Laravel
    
    Args:
        path: Ruta del documento a procesar
        progress_callback: Función de callback para progreso
        evento_id: ID del evento (para integración Laravel)
        inscritos_dict: Dict {dni: id_inscripcion} (para validación)
        evento_nombre: Nombre del evento (para carpetas y PDFs)
    
    Retorna una lista de diccionarios con la información de cada hoja
    """
    # ═══════════════════════════════════════════════════
    # CONFIGURAR CARPETAS POR EVENTO
    # ═══════════════════════════════════════════════════
    
    if evento_nombre:
        # Crear carpetas organizadas por evento
        carpeta_evento, carpeta_evidencias, carpeta_hojas = ensure_event_folder(evento_nombre)
        output_folder = carpeta_evento
        print(f"[INFO] Carpeta del evento: {carpeta_evento}")
    else:
        # Modo offline o sin evento: carpeta general
        carpeta_evidencias = ensure_output_folder()
        carpeta_hojas = carpeta_evidencias
        output_folder = carpeta_evidencias
    
    # Verificar si hay integración Laravel activa
    integracion_activa = (API_DISPONIBLE and evento_id is not None 
                         and inscritos_dict is not None)
    
    if integracion_activa:
        print(f"[INFO] ═══ INTEGRACIÓN LARAVEL ACTIVA ═══")
        print(f"[INFO] Evento ID: {evento_id}")
        print(f"[INFO] Total inscritos: {len(inscritos_dict)}")
    else:
        print(f"[INFO] ═══ MODO OFFLINE (sin integración) ═══")
    
    print(f"[INFO] Cargando documento: {path}")
    images = load_all_pages_as_images(path)
    total_pages = len(images)
    print(f"[INFO] Total de páginas encontradas: {total_pages}")
    
    resultados = []
    
    for idx, img in enumerate(images):
        page_num = idx + 1
        print(f"\n[INFO] ═══════════════════════════════════════")
        print(f"[INFO] Procesando página {page_num}/{total_pages}...")
        
        if progress_callback:
            progress_callback(page_num, total_pages)
        
        try:
            # 1) Recortar (OMR - SIN MODIFICAR)
            recorte = pipeline_recorte(img)
            
            # 2) OMR - Detectar respuestas y DNI (SIN MODIFICAR)
            img_proc, respuestas, dni_result, dni_str = omr_sobre_recorte(recorte)
            
            print(f"[OMR] DNI detectado: {dni_str}")
            
            # ═══════════════════════════════════════════════════
            # 3) INTEGRACIÓN LARAVEL: Validar DNI
            # ═══════════════════════════════════════════════════
            
            inscrito = False
            id_inscripcion = None
            nombre_completo = None
            api_guardado = False
            observacion = None
            
            if integracion_activa:
                inscrito_info = validar_dni_inscrito(dni_str, inscritos_dict)
                
                if inscrito_info:
                    inscrito = True
                    id_inscripcion = inscrito_info.get('id_inscripcion')
                    nombre_completo = inscrito_info.get('nombre_completo')
                    print(f"[API] ✓ DNI {dni_str} INSCRITO - {nombre_completo} (id: {id_inscripcion})")
                else:
                    print(f"[API] ✗ DNI {dni_str} NO INSCRITO en este evento")
                    observacion = f"DNI {dni_str} no está inscrito en el evento"
            
            # 4) Generar PDFs profesionales (evidencia + hoja completa)
            pdf_evidencia, pdf_hoja = generar_pdf_resultado(
                dni_str=dni_str,
                recorte_bgr=recorte,
                img_procesada_bgr=img_proc,
                respuestas=respuestas,
                output_folder=carpeta_evidencias,
                nombre_completo=nombre_completo,
                evento_nombre=evento_nombre,
                generar_hoja_completa=True,
                imagen_completa=img  # Imagen original sin recortar
            )
            
            print(f"[PDF] Evidencia: {pdf_evidencia}")
            if pdf_hoja:
                # Mover hoja completa a su carpeta
                import shutil
                pdf_hoja_destino = os.path.join(carpeta_hojas, os.path.basename(pdf_hoja))
                if os.path.exists(pdf_hoja):
                    shutil.move(pdf_hoja, pdf_hoja_destino)
                    print(f"[PDF] Hoja completa: {pdf_hoja_destino}")
            
            # ═══════════════════════════════════════════════════
            # 5) INTEGRACIÓN LARAVEL: Guardar en API (solo si inscrito)
            # ═══════════════════════════════════════════════════
            
            if integracion_activa and inscrito:
                try:
                    # Calcular respuestas correctas según el gabarito
                    correctas = 0
                    total_preguntas = len(GABARITO) if GABARITO else 30
                    puntaje_obtenido = 0.0
                    puntaje_maximo = sum(PUNTAJES.values()) if PUNTAJES else (total_preguntas * 2)
                    
                    for num_pregunta, resp in respuestas.items():
                        respuesta_marcada = resp.get('texto')
                        if respuesta_marcada and num_pregunta in GABARITO:
                            if respuesta_marcada == GABARITO[num_pregunta]:
                                correctas += 1
                                # Sumar el puntaje de esta pregunta
                                puntaje_obtenido += PUNTAJES.get(num_pregunta, 2.0)
                    
                    # Calcular porcentaje basado en puntaje obtenido vs máximo
                    porcentaje = (puntaje_obtenido / puntaje_maximo * 100) if puntaje_maximo > 0 else 0
                    # Aprobado si puntaje >= 20 (no porcentaje, sino puntaje absoluto)
                    aprobado = puntaje_obtenido >= 20
                    
                    # Preparar respuestas para API
                    respuestas_api = []
                    for num_pregunta in range(1, 31):
                        resp = respuestas.get(num_pregunta, {})
                        respuestas_api.append({
                            'numero_pregunta': num_pregunta,
                            'respuesta_marcada': resp.get('texto'),
                            'confianza': None  # El OMR no calcula confianza actualmente
                        })
                    
                    # Guardar evaluación completa en API
                    success, msg = api_client.guardar_evaluacion_completa(
                        id_inscripcion=id_inscripcion,
                        puntaje=puntaje_obtenido,  # Puntaje real obtenido
                        total_preguntas=total_preguntas,
                        aprobado=aprobado,
                        respuestas=respuestas_api,
                        archivo_pdf=pdf_evidencia  # Usar PDF de evidencia para la API
                    )
                    
                    if success:
                        api_guardado = True
                        print(f"[API] ✓ Resultado guardado en Laravel: {msg}")
                    else:
                        print(f"[API] ✗ Error al guardar en Laravel: {msg}")
                
                except Exception as e:
                    print(f"[API] ✗ Excepción al guardar en Laravel: {e}")
            
            # ═══════════════════════════════════════════════════
            # 6) Agregar resultado a la lista
            # ═══════════════════════════════════════════════════
            
            print(f"[OK] Página {page_num} completada")
            
            resultados.append({
                'page': page_num,
                'dni': dni_str,
                'nombre_completo': nombre_completo,
                'respuestas': respuestas,
                'recorte': recorte,
                'procesada': img_proc,
                'pdf_evidencia': pdf_evidencia,
                'pdf_hoja': pdf_hoja if pdf_hoja else None,
                # Campos de integración Laravel
                'inscrito': inscrito,
                'id_inscripcion': id_inscripcion,
                'api_guardado': api_guardado,
                'observacion': observacion,
            })
            
        except Exception as e:
            print(f"[ERROR] Página {page_num}: {e}")
            import traceback
            traceback.print_exc()
            
            resultados.append({
                'page': page_num,
                'dni': 'ERROR',
                'respuestas': {},
                'recorte': None,
                'procesada': None,
                'pdf_path': None,
                'error': str(e),
                # Campos de integración
                'inscrito': False,
                'id_inscripcion': None,
                'api_guardado': False,
                'observacion': f"Error de procesamiento: {str(e)}"
            })
    
    # ═══════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════
    
    print(f"\n[INFO] ═══════════════════════════════════════")
    print(f"[INFO] PROCESAMIENTO COMPLETADO")
    print(f"[INFO] Total páginas: {total_pages}")
    print(f"[INFO] Procesadas exitosamente: {len([r for r in resultados if r['dni'] != 'ERROR'])}")
    
    if integracion_activa:
        inscritos = len([r for r in resultados if r.get('inscrito')])
        no_inscritos = len([r for r in resultados if not r.get('inscrito') and r['dni'] != 'ERROR'])
        guardados = len([r for r in resultados if r.get('api_guardado')])
        
        print(f"[INFO] DNIs inscritos: {inscritos}")
        print(f"[INFO] Guardados en API: {guardados}")
        
        if no_inscritos > 0:
            print(f"[WARNING] DNIs NO INSCRITOS: {no_inscritos}")
            dnis_no_inscritos = [r['dni'] for r in resultados 
                                if not r.get('inscrito') and r['dni'] != 'ERROR']
            print(f"[WARNING] Lista de DNIs no inscritos: {', '.join(dnis_no_inscritos)}")
            print(f"[WARNING] Estos registros NO fueron guardados en la base de datos")
    
    print(f"[INFO] ═══════════════════════════════════════")
    
    return resultados


# ============================================================
#  DIÁLOGO DE PROGRESO MODAL
# ============================================================

class ProgressDialog(ctk.CTkToplevel):
    """Diálogo modal de progreso que bloquea la interfaz."""
    
    def __init__(self, parent, title="Procesando..."):
        super().__init__(parent)
        
        self.title(title)
        self.geometry("500x200")
        self.resizable(False, False)
        
        # Hacer modal (bloquear ventana principal)
        self.transient(parent)
        self.grab_set()
        
        # Centrar en pantalla
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (200 // 2)
        self.geometry(f"500x200+{x}+{y}")
        
        # Configurar UI
        self._build_ui()
        
    def _build_ui(self):
        # Frame contenedor
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono/animación
        self.label_icon = ctk.CTkLabel(
            container,
            text="⏳",
            font=ctk.CTkFont(size=40)
        )
        self.label_icon.pack(pady=(10, 5))
        
        # Etiqueta de estado
        self.label_status = ctk.CTkLabel(
            container,
            text="Inicializando...",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_status.pack(pady=5)
        
        # Etiqueta de detalle
        self.label_detail = ctk.CTkLabel(
            container,
            text="Por favor espera...",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.label_detail.pack(pady=5)
        
        # Barra de progreso
        self.progressbar = ctk.CTkProgressBar(container, width=400)
        self.progressbar.pack(pady=15)
        self.progressbar.set(0)
        
        # Etiqueta de porcentaje
        self.label_percent = ctk.CTkLabel(
            container,
            text="0%",
            font=ctk.CTkFont(size=12)
        )
        self.label_percent.pack()
    
    def update_progress(self, current, total, status=None, detail=None):
        """Actualiza el progreso del diálogo."""
        if total > 0:
            progress = current / total
            percent = int(progress * 100)
        else:
            progress = 0
            percent = 0
        
        self.progressbar.set(progress)
        self.label_percent.configure(text=f"{percent}%")
        
        if status:
            self.label_status.configure(text=status)
        
        if detail:
            self.label_detail.configure(text=detail)
        
        self.update_idletasks()
    
    def close(self):
        """Cierra el diálogo."""
        self.grab_release()
        self.destroy()


# ============================================================
#  GUI PROFESIONAL CON CUSTOMTKINTER
# ============================================================

class OMRApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Asistencia y Calificación de Exámenes")
        self.geometry("1500x900")
        
        # Paleta minimalista profesional
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.input_path = None
        self.resultados = []
        self.current_page_idx = 0
        self.gabarito_path = None
        self.documento_path = None
        
        # ═══════════════════════════════════════════════════
        # INTEGRACIÓN LARAVEL: Estado de evento e inscritos
        # ═══════════════════════════════════════════════════
        self.evento_seleccionado = None  # ID del evento
        self.inscritos_dict = {}  # DNI → id_inscripcion
        self.eventos_list = []  # Lista de eventos disponibles

        # Variables para animaciones
        self.loading_dialog = None

        self._build_ui()

    def _build_ui(self):
        # Paleta de colores minimalista
        self.color_primary = "#2C3E50"      # Azul oscuro elegante
        self.color_secondary = "#3498DB"    # Azul claro
        self.color_accent = "#E74C3C"       # Rojo acento
        self.color_success = "#27AE60"      # Verde éxito
        self.color_bg = "#ECF0F1"           # Gris claro fondo
        self.color_card = "#FFFFFF"         # Blanco tarjetas
        self.color_text = "#2C3E50"         # Texto oscuro
        self.color_text_light = "#7F8C8D"   # Texto claro
        
        self.configure(fg_color=self.color_bg)
        
        # ═══════════════════════════════════════════════════
        # HEADER - TÍTULO PRINCIPAL
        # ═══════════════════════════════════════════════════
        header_frame = ctk.CTkFrame(self, fg_color=self.color_primary, corner_radius=0, height=80)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)
        
        header_title = ctk.CTkLabel(
            header_frame,
            text="Sistema de Asistencia y Calificación de Exámenes",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        header_title.pack(side="top", pady=(15, 0))

        header_subtitle = ctk.CTkLabel(
            header_frame,
            text="Plataforma de evaluación automática",
            font=ctk.CTkFont(size=14),
            text_color="#BDC3C7"
        )
        header_subtitle.pack(side="top", pady=(2, 10))
        
        # ═══════════════════════════════════════════════════
        # CONTAINER PRINCIPAL CON LAYOUT 20/80
        # ═══════════════════════════════════════════════════
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        # Panel izquierdo (20%) - Carga de archivos
        left_container = ctk.CTkFrame(main_container, fg_color="transparent", width=300)
        left_container.pack(side="left", fill="both", padx=(0, 10))
        left_container.pack_propagate(False)
        
        # Panel derecho (80%) - Resultados
        right_container = ctk.CTkFrame(main_container, fg_color="transparent")
        right_container.pack(side="left", fill="both", expand=True)
        
        # ═══════════════════════════════════════════════════
        # SECCIÓN 1: SELECCIÓN DE EVENTO (si API disponible)
        # ═══════════════════════════════════════════════════
        print(f"[DEBUG] Creando interfaz - API_DISPONIBLE = {API_DISPONIBLE}")
        if API_DISPONIBLE:
            print("[DEBUG] Creando sección de eventos en UI...")
            event_card = ctk.CTkFrame(left_container, fg_color=self.color_card, corner_radius=12)
            event_card.pack(side="top", fill="x", pady=(0, 15))
            
            event_header = ctk.CTkLabel(
                event_card,
                text="📅 Selección de Evento",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=self.color_text,
                anchor="w"
            )
            event_header.pack(side="top", anchor="w", padx=20, pady=(15, 10))
            
            event_content = ctk.CTkFrame(event_card, fg_color="transparent")
            event_content.pack(side="top", fill="x", padx=15, pady=(0, 15))
            
            self.combo_eventos = ctk.CTkComboBox(
                event_content,
                values=["Cargando eventos..."],
                command=self.on_evento_seleccionado,
                width=250,
                height=35,
                font=ctk.CTkFont(size=11),
                dropdown_font=ctk.CTkFont(size=10),
                state="readonly",
                button_color=self.color_secondary,
                button_hover_color=self.color_primary
            )
            self.combo_eventos.pack(side="top", fill="x", pady=(0, 8))
            print("[DEBUG] combo_eventos creado exitosamente")
            
            self.btn_recargar_eventos = ctk.CTkButton(
                event_content,
                text="🔄 Actualizar",
                command=self.on_recargar_eventos,
                height=35,
                font=ctk.CTkFont(size=11),
                fg_color=self.color_secondary,
                hover_color=self.color_primary
            )
            self.btn_recargar_eventos.pack(side="top", fill="x", pady=(0, 8))
            
            self.label_inscritos = ctk.CTkLabel(
                event_content,
                text="Inscritos: -",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=self.color_success
            )
            self.label_inscritos.pack(side="top", anchor="w")
            
            # Cargar eventos al iniciar
            print("[DEBUG] Programando carga de eventos en 500ms...")
            self.after(500, self._cargar_eventos_inicial)
        else:
            print("[WARNING] API no disponible - No se creará la sección de eventos")
        
        # ═══════════════════════════════════════════════════
        # SECCIÓN 2: CARGA DE ARCHIVOS
        # ═══════════════════════════════════════════════════
        files_card = ctk.CTkFrame(left_container, fg_color=self.color_card, corner_radius=12)
        files_card.pack(side="top", fill="both", expand=True, pady=(0, 15))
        
        files_header = ctk.CTkLabel(
            files_card,
            text="📂 Archivos",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.color_text,
            anchor="w"
        )
        files_header.pack(side="top", anchor="w", padx=15, pady=(15, 10))
        
        # Contenedor vertical de botones
        files_content = ctk.CTkFrame(files_card, fg_color="transparent")
        files_content.pack(side="top", fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Gabarito
        gabarito_frame = ctk.CTkFrame(files_content, fg_color="transparent")
        gabarito_frame.pack(side="top", fill="x", pady=(0, 15))
        
        self.btn_cargar_gabarito = ctk.CTkButton(
            gabarito_frame,
            text="📄 Cargar respuestas",
            command=self.on_cargar_gabarito,
            height=45,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.color_secondary,
            hover_color=self.color_primary,
            corner_radius=10
        )
        self.btn_cargar_gabarito.pack(side="top", fill="x", pady=(0, 8))
        
        self.label_gabarito = ctk.CTkLabel(
            gabarito_frame,
            text="Ningún archivo seleccionado",
            font=ctk.CTkFont(size=10),
            text_color=self.color_text_light,
            anchor="w",
            wraplength=250
        )
        self.label_gabarito.pack(side="top", anchor="w", padx=5)
        
        # Documento
        documento_frame = ctk.CTkFrame(files_content, fg_color="transparent")
        documento_frame.pack(side="top", fill="x", pady=(0, 15))
        
        self.btn_cargar = ctk.CTkButton(
            documento_frame,
            text="📋 Cargar Examen",
            command=self.on_cargar,
            height=45,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.color_secondary,
            hover_color=self.color_primary,
            corner_radius=10
        )
        self.btn_cargar.pack(side="top", fill="x", pady=(0, 8))
        
        self.label_documento = ctk.CTkLabel(
            documento_frame,
            text="Ningún archivo seleccionado",
            font=ctk.CTkFont(size=10),
            text_color=self.color_text_light,
            anchor="w",
            wraplength=250
        )
        self.label_documento.pack(side="top", anchor="w", padx=5)
        
        # Botón Procesar en el panel izquierdo
        process_frame = ctk.CTkFrame(files_content, fg_color="transparent")
        process_frame.pack(side="top", fill="x")
        
        self.btn_procesar = ctk.CTkButton(
            process_frame,
            text="⚙️ PROCESAR",
            command=self.on_procesar,
            state="disabled",
            height=55,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.color_success,
            hover_color="#229954",
            corner_radius=12
        )
        self.btn_procesar.pack(side="top", fill="x", pady=(0, 10))
        
        # Botón Limpiar
        self.btn_limpiar = ctk.CTkButton(
            process_frame,
            text="🗑️ LIMPIAR",
            command=self.on_limpiar,
            height=45,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            corner_radius=10
        )
        self.btn_limpiar.pack(side="top", fill="x")
        
        # ═══════════════════════════════════════════════════
        # SECCIÓN 3: PROGRESO (Panel derecho)
        # ═══════════════════════════════════════════════════
        progress_card = ctk.CTkFrame(right_container, fg_color=self.color_card, corner_radius=12)
        progress_card.pack(side="top", fill="x", pady=(0, 15))
        
        progress_header = ctk.CTkFrame(progress_card, fg_color="transparent")
        progress_header.pack(side="top", fill="x", padx=20, pady=(15, 0))
        
        self.progress_label = ctk.CTkLabel(
            progress_header,
            text="⏳ Listo para procesar",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.color_text
        )
        self.progress_label.pack(side="left", pady=(0, 8))
        
        self.btn_abrir_carpeta = ctk.CTkButton(
            progress_header,
            text="📁 Ver Resultados",
            command=self.on_abrir_carpeta,
            width=160,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=self.color_text_light,
            hover_color=self.color_text,
            corner_radius=8
        )
        self.btn_abrir_carpeta.pack(side="right")
        
        progress_content = ctk.CTkFrame(progress_card, fg_color="transparent")
        progress_content.pack(side="top", fill="x", padx=20, pady=(0, 15))
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_content,
            height=20,
            corner_radius=10,
            progress_color=self.color_success
        )
        self.progress_bar.pack(side="top", fill="x")
        self.progress_bar.set(0)
        
        # ═══════════════════════════════════════════════════
        # SECCIÓN 4: VISUALIZACIÓN DE RESULTADOS (Panel derecho)
        # ═══════════════════════════════════════════════════
        results_card = ctk.CTkFrame(right_container, fg_color=self.color_card, corner_radius=12)
        results_card.pack(side="top", fill="both", expand=True)
        
        results_header_frame = ctk.CTkFrame(results_card, fg_color="transparent")
        results_header_frame.pack(side="top", fill="x", padx=20, pady=(15, 10))
        
        results_header = ctk.CTkLabel(
            results_header_frame,
            text="📊 Resultados del Procesamiento",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.color_text,
            anchor="w"
        )
        results_header.pack(side="left")
        
        # Navegación
        nav_frame = ctk.CTkFrame(results_header_frame, fg_color="transparent")
        nav_frame.pack(side="right")
        
        self.btn_prev = ctk.CTkButton(
            nav_frame,
            text="◀",
            command=self.on_prev_page,
            state="disabled",
            width=50,
            height=35,
            font=ctk.CTkFont(size=16),
            fg_color=self.color_secondary,
            hover_color=self.color_primary,
            corner_radius=8
        )
        self.btn_prev.pack(side="left", padx=(0, 8))
        
        self.label_pagina = ctk.CTkLabel(
            nav_frame,
            text="- / -",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.color_text,
            width=80
        )
        self.label_pagina.pack(side="left", padx=8)
        
        self.btn_next = ctk.CTkButton(
            nav_frame,
            text="▶",
            command=self.on_next_page,
            state="disabled",
            width=50,
            height=35,
            font=ctk.CTkFont(size=16),
            fg_color=self.color_secondary,
            hover_color=self.color_primary,
            corner_radius=8
        )
        self.btn_next.pack(side="left", padx=(8, 0))
        
        # Contenido de resultados
        results_content = ctk.CTkFrame(results_card, fg_color=self.color_bg, corner_radius=8)
        results_content.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Izquierda: Vista previa
        left_panel = ctk.CTkFrame(results_content, fg_color=self.color_card, corner_radius=8)
        left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        preview_title = ctk.CTkLabel(
            left_panel,
            text="📄 Vista Previa",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.color_text
        )
        preview_title.pack(side="top", pady=10)
        
        self.label_recorte = ctk.CTkLabel(
            left_panel,
            text="Sin imagen cargada",
            font=ctk.CTkFont(size=12),
            text_color=self.color_text_light
        )
        self.label_recorte.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        
        # Derecha: Información y tabla
        right_panel = ctk.CTkFrame(results_content, fg_color=self.color_card, corner_radius=8)
        right_panel.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)
        
        info_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        info_frame.pack(side="top", fill="x", padx=15, pady=10)
        
        self.label_dni = ctk.CTkLabel(
            info_frame,
            text="DNI: -",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.color_primary
        )
        self.label_dni.pack(side="top", anchor="w")
        
        self.label_pdf = ctk.CTkLabel(
            info_frame,
            text="PDF: No generado",
            font=ctk.CTkFont(size=11),
            text_color=self.color_text_light
        )
        self.label_pdf.pack(side="top", anchor="w", pady=(3, 0))
        
        # Tabla de respuestas
        table_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        table_frame.pack(side="top", fill="both", expand=True, padx=15, pady=(5, 15))
        
        table_title = ctk.CTkLabel(
            table_frame,
            text="📝 Respuestas Detectadas",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.color_text
        )
        table_title.pack(side="top", anchor="w", pady=(0, 8))
        
        # Treeview con estilo minimalista
        columns = ("pregunta", "respuesta")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        self.tree.heading("pregunta", text="Pregunta")
        self.tree.heading("respuesta", text="Respuesta")
        self.tree.column("pregunta", width=120, anchor="center")
        self.tree.column("respuesta", width=180, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Estilo para Treeview minimalista
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground=self.color_text,
            fieldbackground="white",
            rowheight=30,
            borderwidth=0
        )
        style.configure("Treeview.Heading",
            background=self.color_primary,
            foreground="white",
            font=("Helvetica", 11, "bold"),
            borderwidth=0
        )
        style.map("Treeview",
            background=[("selected", self.color_secondary)],
            foreground=[("selected", "white")]
        )

    # ============================================================
    #  HANDLERS DE LA GUI
    # ============================================================
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODOS DE INTEGRACIÓN LARAVEL (EVENTOS)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _cargar_eventos_inicial(self):
        """Carga inicial de eventos desde la API"""
        print(f"[DEBUG] _cargar_eventos_inicial() llamado - API_DISPONIBLE = {API_DISPONIBLE}")
        if not API_DISPONIBLE:
            print("[DEBUG] API no disponible, saliendo de _cargar_eventos_inicial()")
            return
        
        print("[DEBUG] Llamando a on_recargar_eventos()...")
        self.on_recargar_eventos()
    
    def on_recargar_eventos(self):
        """Recarga la lista de eventos desde la API"""
        print(f"[DEBUG] on_recargar_eventos() llamado - API_DISPONIBLE = {API_DISPONIBLE}")
        if not API_DISPONIBLE:
            print("[DEBUG] API no disponible, saliendo de on_recargar_eventos()")
            return
        
        try:
            print("[DEBUG] Configurando combo_eventos a 'Cargando...'")
            self.combo_eventos.configure(values=["Cargando..."], state="disabled")
            self.update()
            
            # Obtener eventos desde API
            print("[DEBUG] Llamando a get_eventos()...")
            eventos = get_eventos()
            print(f"[DEBUG] get_eventos() retornó: {type(eventos)}, cantidad: {len(eventos) if eventos else 0}")
            
            if eventos:
                self.eventos_list = eventos
                
                # Crear valores para el ComboBox
                valores = []
                for evento in eventos:
                    id_ev = evento.get('id_evento')
                    nombre = evento.get('nombre', 'Sin nombre')
                    fecha = evento.get('fecha_evento', '')
                    valores.append(f"{id_ev} - {nombre}")
                
                print(f"[DEBUG] Valores del combo: {valores}")
                self.combo_eventos.configure(values=valores, state="readonly")
                self.combo_eventos.set(valores[0] if valores else "Sin eventos")
                
                # Seleccionar automáticamente el primero
                if valores:
                    self.on_evento_seleccionado(valores[0])
                
                print(f"[INFO] {len(eventos)} eventos cargados desde la API")
            else:
                self.combo_eventos.configure(
                    values=["No hay eventos disponibles"], 
                    state="readonly"
                )
                self.combo_eventos.set("No hay eventos disponibles")
                self.label_inscritos.configure(text="Inscritos: 0")
        
        except Exception as e:
            print(f"[ERROR] No se pudieron cargar eventos: {e}")
            self.combo_eventos.configure(
                values=["Error al cargar eventos"], 
                state="readonly"
            )
            messagebox.showerror(
                "⚠️ Error de Conexión con el Servidor",
                "No hay conexión con el servidor.\n\n"
                "Por favor, comuníquese con el área de informática.\n\n"
                f"Detalle técnico: {str(e)}\n\n"
                "El sistema funcionará en modo OFFLINE."
            )
    
    def on_evento_seleccionado(self, choice):
        """Callback cuando se selecciona un evento"""
        if not API_DISPONIBLE or not choice:
            return
        
        try:
            # Extraer ID del evento desde el string "123 - Nombre evento"
            id_evento = int(choice.split(" - ")[0])
            self.evento_seleccionado = id_evento
            
            # Obtener inscritos
            self.label_inscritos.configure(text="Cargando inscritos...")
            self.update()
            
            self.inscritos_dict = get_inscritos(id_evento)
            
            total_inscritos = len(self.inscritos_dict)
            self.label_inscritos.configure(text=f"Inscritos: {total_inscritos}")
            
            print(f"[INFO] Evento seleccionado: {id_evento}")
            print(f"[INFO] Inscritos cargados: {total_inscritos}")
            
        except Exception as e:
            print(f"[ERROR] Error al seleccionar evento: {e}")
            self.label_inscritos.configure(text="Error al cargar inscritos")
            error_msg = str(e)
            if "conexión" in error_msg.lower() or "connection" in error_msg.lower() or "network" in error_msg.lower():
                messagebox.showerror(
                    "⚠️ Error de Conexión con el Servidor",
                    "No hay conexión con el servidor al cargar inscritos.\n\n"
                    "Por favor, comuníquese con el área de informática.\n\n"
                    f"Detalle técnico: {error_msg}"
                )
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODOS ORIGINALES DE LA GUI
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def mostrar_loading(self, mensaje="Cargando..."):
        """Muestra modal de carga centrado con animación."""
        self.loading_dialog = ctk.CTkToplevel(self)
        self.loading_dialog.title("")
        self.loading_dialog.geometry("400x250")
        self.loading_dialog.resizable(False, False)
        
        # Centrar ventana
        self.loading_dialog.transient(self)
        self.loading_dialog.grab_set()
        
        x = (self.winfo_screenwidth() // 2) - 200
        y = (self.winfo_screenheight() // 2) - 125
        self.loading_dialog.geometry(f"400x250+{x}+{y}")
        
        # Eliminar decoraciones de ventana
        self.loading_dialog.overrideredirect(True)
        
        # Fondo elegante
        main_frame = ctk.CTkFrame(
            self.loading_dialog,
            fg_color=self.color_card,
            corner_radius=15,
            border_width=2,
            border_color=self.color_secondary
        )
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Icono animado
        icon_label = ctk.CTkLabel(
            main_frame,
            text="⏳",
            font=ctk.CTkFont(size=60)
        )
        icon_label.pack(pady=(40, 10))
        
        # Mensaje
        msg_label = ctk.CTkLabel(
            main_frame,
            text=mensaje,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.color_primary
        )
        msg_label.pack(pady=10)
        
        # Barra de progreso indeterminada
        progress = ctk.CTkProgressBar(
            main_frame,
            width=300,
            height=8,
            corner_radius=4,
            mode="indeterminate",
            progress_color=self.color_secondary
        )
        progress.pack(pady=20)
        progress.start()
        
        detail_label = ctk.CTkLabel(
            main_frame,
            text="Por favor espere...",
            font=ctk.CTkFont(size=11),
            text_color=self.color_text_light
        )
        detail_label.pack(pady=(0, 20))
        
        self.loading_dialog.update()
        return self.loading_dialog
    
    def cerrar_loading(self):
        """Cierra el modal de carga."""
        if self.loading_dialog:
            self.loading_dialog.grab_release()
            self.loading_dialog.destroy()
            self.loading_dialog = None

    def on_cargar_gabarito(self):
        """Cargar archivo de gabarito con respuestas correctas."""
        path = filedialog.askopenfilename(
            title="Selecciona el archivo de respuestas (.txt)",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        
        # Mostrar animación de carga
        loading = self.mostrar_loading("Cargando respuestas...")
        self.after(100, lambda: self._cargar_gabarito_async(path, loading))
    
    def on_limpiar(self):
        """Limpiar todos los archivos cargados y resultados."""
        respuesta = messagebox.askyesno(
            "🗑️ Confirmar Limpieza",
            "¿Está seguro de que desea limpiar?\n\n"
            "Se eliminarán:\n"
            "• respuestas cargado\n"
            "• Documento de examen\n"
            "• Todos los resultados del procesamiento\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if not respuesta:
            return
        
        try:
            # Limpiar variables globales
            global GABARITO, PUNTAJES
            GABARITO = {}
            PUNTAJES = {}
            
            # Limpiar paths
            self.gabarito_path = None
            self.input_path = None
            self.documento_path = None
            
            # Limpiar resultados
            self.resultados = []
            self.current_page_idx = 0
            
            # Resetear labels de archivos
            self.label_gabarito.configure(
                text="Ningún archivo seleccionado",
                text_color=self.color_text_light
            )
            self.label_documento.configure(
                text="Ningún archivo seleccionado",
                text_color=self.color_text_light
            )
            
            # Deshabilitar botón procesar
            self.btn_procesar.configure(state="disabled")
            
            # Limpiar visualización
            self._clear_display()
            
            # Resetear barra de progreso
            self.progress_bar.set(0)
            self.progress_label.configure(text="⏳ Listo para procesar")
            
            messagebox.showinfo(
                "✓ Limpieza Completada",
                "Se han limpiado todos los archivos y resultados.\n\n"
                "Puede volver a cargar nuevos archivos."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al limpiar: {str(e)}"
            )
    
    def _cargar_gabarito_async(self, path, loading):
        """Proceso asíncrono de carga de gabarito."""
        try:
            if cargar_gabarito(path):
                self.gabarito_path = path
                self.label_gabarito.configure(
                    text=f"✓ {os.path.basename(path)}",
                    text_color=self.color_success
                )
                
                # Calcular puntaje total
                puntaje_total = sum(PUNTAJES.values())
                
                self.cerrar_loading()
                
                messagebox.showinfo(
                    "✓ respuestas Cargado",
                    f"Archivo: {os.path.basename(path)}\n\n"
                    f"✓ Respuestas cargadas: {len(GABARITO)}\n"
                    f"✓ Puntaje total: {puntaje_total:.1f} puntos\n\n"
                    f"🟢 VERDE = Correcta\n"
                    f"🔴 ROJO = Incorrecta\n"
                    f"🔵 AZUL = Sin marcar"
                )
            else:
                self.cerrar_loading()
                messagebox.showerror(
                    "✗ Error",
                    f"No se pudo cargar las respuestas.\n\n"
                    f"Formato esperado:\n"
                    f"pregunta:respuesta:puntaje\n"
                    f"Ejemplo: 1:a:2"
                )
        except Exception as e:
            self.cerrar_loading()
            error_msg = str(e)
            if "conexión" in error_msg.lower() or "connection" in error_msg.lower() or "network" in error_msg.lower():
                messagebox.showerror(
                    "⚠️ Error de Conexión con el Servidor",
                    "No hay conexión con el servidor.\n\n"
                    "Por favor, comuníquese con el área de informática.\n\n"
                    f"Detalle técnico: {error_msg}"
                )
            else:
                messagebox.showerror(
                    "❌ Error al Cargar respuestas",
                    f"No se pudo cargar el archivo de respuestas.\n\n"
                    f"Error: {error_msg}\n\n"
                    "Verifique que el archivo tenga el formato correcto."
                )


    def on_cargar(self):
        """Cargar documento de examen."""
        filetypes = [
            ("PDF files", "*.pdf"),
            ("Image files", "*.jpg;*.jpeg;*.png"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(
            title="Selecciona el documento con hojas de respuestas",
            filetypes=filetypes
        )
        if not path:
            return

        # Mostrar animación de carga
        loading = self.mostrar_loading("Cargando Documento...")
        self.after(100, lambda: self._cargar_documento_async(path, loading))
    
    def _cargar_documento_async(self, path, loading):
        """Proceso asíncrono de carga de documento."""
        try:
            self.input_path = path
            self.documento_path = path
            self.label_documento.configure(
                text=f"✓ {os.path.basename(path)}",
                text_color=self.color_success
            )
            self.btn_procesar.configure(state="normal")
            self.resultados = []
            self.current_page_idx = 0
            self._clear_display()
            
            self.cerrar_loading()
            
        except Exception as e:
            self.cerrar_loading()
            error_msg = str(e)
            if "conexión" in error_msg.lower() or "connection" in error_msg.lower() or "network" in error_msg.lower():
                messagebox.showerror(
                    "⚠️ Error de Conexión con el Servidor",
                    "No hay conexión con el servidor.\n\n"
                    "Por favor, comuníquese con el área de informática.\n\n"
                    f"Detalle técnico: {error_msg}"
                )
            else:
                messagebox.showerror(
                    "❌ Error al Cargar Documento",
                    f"No se pudo cargar el documento.\n\n"
                    f"Error: {error_msg}\n\n"
                    "Verifique que el archivo sea válido."
                )

    def _clear_display(self):
        """Limpia la visualización."""
        self.label_recorte.configure(image=None, text="Sin imagen cargada")
        self.label_dni.configure(text="DNI: -")
        self.label_pdf.configure(text="PDF: No generado")
        self.label_pagina.configure(text="- / -")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.btn_prev.configure(state="disabled")
        self.btn_next.configure(state="disabled")

    def update_progress(self, current, total):
        """Callback para actualizar la barra de progreso."""
        progress = current / total
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"⚙️ Procesando página {current}/{total}...")
        self.update()

    def on_procesar(self):
        if not self.input_path:
            return
        
        # ═══════════════════════════════════════════════════
        # VALIDACIÓN: Si API está activa, requiere evento
        # ═══════════════════════════════════════════════════
        if API_DISPONIBLE and not self.evento_seleccionado:
            messagebox.showwarning(
                "Evento requerido",
                "Debes seleccionar un EVENTO antes de procesar.\n\n"
                "El sistema necesita validar los DNIs contra la lista de inscritos."
            )
            return

        # Mostrar animación de carga modal y bloquear interfaz
        loading = self.mostrar_loading("Procesando Exámenes...")
        
        # Deshabilitar todos los botones
        self.btn_procesar.configure(state="disabled")
        self.btn_cargar.configure(state="disabled")
        self.btn_cargar_gabarito.configure(state="disabled")
        if API_DISPONIBLE:
            self.btn_recargar_eventos.configure(state="disabled")
            self.combo_eventos.configure(state="disabled")
        
        # Procesar después de mostrar el modal
        self.after(200, lambda: self._procesar_async(loading))
    
    def _procesar_async(self, loading):
        """Procesa el documento de forma asíncrona."""
        try:
            # Función de callback para actualizar progreso
            def update_progress_dialog(current, total):
                self.progress_bar.set(current / total)
                self.progress_label.configure(
                    text=f"⚙️ Procesando hoja {current} de {total}..."
                )
                self.update()
            
            # Obtener nombre del evento para las carpetas
            evento_nombre = None
            if API_DISPONIBLE and self.evento_seleccionado:
                for evt in self.eventos_list:
                    if evt.get('id_evento') == self.evento_seleccionado:
                        evento_nombre = evt.get('nombre', f"Evento_{self.evento_seleccionado}")
                        break
            
            self.progress_label.configure(text="⚙️ Analizando documento...")
            self.update()
            
            # PROCESAR
            self.resultados = procesar_documento_completo(
                self.input_path, 
                progress_callback=update_progress_dialog,
                evento_id=self.evento_seleccionado if API_DISPONIBLE else None,
                inscritos_dict=self.inscritos_dict if API_DISPONIBLE else None,
                evento_nombre=evento_nombre
            )

            self.progress_label.configure(text="✓ Completado")
            self.progress_bar.set(1)
            self.update()

            if self.resultados:
                self.current_page_idx = 0
                self._show_current_page()
                self._update_nav_buttons()

            # Cerrar loading
            self.cerrar_loading()

            # Mensaje final
            if API_DISPONIBLE:
                inscritos = len([r for r in self.resultados if r.get('inscrito')])
                guardados = len([r for r in self.resultados if r.get('api_guardado')])
                no_inscritos = len([r for r in self.resultados if not r.get('inscrito') and r['dni'] != 'ERROR'])
                
                mensaje = (
                    f"✅ Procesamiento completado\n\n"
                    f"Total hojas: {len(self.resultados)}\n"
                    f"DNIs inscritos: {inscritos}\n"
                    f"Guardados en API: {guardados}\n"
                    f"DNIs NO inscritos: {no_inscritos}\n\n"
                    f"Los PDFs se guardaron en la carpeta de resultados"
                )
            else:
                mensaje = (
                    f"✅ Procesamiento completado\n\n"
                    f"Total hojas: {len(self.resultados)}\n\n"
                    f"Los PDFs se guardaron en la carpeta de resultados"
                )
            
            messagebox.showinfo("Éxito", mensaje)

        except Exception as e:
            self.cerrar_loading()
            error_msg = str(e)
            print(f"[ERROR] {e}")
            import traceback
            traceback.print_exc()
            
            # Determinar tipo de error
            if "conexión" in error_msg.lower() or "connection" in error_msg.lower() or "network" in error_msg.lower() or "api" in error_msg.lower():
                messagebox.showerror(
                    "⚠️ Error de Conexión con el Servidor",
                    "No hay conexión con el servidor durante el procesamiento.\n\n"
                    "Por favor, comuníquese con el área de informática.\n\n"
                    f"Detalle técnico: {error_msg}\n\n"
                    "Los archivos procesados hasta el momento se han guardado."
                )
            else:
                messagebox.showerror(
                    "❌ Error al Procesar Exámenes",
                    f"Ocurrió un error durante el procesamiento.\n\n"
                    f"Error: {error_msg}\n\n"
                    "Si el problema persiste, comuníquese con el área de informática."
                )

        finally:
            # Rehabilitar botones
            self.btn_procesar.configure(state="normal")
            self.btn_cargar.configure(state="normal")
            self.btn_cargar_gabarito.configure(state="normal")
            if API_DISPONIBLE:
                self.btn_recargar_eventos.configure(state="normal")
                self.combo_eventos.configure(state="normal")

    def _show_current_page(self):
        """Muestra la información de la página actual."""
        if not self.resultados:
            return

        result = self.resultados[self.current_page_idx]
        
        self.label_pagina.configure(
            text=f"Página: {self.current_page_idx + 1}/{len(self.resultados)}"
        )

        # DNI + estado de inscripción
        dni_text = f"DNI: {result['dni']}"
        
        # Agregar nombre si existe
        if result.get('nombre_completo'):
            dni_text += f"\n👤 {result['nombre_completo']}"
        
        if API_DISPONIBLE:
            if result.get('inscrito'):
                dni_text += " ✓ INSCRITO"
            else:
                dni_text += " ✗ NO INSCRITO"
            
            if result.get('api_guardado'):
                dni_text += " | Guardado en API ✓"
        
        self.label_dni.configure(text=dni_text)
        
        # PDF paths + observaciones
        pdf_evidencia = result.get('pdf_evidencia', result.get('pdf_path'))  # Compatibilidad
        pdf_hoja = result.get('pdf_hoja')
        
        if pdf_evidencia:
            pdf_text = f"PDF Evidencia: {os.path.basename(pdf_evidencia)}"
            if pdf_hoja:
                pdf_text += f"\nHoja Completa: {os.path.basename(pdf_hoja)}"
        else:
            pdf_text = "PDF: No generado"
        
        if result.get('observacion'):
            pdf_text += f"\n⚠ {result['observacion']}"
        
        self.label_pdf.configure(text=pdf_text)

        # Imagen procesada con círculos de colores (igual que en PDF evidencia)
        if result.get('procesada') is not None:
            self._show_image_on_label(result['procesada'], self.label_recorte, is_bgr=True)
        elif result['recorte'] is not None:
            self._show_image_on_label(result['recorte'], self.label_recorte, is_bgr=True)
        else:
            self.label_recorte.configure(image=None, text="(Error en recorte)")

        # Tabla de respuestas
        for row in self.tree.get_children():
            self.tree.delete(row)

        for q in range(1, 31):
            info = result['respuestas'].get(q, {"texto": None})
            respuesta = info.get("texto")
            if respuesta is None:
                respuesta_text = "null"
            else:
                respuesta_text = respuesta
            self.tree.insert("", "end", values=(f"P{q}", respuesta_text))

    def _update_nav_buttons(self):
        """Actualiza el estado de los botones de navegación."""
        if len(self.resultados) <= 1:
            self.btn_prev.configure(state="disabled")
            self.btn_next.configure(state="disabled")
        else:
            self.btn_prev.configure(
                state="normal" if self.current_page_idx > 0 else "disabled"
            )
            self.btn_next.configure(
                state="normal" if self.current_page_idx < len(self.resultados) - 1 else "disabled"
            )

    def on_prev_page(self):
        if self.current_page_idx > 0:
            self.current_page_idx -= 1
            self._show_current_page()
            self._update_nav_buttons()

    def on_next_page(self):
        if self.current_page_idx < len(self.resultados) - 1:
            self.current_page_idx += 1
            self._show_current_page()
            self._update_nav_buttons()

    def on_abrir_carpeta(self):
        """Abre la carpeta de resultados en el explorador."""
        folder = ensure_output_folder()
        abs_path = os.path.abspath(folder)
        if sys.platform == 'win32':
            os.startfile(abs_path)
        elif sys.platform == 'darwin':
            os.system(f'open "{abs_path}"')
        else:
            os.system(f'xdg-open "{abs_path}"')

    # ============================================================
    #  UTILIDAD PARA MOSTRAR IMÁGENES EN LA GUI
    # ============================================================

    def _show_image_on_label(self, img, label, is_bgr=True, max_size=(550, 500)):
        """
        Muestra una imagen (numpy) en un CTkLabel, reescalando si es necesario.
        """
        if is_bgr:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = img

        h, w = img_rgb.shape[:2]
        max_w, max_h = max_size

        scale = min(max_w / w, max_h / h, 1.0)
        new_w = int(w * scale)
        new_h = int(h * scale)

        img_resized = cv2.resize(img_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)

        pil_img = Image.fromarray(img_resized)
        tk_img = ImageTk.PhotoImage(pil_img)

        label.configure(image=tk_img, text="")
        label.image = tk_img

# ============================================================
#  MAIN
# ============================================================
if __name__ == "__main__":
    app = OMRApp()
    app.mainloop()
