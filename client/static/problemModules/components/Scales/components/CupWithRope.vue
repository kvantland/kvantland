<template>
	<g>
		<g :class= "`cup ${name}`" :transform="`translate(0 ${ropeHight})`">
			<ellipse 
				class="inside" 
				style="fill: url(#cupShadowInside);	stroke: #949494; stroke-width: 2;" 
				cx="0"
				cy="0"
				:rx="`${cupInnerRadiusX}`"
				:ry="`${cupInnerRadiusY}`" />
			<g class="objects" :transform="`scale(${objectsToCenterScale}) translate(0 ${objectMarginTop})`">
				<g 
					v-for="(object, objectNum) in objects" :key="`cup-item_num-${objectNum}`" 
					:transform="`scale(${objectScale.x} ${objectScale.y}) 
					translate(${objectsCoordinates[objectNum].x} ${objectsCoordinates[objectNum].y})`"
					class="object" 
					@touchstart="moveFromCup(object, objectNum)"
					@mousedown="moveFromCup(object, objectNum)"
					v-html="object.html"></g>
			</g>
			<path 
				class="outside" 
				style="fill: url(#cupShadowOutside); stroke: #949494; stroke-width: 2;"
				:d="`
					M  ${-cupOuterRadiusX} 0 
					a ${cupOuterRadiusX} ${cupOuterRadiusY} 0 0 0 ${cupWidth} 0
					A ${cupInnerRadiusX} ${cupInnerRadiusY} 0 0 1 ${-cupWidth / 2} 0 `" />
		</g>

		<g class="ropes" style="stroke: #484848; stroke-width: 2;">
			<line 
				x1="0"
				y1="0"
				:x2="`${-cupWidth / 2}`"
				:y2="ropeHight" />
			<line 
				x1="0"
				y1="0"
				x2="0"
				:y2="ropeHight + cupInnerRadiusY" />
			<line 
				x1="0"
				y1="0"
				:x2="`${cupWidth / 2}`"
				:y2="ropeHight" />
		</g>
						
		<circle 
			class="hinge" 
			style="fill: #A7763D; stroke: #815A30; stroke-width: 4;"
			cx="0"
			cy="0"
			:r="`${hingeR}`"/>
	</g>
</template>

<script>
export default {
		props: {
				cupWidth: {},
				cupInnerRadiusX: {},
				cupInnerRadiusY: {},
				cupOuterRadiusX: {},
				cupOuterRadiusY: {},
				ropeHight: {},
				ropeWidth: {},
				hingeR: {},
				name: {default: ''},
				objects: {default: () => {return []}},
				objectMarginTop: {default: 4},
				objectsToCenterScale: {
					type: Number,
					default: 0.7
				},
				objectSide: {
					type: Number,
					default: 0
				},
				objectScale: {
					type: Object,
					default: () => {return {x: 1, y: 1}},
				}
		},
		computed: {
				objectsCoordinates() {
						let coordinates = []
						let angle = 0
						const objectsAmount = this.objects.length
						const angleStep = Math.PI * 2 / objectsAmount
						for (let objectNum = 0; objectNum < objectsAmount; objectNum++) {
								angle += angleStep
								const x = this.cupInnerRadiusX * Math.cos(angle) - this.objectSide / 2
								const y = this.cupInnerRadiusY * Math.sin(angle) - this.objectSide / 2
								coordinates.push({x: x, y: y})
						}
						return coordinates
				}
		},
		methods: {
			moveFromCup(item, itemIndex) {
				console.log(item)
				this.$emit('moveFromCup', {item, itemIndex, cup: this.name.split('_')[0]})
			}
		},
		created() {
				console.log(this.objects, this.name)
		},
}
</script>

<style scoped>

.object {
		cursor: grab;
}

</style>