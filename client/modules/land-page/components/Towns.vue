<template>
<g class="towns">
	<image v-for="twn in townsInfo" :key="`shadow_${twn.townID}`" class="icon-shadow" href="/town-icon/icon-shadow.svg" :x="twn.x - 50" :y="twn.y + 30" width="100px" />
    <NuxtLink v-for="twn in townsInfo" :class="twn.opened ? 'town' : 'town town_completed'" :transform="`translate(${twn.x} ${twn.y})`" :to="`/town/${twn.townID}/`" :key="`towns_${twn.townID}`">
        <image :href="`/town-icon/icon-${twn.townID}.svg`" x="-40px" y ="-40px" width="80px" clip-path="url(#icon_border)" />
        <circle class="town-icon" r="40px" />
        <g class="town-name">
			<path class="town-name" :num="twn.townID-1" :d="townNamesPaths[twn.townID-1]" 
			:transform="`translate(${-transformOrigins[twn.townID-1][1]} ${-70-transformOrigins[twn.townID-1][0]})`" 
			style="filter:url(#dropshadow)"/>
            <text class="town-name" style="font-family:Montserrat Alternates" :num="twn.townID-1" y="-70" dy="0.35em">{{twn.name}}</text>
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
					'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 78.1116943359375 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -78.1116943359375 a 5 5 0 0 0 -5 5 v 29.24428939819336 z',
					'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 170.1874542236328 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -170.1874542236328 a 5 5 0 0 0 -5 5 v 29.24428939819336 z',
					'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 90.57801055908203 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -90.57801055908203 a 5 5 0 0 0 -5 5 v 29.24428939819336 z',
					'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 89.62506866455078 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -89.62506866455078 a 5 5 0 0 0 -5 5 v 29.24428939819336 z',
				],
			transformOrigins: [
				[19.62214469909668, 44.05584716796875],
				[19.62214469909668, 90.0937271118164],
				[19.62214469909668, 50.289005279541016],
				[19.62214469909668, 49.81253433227539],
				]
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
    }, */

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
	},

	
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