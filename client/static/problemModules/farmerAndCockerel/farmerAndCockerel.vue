<template>
	<div class="play-board">
		<div 
			v-if="mode === 'chooseTurn'"
			class="play-board__buttons">
			<button class="play-board__button" @click="setTurn('player')"> Ходить первым </button>
			<button class="play-board__button" @click="setTurn('computer')"> Ходить вторым </button>
		</div>
		<p v-else-if="mode === 'game'" :class="['turn_sign', turn]"> 
			{{ turn === 'player' ? 'Ваш ход' : 'Ход компьютера' }} 
		</p>
		<svg 
			version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
			preserveAspectRatio="xMidYMid meet" 
			overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
			<line 
				v-for="_, lineNum in boardWidth + 1" :key="`line_vertical_num-${lineNum}`"
				:x1="boardItemSide * lineNum" y1="0"
				:x2="boardItemSide * lineNum" :y2="boardHeight * boardItemSide" />
			<line 
				v-for="_, lineNum in boardHeight + 1" :key="`line_horizontal_num-${lineNum}`"
				x1="0" :y1="boardItemSide * lineNum"
				:x2="boardWidth * boardItemSide" :y2="boardItemSide * lineNum" />
			<image 
				:x="boardItemSide * farmerPosition.x" :y="boardItemSide * farmerPosition.y"
				:width="boardItemSide" :height="boardItemSide"
				:href="`/problem_assets/farmer_and_cockerel/farmer.svg`" />
			<image 
				:x="boardItemSide * cockerelPosition.x" :y="boardItemSide * cockerelPosition.y"
				:width="boardItemSide" :height="boardItemSide"
				:href="`/problem_assets/farmer_and_cockerel/cockerel.svg`" />
		</svg>
	</div>
</template>

<script>
export default {
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		}
	},
	data() {
		return {
			mode: 'chooseTurn',
			turn: undefined,
			boardItemSide: 50,
		}
	},
	computed: {
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
		farmerPosition() {
			return {x: this.problemParams.farmer_coordinates[1], y: this.problemParams.farmer_coordinates[0]}
		},
		farmerPositionStr() {
			return this.farmerPosition.x + ' ' + this.farmerPosition.y
		},
		cockerelPosition() {
			return {x: this.problemParams.cockerel_coordinates[1], y: this.problemParams.cockerel_coordinates[0]}
		},
		cockerelPositionStr() {
			return this.cockerelPosition.x + ' ' + this.cockerelPosition.y
		}
	},
	methods: {
		setTurn(turn) {
			this.turn = turn
			this.mode = 'game'
		}
	},
}
</script>