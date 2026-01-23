<script setup>
    import { RouterView } from 'vue-router'
</script>

<template>
    <VApp>
        <VMain class="pa-0 ma-0">
            <VContainer class="pa-0 ma-0" fluid>
                <RouterView />
            </VContainer>
        </VMain>
    </VApp>
</template>
