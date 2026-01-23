<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  authStore.checkAuth()
})

</script>

<template>
  <RouterView v-if="authStore.isAuthCheckComplete" />

  <div v-else class="loading-container">
    <VProgressCircular indeterminate color="primary" size="64" />
  </div>
</template>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>