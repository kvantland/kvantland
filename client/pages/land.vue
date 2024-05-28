<template>
    <div>
        <StartHeader />
        <div class="content_wrapper_land">
            <Breadcrumbs :crumbs="landCrumbs" />
            <LandMap />
        </div>
    </div>
</template>


<script>
import StartHeader from '../modules/all-pages/Headers/StartHeader.vue'
import Breadcrumbs from '../modules/all-pages/Breadcrumbs.vue'
import LandMap from '../modules/land-page/LandMap.vue'
    export default {
        head() {
            return {
                title: 'Квантландия'
            };
        },
        middleware: 'full-auth',
        components: {
            StartHeader,
            Breadcrumbs,
            LandMap,
        },

        data() {
            return {
                landCrumbs: {},
            }
        },

    async fetch() {
        const landCrumbsData = await this.$axios.$get('/api/land_crumbs')
        this.landCrumbs = landCrumbsData
    },
};
</script>

<style scoped>
.content_wrapper_land {
    width: 100%;
    padding: 0 min(5vw, 80px) 80px min(5vw, 80px);
    margin-top: 130px;
    box-sizing: border-box;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 40px;
    display: inline-flex;
}

</style>
