<template>
	<svg 
				v-if="plotConfig.length"
				version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`" 
        preserveAspectRatio="xMidYMid"  overflow="visible" 
        xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
		<g
			v-for="__, rowNum in plotHeight"
			:key="`plot-row_num-${rowNum}`"
			:transform="`translate(0 ${rowNum * itemSide})`">
			<g 
				v-for="_, itemNum in plotWidth"
				:key="`item_row-${rowNum}_num-${itemNum}`"
				:transform="`translate(${itemNum * itemSide} 0)`"
				@click="toggleItem(rowNum, itemNum)">
				<image 
					v-if="plotConfig[rowNum][itemNum].image"
					x="0" y="0" :width="itemSide" :height="itemSide"
					:href="`/problem_assets/${plotConfig[rowNum][itemNum].image}`" />
				<rect 
					x="0" y="0" :width="itemSide" :height="itemSide"
					:style="calculateStyles(rowNum, itemNum)" />
			</g>
		</g>
	</svg>
</template>

<script>
export default {
	props: {
		plotConfig: {
			type: Array,
			default:() => { return []}
		},
		itemSide: {
			type: Number,
			default: 30
		},
		choosedColor: {
			type: String,
			default: "rgba(0, 0, 0, 0.5)"
		},
		notChoosedColor: {
			type: String,
			default: "rgba(0, 0, 0, 0)"
		}
	},
	computed: {
		plotWidth() {
			if (!this.plotConfig) return 0;
			return this.plotConfig[0].length
		},
		plotHeight() {
			if (!this.plotConfig) return 0;
			return this.plotConfig.length
		},
		svgWidth() {
			return this.plotWidth * this.itemSide
		},
		svgHeight() {
			return this.plotHeight * this.itemSide
		},
	},
	created() {
		console.log(this.plotConfig)
	},
	methods: {
		calculateStyles(row, column) {
			let styles = "stroke: black; stroke-width: 2px; transition: 0.3s all;"
			console.log(this.choosedColor)
			if (this.plotConfig[row][column].choosed) {
				styles += `fill: ${this.choosedColor};`
			}
			else {
				styles += `fill: ${this.notChoosedColor};`
			}
			if (this.plotConfig[row][column].active) styles += "cursor: pointer;"
			return styles
		},
		toggleItem(row, column) {
			if (!this.plotConfig[row][column].active) return;

			const configCopy = JSON.parse(JSON.stringify(this.plotConfig))
			const answer = []

			configCopy[row][column].choosed = !configCopy[row][column].choosed
			this.$emit('updateConfig', configCopy)

			for (let rowNum = 0; rowNum < this.plotHeight; rowNum++) {
				for (let columnNum = 0; columnNum < this.plotWidth; columnNum++) {
					if (configCopy[rowNum][columnNum].choosed) {
						answer.push([rowNum, columnNum])
					}
				}
			}

			this.$emit('updateAnswer', answer)
		}
	}
}
</script>