<template>
	<div class="game_plot">
		<p :class="['turn_sign', this.turn]"> {{ this.turn === 'player' ? 'Ваш ход' : 'Ход компьютера' }} </p>
		<svg version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
			preserveAspectRatio="xMidYMid meet" 
			overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
			<g class="board">
				<g class="row" v-for="(row_index, row) in boardSide" :transform="`translate(0 ${row * (boardItemHeight)})`" :key="`row_${row}`">
					<g :class="possiblePositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([row, column])}) ? 'possible item' : 'item'" 
						v-for="(column_index, column) in boardSide" :transform="`translate(${column * (boardItemWidth)} 0)`" :key="`item_${row}_${column}`"
						@click="endPlayerMove(row, column)">
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
			<image :class="[mode == 'move' ? turn : null, 'queen', 'active']" href="/problem_assets/chess/queen_w.png" @click="startPlayerMove"
				:width="boardItemWidth" :height="boardItemHeight" 
				:x="turn === 'computer' ? queenComputerPosition[1] * boardItemWidth : queenPosition[1] * boardItemWidth" 
				:y="turn === 'computer' ? queenComputerPosition[0] * boardItemHeight : queenPosition[0] * boardItemHeight" />
		</svg>
	</div>
</template>

<script>
export default {
	props: ["problemParams", "newXhr", "xhrData"],
	model: {
		prop: 'answer',
		event: 'updateAnswer'
	},

	data() {
		return {
			turn: 'player',
			mode: 'await',
			possiblePositions: [],
			boardItemWidth: 20,
			boardItemHeight: 20,
			queenComputerPosition: undefined,
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

	watch: {
		newXhr(isNew) {
			if (isNew) {
				console.log('newXhr')
				this.$emit('xhrGet')
				console.log(this.turn, this.xhrData)
				if (this.xhrData.xhr_answer.status === 'accepted') {
					if (this.xhrData.xhr_answer.turn === 'computer' && this.mode == 'await') {
						console.log(this.queenComputerPosition)
						this.startComputerMove(this.xhrData.xhr_answer.row, this.xhrData.xhr_answer.column)
					}
					else if (this.xhrData.xhr_answer.turn === 'player') {
						console.log('computer turn!')
						setTimeout(function(){this.$emit('xhrRequest', {turn: 'computer', 'solution': document.querySelector('.game_plot').outerHTML})}.bind(this), 10)
					}
				}
			}
		},
		mode(newValue) {
			console.log(newValue)
			if (newValue === 'await') {
				this.possiblePositions = []
			}
		},
	},

	methods: {
		startPlayerMove() {
			if (this.turn !== 'player') {
				return;
			} 
			console.log('move start!')
			if (this.mode === 'await')
				this.mode = 'move';
			else {
				this.mode = 'await';
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
		},

		endPlayerMove(row, column) {
			if (!this.mode == 'move') {
				return
			}
			if (this.possiblePositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([row, column])})) {
				this.queenComputerPosition = [row, column]
				this.turn = 'computer'
				this.mode = 'await'
				this.$emit('xhrRequest', {row: row, column: column, turn: 'player'})
			}
		},

		startComputerMove(row, column) {
			this.mode = 'move'
			const step = [(row - this.queenComputerPosition[0]) / 30, (column - this.queenComputerPosition[1]) / 30]
			console.log(step)	
			console.log(this.queenComputerPosition, row, column)
			const movement = setInterval(function(){
				console.log(this.queenComputerPosition, row, column)
				if (Math.abs(this.queenComputerPosition[0] - row) >= 0.1 || Math.abs(this.queenComputerPosition[1] - column) >= 0.1) {
					console.log('iteration', [this.queenComputerPosition[0] + step[0], this.queenComputerPosition[1] + step[1]]);
					this.queenComputerPosition = [this.queenComputerPosition[0] + step[0], this.queenComputerPosition[1] + step[1]];
				}
				else {
					console.log('stop computer movement')
					clearInterval(movement);
					this.turn = 'player'
					this.mode = 'await'
					setTimeout(function(){this.$emit('xhrRequest', {'check': true, 'solution': document.querySelector('.game_plot').outerHTML})}.bind(this), 20)
				}
			}.bind(this), 15)
		}
	}
}
</script>