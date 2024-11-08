<template>
	<div class="game-plot">
		<div class="game-plot__table table">
			<div 
				v-for="row, rowNum in plot"
				:key="`plot-row_num-${rowNum}`"
				class="table__row">
				<div 
					v-for="_, itemNum in row"
					:key="`plot-item_num-${itemNum}_row-${rowNum}`"
					:class="['table__item', ...getBorderClasses(rowNum, itemNum)]">
					<p v-if="startNumbers[rowNum][itemNum] !== 0"> {{ startNumbers[rowNum][itemNum] }} </p>
					<input v-else 
						:input-save-value="inputValues[rowNum][itemNum]"
						:value="inputValues[rowNum][itemNum]" @keydown="inputNUmber(rowNum, itemNum, $event)" />
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	model: {
		prop: 'answer',
		event: 'updateAnswer',
	},
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		}
	},
	data() {
		return {
			inputValues: []
			}
	},
	computed: {
		plot() {
			return this.problemParams.plot
		},
		plotWidth() {
			return this.plot[0].length
		},
		plotHeigth() {
			return this.plot.length
		},
		startNumbers() {
			return this.problemParams.start_numbers
		},
	},
	created() {
		// changing zeros from params to ''
		this.inputValues = JSON.parse(JSON.stringify(this.startNumbers))
		for (let row = 0; row < this.inputValues.length; row++) {
			for (let column = 0; column < this.inputValues[0].length; column++) {
				if (this.inputValues[row][column] === 0) {
					this.$set(this.inputValues[row], column, '')
				}
			}
		}
		this.$emit('updateAnswer', this.inputValues)
	},
	methods: {
		getBorderClasses(row, column) {
			const currentColor = this.plot[row][column]
			const leftColor = column > 0 ? this.plot[row][column - 1] : null
			const rightColor = column + 1 < this.plotWidth ? this.plot[row][column + 1] : null
			const topColor = row > 0 ? this.plot[row - 1][column] : null
			const bottomColor = row + 1 < this.plotHeigth ? this.plot[row + 1][column] : null

			const classes = []
			if (currentColor !== leftColor || column === 0) classes.push('left-border')
			if (currentColor !== rightColor || column === this.plotWidth - 1) classes.push('right-border')
			if (currentColor !== topColor || row === 0) classes.push('top-border')
			if (currentColor !== bottomColor || row === this.plotHeigth - 1) classes.push('bottom-border')

			return classes
		},

		inputNUmber(row, column, event) {
			if (event.key === 'Backspace' || event.key === 'Delete') {
				this.$set(this.inputValues[row], column, '')
				return;
			}
			event.preventDefault()
			if (!['1', '2', '3', '4', '5', '6'].includes(event.key)) return;
			this.$set(this.inputValues[row], column, event.key)	
			this.$emit('updateAnswer', this.inputValues)
		}
	},
}
</script>