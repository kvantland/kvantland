<template>
    <div>
        <StartHeader />
        <div class="content_wrapper_land">
            <Breadcrumbs :crumbs="landCrumbs" />
            <LandInfo />
        </div>
    </div>
</template>


<script>
import StartHeader from '../modules/all-pages/Headers/StartHeader.vue'
import Breadcrumbs from '../modules/all-pages/Breadcrumbs.vue'
import LandInfo from '../modules/land-page/LandInfo.vue'
    export default {
        head() {
            return {
                title: 'Квантландия'
            };
        },
        middleware: 'auth',
        components: {
            StartHeader,
            Breadcrumbs,
            LandInfo,
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

<style>
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

.town-icon {
    stroke: currentColor;
    stroke-width: 6px;
    fill: transparent;
}

.town-name {
    fill: #B62C5A;
}

text.town-name {
    dominant-baseline: central;
    text-anchor: middle;
    fill: currentColor; 
    font-size: 24px; 
    font-family: Montserrat Alternates; 
    font-weight: 700;
}

a.town {
    color: white;
}

a.town * {
    transition: 0.5s all;
}

a.town.town_completed {
    color: #bdbdbd !important;
}

@media(min-width: 961px) {
    a.town:hover {
        color: #ffc400;
    }
}


a.town:hover g.town-name {
    transform: translateY(1%) scale(1.2);
}

g.town-name {
    position: absolute;
    z-index: 10;
}
</style>
