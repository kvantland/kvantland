<template>
    <div class="background" style="background-color: #D2E8E9;">
        <EmptyHeader />
        <Nuxt />
        <InfoFooter/>
    </div>
</template>

<script>
import InfoFooter from "../modules/all-pages/InfoFooter.vue"
import EmptyHeader from "../modules/all-pages/Headers/EmptyHeader.vue"

export default {
    components: {
        InfoFooter,
        EmptyHeader,
    }
}
</script>