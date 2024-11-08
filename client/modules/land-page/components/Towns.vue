<template>
<g class="towns">
	<image v-for="twn in townsInfo" :key="`shadow_${twn.townID}`" class="icon-shadow" href="/town-icon/icon-shadow.svg" :x="twn.x - 50" :y="twn.y + 30" width="100px" />
    <NuxtLink v-for="twn in townsInfo" :class="twn.opened ? 'town' : 'town town_completed'" :transform="`translate(${twn.x} ${twn.y})`" :to="`/town/${twn.townID}/`" :key="`towns_${twn.townID}`">
        <image :href="`/town-icon/icon-${twn.townID}.svg`" x="-40px" y ="-40px" width="80px" clip-path="url(#icon_border)" />
        <circle class="town-icon" r="40px" />
        <g class="town-name">
			<path 
			class="town-name" :num="twn.townID-1" :d="townNamesPaths[twn.townID-1]" 
			:transform="`translate(${transformOrigins[twn.townID-1]})`" 
			style="filter:url(#dropshadow)"/>
            <text class="town-name" style="font-family:Montserrat Alternates" :num="twn.townID-1" y="-60" dy="0.35em">{{twn.name}}</text>
        </g>
    </NuxtLink>
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
            transformOrigins: [ 
                    '-83.48246459960937 -76.86099521636963',
                    '-121.46558837890625 -76.86099521636963',
                    '-97.9694107055664 -76.86099521636963',
                    '-52.217011260986325 -76.86099521636963',
                    '-138.62077789306642 -76.86099521636963'
                    ],
        }
    },

    async fetch() {
        const townsInfoData = await this.$axios.$get('/api/towns_info')
        this.townsInfo = townsInfoData
    },

	/* mounted() {
		for(const test of document.querySelectorAll('text')) {
			const rect = test.getBBox()
			this.printPath(rect.width, rect.height)
		}
		return true
    }, 

	methods: {
		printPath(width=0, height=0) {
			const paddingX = 10
			const paddingY = 5
			const r = 5
			const h = height + paddingY * 2 - 2 * r
			const w = width + paddingX * 2 - 2 * r
			console.log('origin: ', h / 2 + r, w / 2 + r)
			console.log(`m 0 ${r} v ${h} a ${r} ${r} 0 0 0 ${r} ${r} h ${w} a ${r} ${r} 0 0 0 ${r} ${-r} v ${-h} a ${r} ${r} 0 0 0 ${-r} ${-r} h ${-w} a ${r} ${r} 0 0 0 ${-r} ${r} v ${h} z`)
		}
	}, */

	
}
</script>
<style scoped>
.town-icon {
    stroke: currentColor;
    stroke-width: 6px;
    fill: transparent;
}

.town-name {
    fill: #3946B9;
}

text.town-name {
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