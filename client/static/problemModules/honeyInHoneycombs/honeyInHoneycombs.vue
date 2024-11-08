<template>
	<svg version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
		preserveAspectRatio="xMidYMid meet" 
		overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
		<g
			v-for="row, rowNum in honeycombs" :key="`honeycomb-row_row-${rowNum}`"
			class="honeycomb-row"
			:transform="`translate(${rowsTranslateX[rowNum]} ${rowNum * rowGap})`">
			<g 
				v-for="honeycomb, itemNum in row" :key="`honeycomb-row__item_num-${itemNum}_row-${rowNum}`"
				:transform="`translate(${itemNum * hexagonalWidth} 0)`"
				@click="choose(rowNum, itemNum)">
				<path 
				:class="['honeycomb-row__item', `honeycomb-row__item_active-${honeycombs[rowNum][itemNum] === ''}`,
				`honeycomb-row__item_choosed-${choosedCombs[rowNum][itemNum]}`]" 
				:d="`M ${hexagonalWidth / 2} 0
						l ${hexagonalWidth / 2} ${(hexagonalHeight - hexagonalSide) / 2}
						v ${hexagonalSide}
						l ${-hexagonalWidth / 2} ${(hexagonalHeight - hexagonalSide) / 2}
						l ${-hexagonalWidth / 2} ${-(hexagonalHeight - hexagonalSide) / 2}
						v ${-hexagonalSide}
						l ${hexagonalWidth / 2} ${-(hexagonalHeight - hexagonalSide) / 2} z`"/>
				<text v-if="honeycombs[rowNum][itemNum] !== ''" 
					:x="hexagonalWidth / 2" :y="hexagonalHeight / 2" dy="0.35em"
					 class='honeycomb-row__item-text'> 
					{{ honeycombs[rowNum][itemNum] }} </text>
			</g>
		</g>
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
			choosedCombs: [],
			hexagonalSide: 20
		}
	},
	computed: {
		honeycombs() {
			return this.problemParams.honeycombsConfig
		},
		hexagonalWidth() {
			return Math.cos(Math.PI / 6) * 2 * this.hexagonalSide
		},
		hexagonalHeight() {
			return this.hexagonalSide + 2 * Math.sin(Math.PI / 6) * this.hexagonalSide
		},
		svgHeight() {
			return this.honeycombs.length * (this.hexagonalSide + (this.hexagonalHeight - this.hexagonalSide) / 2) + 
					(this.hexagonalHeight - this.hexagonalSide) / 2
		},
		svgWidth() {
			return 6 * this.hexagonalWidth // пока лень возиться, чтобы автоматически считать
		},
		rowsTranslateX() {
			return [
				this.hexagonalWidth / 2,
				0,
				this.hexagonalWidth / 2,
				0,
				this.hexagonalWidth / 2,
				this.hexagonalWidth
			]
		},
		rowGap() {
			return this.hexagonalSide + Math.sin(Math.PI / 6) * this.hexagonalSide
		}
	},
	created() {
		this.choosedCombs = JSON.parse(JSON.stringify(this.honeycombs))
		for (let row = 0; row < this.choosedCombs.length; row++) {
			for (let column = 0; column < this.choosedCombs[row].length; column++) {
				this.$set(this.choosedCombs[row], column, false)
			}
		}
	},
	methods: {
		choose(row, column) {
			if (this.honeycombs[row][column] !== '') return;
			const isActive = this.choosedCombs[row][column]
			this.$set(this.choosedCombs[row], column, Boolean(1 - isActive))
			this.$emit('updateAnswer', this.choosedCombs)
		}
	}
}
</script>