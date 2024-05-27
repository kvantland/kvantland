<template>
<g class="towns">
<a v-for="twn in townsInfo" class="town" :transform="`translate(${twn.x} ${twn.y})`" :xlink:href="`/town/${twn.town}/`">
    <image :href="`town-icon/icon-${twn.town}.png`" x="-40px" y ="-40px" width="80px" clip-path="url(#icon_border)" />
    <circle class="town-icon" r="33px" />
    <g class="town-name">
        <path class="town-name" :num="twn.cnt" :d="paths[twn.cnt]" :transform="`translate(${trans[twn.cnt]})`" style="filter:url(#dropshadow)"/>
        <text class="town-name" style="font-family:Montserrat Alternates" :num="twn.cnt" y="-60">{{twn.name}}</text>
    </g>
</a>
</g>
</template>
<script>
export default {
    data() {
        return {
            townsInfo:{},
            paths: [
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 154.96492919921874 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -154.96492919921874 a 6 6 0 0 0 -6 6 z',
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 230.9311767578125 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -230.9311767578125 a 6 6 0 0 0 -6 6 z',
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 183.9388214111328 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -183.9388214111328 a 6 6 0 0 0 -6 6 z',
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 92.43402252197265 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -92.43402252197265 a 6 6 0 0 0 -6 6 z',
                    'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 265.24155578613284 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -265.24155578613284 a 6 6 0 0 0 -6 6 z'
                    ],
            trans: [ 
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