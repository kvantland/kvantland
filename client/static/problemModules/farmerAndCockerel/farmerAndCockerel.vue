<template>
	<div class="play-board">
		<div 
			v-if="mode === 'chooseTurn'"
			class="play-board__buttons">
			<button class="play-board__button" @click="setTurn('player')"> Ходить первым </button>
			<button class="play-board__button" @click="setTurn('computer')"> Ходить вторым </button>
		</div>
		<div v-else-if="mode === 'await' || mode === 'move'" style="display: flex; flex-direction: column; align-items: center;">
			<p :class="['turn_sign', turn]"> 
				{{ turn === 'player' ? 'Ваш ход' : 'Ход компьютера' }} 
			</p>
			<p> Осталось ходов: {{ remainingMovements }} </p>
		</div>
		<svg 
			version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
			preserveAspectRatio="xMidYMid meet" 
			overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
			<g
				v-for="_, boardRowNum in boardHeight" :key="`board-row_num-${boardRowNum}`"
				:transform="`translate(0 ${boardRowNum * boardItemSide})`">
				<g
					v-for="__, boardColumnNum in boardWidth" :key="`board-item_row-${boardRowNum}_num-${boardColumnNum}`"
					:transform="`translate(${boardColumnNum * boardItemSide} 0)`">
					<rect 
						fill="white"
						stroke="black"
						stroke-width="1px"
						:width="boardItemSide"
						:height="boardItemSide"
						x="0" y="0"
						@click="requestToMoveFarmerToPosition(boardRowNum, boardColumnNum)"/>
				</g>
			</g>
			<image 
				class="cockerel"
				:x="boardItemSide * cockerelPositionCurrent.x" :y="boardItemSide * cockerelPositionCurrent.y"
				:width="boardItemSide" :height="boardItemSide"
				:href="`/problem_assets/farmer_and_cockerel/cockerel.svg`" />
			<image 
				:x="boardItemSide * farmerPositionCurrent.x" :y="boardItemSide * farmerPositionCurrent.y"
				:width="boardItemSide" :height="boardItemSide"
				:href="`/problem_assets/farmer_and_cockerel/farmer.svg`" />
			<g
				v-for="_, boardRowNum in boardHeight" :key="`board-row_position_num-${boardRowNum}`"
				:transform="`translate(0 ${boardRowNum * boardItemSide})`">
				<g
					v-for="__, boardColumnNum in boardWidth" :key="`board-item_position_row-${boardRowNum}_num-${boardColumnNum}`"
					:transform="`translate(${boardColumnNum * boardItemSide} 0)`">
					<circle 
						v-if="isPositionPossible(boardRowNum, boardColumnNum) && mode == 'await'" 
						class="possible_position"
						:cx="boardItemSide / 2" :cy="boardItemSide / 2" :r="boardItemSide * 0.2" />
				</g>
			</g>
		</svg>
	</div>
</template>

