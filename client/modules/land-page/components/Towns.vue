<template>
<g class="towns">
<a v-for="twn in townsInfo" :class="twn.opened ? 'town' : 'town town_completed'" :transform="`translate(${twn.x} ${twn.y})`" :xlink:href="`/town/${twn.townID}/`">
    <image :href="`town-icon/icon-${twn.townID}.png`" x="-40px" y ="-40px" width="80px" clip-path="url(#icon_border)" />
    <circle class="town-icon" r="33px" />
    <g class="town-name">
        <path class="town-name" :num="twn.townID-1" :d="townNamesPaths[twn.townID-1]" :transform="`translate(${townNamesTransforms[twn.townID-1]})`" style="filter:url(#dropshadow)"/>
        <text class="town-name" style="font-family:Montserrat Alternates" :num="twn.townID-1" y="-60">{{twn.name}}</text>
    </g>
</a>
</g>
</template>
<script>
export default {
    data() {
        return {
            townsInfo:{},
            townNamesPaths: [
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 154.96492919921874 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -154.96492919921874 a 6 6 0 0 0 -6 6 z',
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 230.9311767578125 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -230.9311767578125 a 6 6 0 0 0 -6 6 z',
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 183.9388214111328 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -183.9388214111328 a 6 6 0 0 0 -6 6 z',
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 92.43402252197265 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -92.43402252197265 a 6 6 0 0 0 -6 6 z',
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 265.24155578613284 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -265.24155578613284 a 6 6 0 0 0 -6 6 z'
                    ],
            townNamesTransforms: [ 
                    '-83.48246459960937 -76.86099521636963',
                    '-121.46558837890625 -76.86099521636963',
                    '-97.9694107055664 -76.86099521636963',
                    '-52.217011260986325 -76.86099521636963',
                    '-138.62077789306642 -76.86099521636963'
                    ],
        }
    },

    computed: {
        
    },

    async fetch() {
        const townsInfoData = await this.$axios.$get('/api/towns_info')
        this.townsInfo = townsInfoData
    }
}
</script>
<style scoped>
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