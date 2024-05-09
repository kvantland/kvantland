<template>
    <div style="background-color: #D2E8E9;">
        <Nuxt />
        <InfoFooter/>
    </div>
</template>

<script>
import InfoFooter from "../modules/all-pages/InfoFooter.vue"

export default {
    components: {
        InfoFooter,
    }
}
</script>