<script>
export default {
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		},
		xhrData: {
			type: Object,
			default: () => {}
		},
		newXhr: {
			type: Boolean,
			default: false
		}
	},
	data() {
		return {
			mode: 'chooseTurn', // chooseTurn, await or move
			turn: undefined, // player or computer
			boardItemSide: 50,
			farmerPositionCurrent: {x: undefined, y: undefined},
			cockerelPositionCurrent: {x: undefined, y: undefined},
		}
	},
	computed: {
		remainingMovements() {
			return this.problemParams.remaining_moves
		},
		boardWidth() {
			return this.problemParams.board_width
		},
		boardHeight() {
			return this.problemParams.board_height
		},
		svgHeight() {
			return this.boardHeight * this.boardItemSide
		},
		svgWidth() {
			return this.boardWidth * this.boardItemSide
		},
		farmerPositionReal() {
			return {x: this.problemParams.farmer_coordinates[1], y: this.problemParams.farmer_coordinates[0]}
		},
		farmerPositionStr() {
			return this.farmerPositionReal.x + ' ' + this.farmerPositionReal.y
		},
		cockerelPositionReal() {
			return {x: this.problemParams.cockerel_coordinates[1], y: this.problemParams.cockerel_coordinates[0]}
		},
		cockerelPositionStr() {
			return this.cockerelPositionReal.x + ' ' + this.cockerelPositionReal.y
		},
		possiblePositions() {
			const possiblePositions = []
			const movements = [[-1, 0], [0, -1], [0, 1], [1, 0]]

			if (!(this.turn === 'player')) return possiblePositions;

			for (const movement of movements) {
				const newXposition = this.farmerPositionReal.x + movement[0]
				const newYposition = this.farmerPositionReal.y + movement[1]
				if (newXposition < 0 || newXposition >= this.boardWidth) continue;
				if (newYposition < 0 || newYposition >= this.boardHeight) continue;
				possiblePositions.push([newXposition, newYposition])
			}
			console.log(possiblePositions)
			return possiblePositions
		},
	},
	watch: {
		farmerPositionStr() {
			console.log('updateFarmerCoordinates')
			console.log(this.farmerPositionReal)
			this.updatePosition('player', this.farmerPositionReal)
		},
		cockerelPositionStr() {
			this.updatePosition('computer', this.cockerelPositionReal)
		},
		newXhr(isNew) {
			if (isNew) {
				this.$emit('xhrGet')
				if (this.xhrData.xhr_answer.status === "not allowed") {
					this.$emit('showXhrDialog', "Невозможно сделать ход!")
				}
			}
		}
	},
	created() {
		this.farmerPositionCurrent.x = this.farmerPositionReal.x
		this.farmerPositionCurrent.y = this.farmerPositionReal.y
		this.cockerelPositionCurrent.x = this.cockerelPositionReal.x
		this.cockerelPositionCurrent.y = this.cockerelPositionReal.y
	},
	methods: {
		setTurn(turn) {
			this.turn = turn
			if (turn === 'computer') {
				this.$emit('xhrRequest', {moveObject: 'cockerel'})
			}
			this.mode = 'await'
		},
		changeTurn() {
			if (this.turn === 'player') {
				this.turn = 'computer'
				this.$emit('xhrRequest', {moveObject: 'cockerel'})
			}
			else if (this.turn === 'computer') this.turn = 'player';
		},
		isPositionPossible(rowNum, columnNum) {
			return this.possiblePositions.some(elem => {return JSON.stringify(elem) === JSON.stringify([columnNum, rowNum])})
		},
		requestToMoveFarmerToPosition(rowNum, columnNum) {
			if (this.isPositionPossible(rowNum, columnNum)) {
				this.$emit('xhrRequest', {moveObject: 'farmer', moveTo: {x: columnNum, y: rowNum}})
			}
		},
		updatePosition(turn, newPosition) {
			if (turn === 'player') {
				this.mode = 'move'
				this.playAnimation(this.farmerPositionCurrent, newPosition)
			}
			else if (turn === 'computer') {
				this.mode = 'move'
				this.playAnimation(this.cockerelPositionCurrent, newPosition)
			}
		},
		playAnimation(positionFrom, positionTo) {
			const stepX = (positionFrom.x - positionTo.x) / 10
			const stepY = (positionFrom.y - positionTo.y) / 10

			const moveAnimation = setInterval(function(){
				const distY = Math.abs(positionFrom.y - positionTo.y)
				const distX = Math.abs(positionFrom.x - positionTo.x)

				if (distX < 0.01 && distY < 0.01) {
					this.$set(positionFrom, 'x', positionTo.x)
					this.$set(positionFrom, 'y', positionTo.y)
					this.mode = 'await'
					this.changeTurn()
					clearInterval(moveAnimation)
				}
				else {
					const newXposition = positionFrom.x - stepX 
					const newYposition = positionFrom.y - stepY
					console.log(newXposition, newYposition)
					this.$set(positionFrom, 'x', newXposition)
					this.$set(positionFrom, 'y', newYposition)
				}
			}.bind(this), 20)
		}
	},
}
</script>