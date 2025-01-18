<template>
<g class="towns">
	<image v-for="twn in townsInfo" :key="`shadow_${twn.townID}`" class="icon-shadow" href="/town-icon/icon-shadow.svg" :x="twn.x - 50" :y="twn.y + 30" width="100px" />
    <NuxtLink 
			v-for="twn in townsInfo" 
			:key="`towns_${twn.townID}`" 
			:class="twn.opened ? 'town' : 'town town_completed'" 
			:transform="`translate(${twn.x} ${twn.y})`" 
			:to="`/class/${classValue}/town/${twn.townID}/`">
        <image 
					:href="`/town-icon/${$config.tournamentType}/icon-${twn.townID}.svg`" 
					:x="`${-iconRadius}px`"	:y="`${-iconRadius}px`" 
					:width="`${2 * iconRadius}px`" clip-path="url(#icon_border)" />
        <circle class="town-icon" :r="`${iconRadius}px`" />
        <g class="town-name">
					<g :transform="`translate(0 ${-iconRadius * 1.7})`">
					<path 
					class="town-name" :num="twn.townID-1" :d="townNamesPaths[twn.townID-1]" 
					:transform="`translate(${transformOrigins[twn.townID-1]})`" 
					style="filter:url(#dropshadow)"/>
					<text class="town-name" style="font-family:Montserrat Alternates" :num="twn.townID-1" dy="0.35em">{{twn.name}}</text>
					</g>
        </g>
    </NuxtLink>
</g>
</template>
<script>
export default {
	props: {
		classValue: {
			type: String,
			default: 'all'
		}
	},
	data() {
			return {
					iconRadius: 40,
					townsInfo:{},
					townNamesPaths: [
						'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 150.3788299560547 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -150.3788299560547 a 5 5 0 0 0 -5 5 z',
						'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 226.30149841308594 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -226.30149841308594 a 5 5 0 0 0 -5 5 z',
						'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 179.31068420410156 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -179.31068420410156 a 5 5 0 0 0 -5 5 z',
						'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 87.82855224609375 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -87.82855224609375 a 5 5 0 0 0 -5 5 z',
						'm 0 5 v 29.24428939819336 a 5 5 0 0 0 5 5 h 260.59169006347656 a 5 5 0 0 0 5 -5 v -29.24428939819336 a 5 5 0 0 0 -5 -5 h -260.59169006347656 a 5 5 0 0 0 -5 5 z'],
					transformOrigins: [ 
									'-80.18941497802734 -19.62214469909668',
									'-118.15074920654297 -19.62214469909668',
									'-94.65534210205078 -19.62214469909668',
									'-48.914276123046875 -19.62214469909668',
									'-135.29584503173828 -19.62214469909668'
									],
			}
    },

    async fetch() {
        const townsInfoData = await this.$axios.$get(`/api/towns_info?classes=${this.classValue}`)
        this.townsInfo = townsInfoData
    },

	mounted() {
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
			console.log('origin: ', -(w / 2 + r), -(h / 2 + r))
			console.log(`m 0 ${r} v ${h} a ${r} ${r} 0 0 0 ${r} ${r} h ${w} a ${r} ${r} 0 0 0 ${r} ${-r} v ${-h} a ${r} ${r} 0 0 0 ${-r} ${-r} h ${-w} a ${r} ${r} 0 0 0 ${-r} ${r} z`)
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
    fill: #B62C5A;
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