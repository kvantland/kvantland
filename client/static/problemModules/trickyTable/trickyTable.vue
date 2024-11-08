<template>
	<table class="tricky-table">
		<tbody class="tricky-table__body">
			<tr 
				v-for="_, rowNum in side" :key="`table-row_num-${rowNum}`"
				class="tricky-table__row">
				<td	
					v-for="__, columnNum in side" :key="`table-item_column-${columnNum}_row-${rowNum}`"
				class="tricky-table__item">
					<input 
						class="tricky-table-item__input" 
						:style="`color: ${inputColors[rowNum][columnNum]};`"
						:input-save-value="inputValues[rowNum][columnNum]"
						:value="inputValues[rowNum][columnNum]"
						@keypress="checkFormat($event)"
						@input="inputNumber(rowNum, columnNum, $event)" />
				</td>
			</tr>
		</tbody>
	</table>
</template>

<script>
export default {
	model: {
		prop: 'answer',
		event: 'updateAnswer'
	},
	data() {
		return {
			side: 3,
			inputValues:
			 [
				['', '', ''],
			 	['', '', ''],
				['', '', '']
			],
			inputColors: []
		}
	},
	created() {
		this.inputColors = JSON.parse(JSON.stringify(this.inputValues))
		for (let row = 0; row < this.inputColors.length; row++) {
			for (let column = 0; column < this.inputColors[row].length; column++) {
				this.$set(this.inputColors[row], column, "#"+((1<<24)*Math.random()|0).toString(16))
			}
		}
	},
	methods: {
		checkFormat(event) {
			if (isNaN(event.key) && !['Backspace', 'Delete'].includes(event.key)) {
				event.preventDefault();
			}
		},
		inputNumber(row, column, event) {
			const newValue = Number(event.target.value)
			if ((newValue < 1 || newValue > 200) && event.target.value !== "") {
				event.target.value = this.inputValues[row][column]
				return;
			}
			this.$set(this.inputValues[row], column, event.target.value)	
			this.$emit('updateAnswer', this.inputValues)
		},
	}
}
</script>