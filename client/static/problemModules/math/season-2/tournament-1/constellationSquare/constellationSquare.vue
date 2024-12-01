<template>
	<svg 
		version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
		preserveAspectRatio="xMidYMid meet" 
		overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
		<line 
			v-for="_, lineNum in mapWidth + 1" :key="`vertical-line_num-${lineNum}`"
			:x1="lineNum * side" y1="0" :x2="lineNum * side" :y2="svgHeight" />
		<line
			v-for="_, lineNum in mapHeight + 1" :key="`horizontal-line_num-${lineNum}`"
			x1="0" :y1="lineNum * side" :x2="svgWidth" :y2="lineNum * side" />
		<polygon 
			v-for="star, starNum in stars" :key="`star_num-${starNum}`"
			:class="[`star_choosed-${star.active}`, 'star']"
			:transform="`translate(${-12 + star.x * side} ${-12 + star.y * side})`"
			points="12,0,14.938926261462367,7.954915028125263,23.412678195541844,8.29179606750063,
			16.755282581475768,13.545084971874736,19.05342302750968,21.708203932499366,12,17,4.946576972490323
			,21.70820393249937,7.244717418524233,13.545084971874738,0.5873218044581563,8.291796067500634,
			9.061073738537633,7.954915028125264" 
			@click="chooseStar(starNum)"/>	
	
	</svg>
</template>


<script>
export default {
	model: {
		prop: 'answer',
		event: 'updateAnswer'
	},
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		}
	},
	data() {
		return {
			side: 40,
			stars: [],
		}
	},
	computed: {
		skyMap() {
			return this.problemParams.skyMap
		},
		mapWidth() {
			return this.skyMap.length
		},
		mapHeight() {
			return this.skyMap[0].length
		},
		svgHeight() {
			return this.mapHeight * this.side
		},
		svgWidth() {
			return this.mapWidth * this.side
		},
	},
	created() {
		const stars = []
			for (let row = 0; row < this.mapHeight; row++) {
				for (let column = 0; column < this.mapWidth; column++) {
					if (this.skyMap[row][column] === 'S') {
						stars.push({x: column, y: row, active: false})
					}
				}
			}
			this.stars = stars
	},
	methods: {
		chooseStar(starNum) {
			this.$set(this.stars[starNum], 'active', Boolean(1 - this.stars[starNum].active))
			this.$emit('updateAnswer', this.stars)
		}
	}
}
</script>