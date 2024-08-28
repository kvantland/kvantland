<template>
	<svg version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
		preserveAspectRatio="xMidYMid meet" 
		overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
		<g class="dron_zone" :transform="`translate(${dronZoneTranslateX} 0)`">
			<g v-for="dronNum in dronAmount" class="dron" :transform="`translate(${(dronNum - 1) * (dronSide + dronGap)} 0)`" :key="`dron_${dronNum}`">
				<text :x="dronSide / 2" :y="dronSide / 2" class="dron_num" dy="0.35em"> {{ dronNum }} </text>
				<image :href='`/problem_assets/drones/dron_${dronNum}.svg`' x="0" :y="dronSide" :width="dronSide" :height="dronSide"/>
				<image v-if="result[dronNum - 1]" :href="`/problem_assets/${result[dronNum - 1]}.svg`" x="0" :y="2.2 * dronSide" :width="dronSide" :height="dronSide" />
			</g>
		</g>
		<g v-if="mode === 'final'" class="final_text" :transform="`translate(0 ${dronZoneHeight})`">
			<text class="final_text" :x="svgWidth / 2" y="0" dy="2em"> Выделите кетку, на которой </text>
			<text class="final_text" :x="svgWidth / 2" y="0" dy="3em"> произошло крушение корабля </text>
		</g>
		<g class="board" :transform="`translate(0 ${dronZoneHeight + gap + finalTextHeight})`">
			<g class="row" v-for="(row, rowNum) in boardSide" :key="`row_${rowNum}`" :transform="`translate(0 ${rowNum * boardItemSide})`">
				<rect v-for="(column, columnNum) in boardSide" :class="['item', JSON.stringify(choicedSquare) === JSON.stringify([rowNum, columnNum]) ? 'choiced' : null]" 
					:style="`fill: ${board[rowNum][columnNum]}`" :key="`item_${rowNum}_${columnNum}`" 
					:x="columnNum * boardItemSide" y="0" :width="boardItemSide" :height="boardItemSide" @click="selection(rowNum, columnNum)"/>
			</g>
			<circle v-if="leftBottomItem && mode === 'select'" class="start_point" :cx="(leftBottomItem[1] + 0.5) * boardItemSide" 
				:cy="(leftBottomItem[0] + 0.5) * boardItemSide" :r="boardItemSide / 4" />
		</g>
		
	</svg>
</template>

<script>
export default {
	props: ['problemParams', 'xhrData', 'newXhr', 'confirmActionResult'],

	model: {
		prop: 'answer',
		event: 'updateAnswer'
	},

	data() {
		return {
			choicedSquare: undefined,
			leftBottomItem: undefined,
			rightTopItem: undefined,
			mode: this.problemParams.search_num === this.problemParams.dron_amount ? 'final' : 'await',
			gap: 15,
			dronGap: 2,
			boardItemSide: 20,
			colors: ['#FCD770', '#70FC8680', '#32D2E8', '#3265E8', '#D932E8', '#FF0606', '#FF8C06'],
		}
	},

	computed: {
		confirmSelection() {
			return this.confirmActionResult
		},
		result() {
			return this.problemParams.result
		},
		board() {
			return this.problemParams.board
		},
		boardSide() {
			return this.problemParams.board_side
		},
		dronAmount() {
			return this.problemParams.dron_amount
		},
		searchNum() {
			return this.problemParams.search_num
		},
		boardWidth() {
			return this.boardSide * this.boardItemSide
		},
		boardHeight() {
			return this.boardItemSide * this.boardSide
		},
		dronSide() {
            return (this.boardWidth - (this.dronAmount - 1) * this.dronGap) / this.dronAmount
        },
		dronZoneWidth() {
			return (this.dronSide + this.dronGap) * this.dronAmount - this.dronGap
		},
		dronZoneHeight() {
			return this.dronSide * 3.2
		},
		dronZoneTranslateX() {
			return (this.boardWidth - this.dronZoneWidth) / 2
		},
		finalTextHeight() {
			return this.mode === 'final' ? 20 : 0
		},
		svgWidth() {
			return this.boardWidth
		},
		svgHeight() {
			return this.boardHeight + this.dronZoneHeight + this.gap + this.finalTextHeight
		}
	},

	watch: {

		confirmSelection(newConfirm) {
			if (newConfirm) {
				this.$emit('xhrRequest', {left_bottom_item: this.leftBottomItem, right_top_item: this.rightTopItem, color: this.colors[this.searchNum]})
				this.leftBottomItem = undefined
			}
		},

		newXhr(isNew) {
			if (isNew) {
				this.$emit('xhrGet')
				if (this.xhrData.xhr_answer.status === "tries out") {
					this.$emit('showXhrDialog', "Попытки закончились!")
				}
			}
		},

		searchNum(newValue) {
			if (newValue === this.dronAmount) {
				this.mode = 'final'
			}
		},
	},

	methods: {
		selection(row, column) {
			if (this.mode === 'await') {
				this.leftBottomItem = [row, column]
				this.mode = 'select'
			}
			else if (this.mode === 'select') {
				this.rightTopItem = [row, column]
				if (this.leftBottomItem[0] < this.rightTopItem[0]) {
					this.mode = 'await';
					return;
				}
				if (this.leftBottomItem[1] > this.rightTopItem[1]) {
					this.mode = 'await';
					return;
				}
				this.mode = 'await'
				this.$emit('showConfirmDialog', {content: "Вы уверены, что хотите отправить дрон?", acceptText: "Да", refuseText: "Нет"})
			}
			else if (this.mode === 'final') {
				this.choicedSquare = [row, column]
				this.$emit('updateAnswer', [row, column])
			}
		},
	}
}
</script>