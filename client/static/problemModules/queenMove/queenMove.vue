<template>
	<svg version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
		preserveAspectRatio="xMidYMid meet" 
		overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
		<g class="board">
			<g class="row" v-for="(row_index, row) in boardSide" :transform="`translate(0 ${row * (boardItemHeight)})`" :key="`row_${row}`">
				<g class="item" v-for="(column_index, column) in boardSide" :transform="`translate(${column * (boardItemWidth)} 0)`" :key="`item_${row}_${column}`">
					<rect :class="(column + row) % 2 == 0 ? 'item orange' : 'item white'"
						:width="boardItemWidth" :height="boardItemHeight" x="0" y="0" />
					<image v-if="horseConfig[row][column] === 'H'"
						class="horse" 
						href="/problem_assets/chess/horse_b.png" :key="`horse_${row}_${column}`"
						:width="boardItemWidth" :height="boardItemHeight" x="0" y="0" />
					<circle v-if="possiblePositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([row, column])})" class="possible_position"
						:cx="boardItemWidth / 2" :cy="boardItemHeight / 2" :r="boardItemWidth * 0.2" />
				</g>
			</g>
		</g>
		<image class="queen active" href="/problem_assets/chess/queen_w.png" @click="startMove"
			:width="boardItemWidth" :height="boardItemHeight" :x="queenPosition[1] * boardItemWidth" :y="queenPosition[0] * boardItemHeight" />
	</svg>
</template>

<script>
export default {
	props: ["problemParams"],
	model: {
		prop: 'answer',
		event: 'updateAnswer'
	},

	data() {
		return {
			mode: 'await',
			possiblePositions: [],
			boardItemWidth: 20,
			boardItemHeight: 20,
		}
	},

	computed: {
		horseConfig() {
			console.log(this.problemParams.horse_config)
			return this.problemParams.horse_config
		},
		queenPosition() {
			return this.problemParams.queen_position
		},
		boardSide() {
			return this.horseConfig.length
		},
		svgWidth() {
			return this.boardItemWidth * this.boardSide 
		},
		svgHeight() {
			return this.boardItemHeight * this.boardSide
		},
		canceledPositions() {
			let canceledPositions = []
			let moves = [[-2, 1], [-2, -1], [2, -1], [2, 1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
			for (let row = 0; row < this.boardSide; row++) {
				for (let column = 0; column < this.boardSide; column++) {
					if (this.horseConfig[row][column] === 'H') {
						for (let move of moves) {
							canceledPositions.push([row + move[0], column + move[1]])
						}
					}
				}
			}
			return canceledPositions
		},
		stopPositions() {
			let stopPositions = []
			for (let row = 0; row < this.boardSide; row++) {
				for (let column = 0; column < this.boardSide; column++) {
					if (this.horseConfig[row][column] === 'H') {
						stopPositions.push([row, column])
					}
				}
			}
			return stopPositions
		},
	},

	methods: {
		startMove() {
			console.log('move start!')
			if (this.mode == 'await')
				this.mode = 'move';
			else {
				this.mode = 'await';
				this.possiblePositions = []
				return;
			}
			let currentPossiblePositions = []
			let [queenY, queenX] = this.queenPosition

			for (let y = queenY - 1; y >= 0; y--) {
				if (this.stopPositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([y, queenX])}))
					break;
				if (this.canceledPositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([y, queenX])}))
					continue;
				currentPossiblePositions.push([y, queenX])
			}
			for (let x = queenX + 1; x < this.boardSide; x++) {
				if (this.stopPositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([queenY, x])}))
					break;
				if (this.canceledPositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([queenY, x])}))
					continue;
				currentPossiblePositions.push([queenY, x])
			}
			let diagonalStepsAmount = Math.min(queenY, this.boardSide - queenX)
			for (let diagonalStep = 1; diagonalStep < diagonalStepsAmount; diagonalStep++) {
				let newX = queenX + diagonalStep
				let newY = queenY - diagonalStep
				if (this.stopPositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([newY, newX])}))
					break;
				if (this.canceledPositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([newY, newX])}))
					continue;
				currentPossiblePositions.push([newY, newX])
			}
			this.possiblePositions = currentPossiblePositions
		}
	}
}
</script>