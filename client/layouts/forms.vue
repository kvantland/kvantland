<template>
    <div class="background" style="background-color: #D2E8E9;">
        <DefaultHeader />
        <Nuxt />
        <InfoFooter/>
    </div>
</template>

<script>
import InfoFooter from "../modules/all-pages/InfoFooter.vue"
import DefaultHeader from "../modules/all-pages/Headers/DefaultHeader.vue"

export default {
    components: {
        InfoFooter,
        DefaultHeader,
    }
}
</script>