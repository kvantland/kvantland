<template>
	<ChessProblemLayout 
		:drag-figures="dragFigures"
		:board-configuration="boardConfiguration"
		style="width: 57%"
		@updateConfig="updateConfig" @updateFiguresAmount="updateFiguresAmount" />
</template>

<script>
import ChessProblemLayout from '../components/chessProblemLayout.vue';

export default {
	components: {
		ChessProblemLayout,
	},
	model: {
		prop: 'answer',
		event: 'updateAnswer',
	},
	props: {
		problemParams: {
			type: Object,
			default: () =>{}
		}
	},
	data() {
		return {
			dragFigures: [{type: 'rook_b', amount: 4}, {type: 'bishop_w', amount: 4}],
			boardConfiguration: []
		}
	},
	created() {
		const positions = this.problemParams.positions
		const configuration = []

		for (let row = 0; row < 8; row++) {
			configuration.push([])
			for (let column = 0; column < 8; column++) {
				if (!positions.some(position => position[0] === row && position[1] === column)) {
					configuration[row].push({type: '', moveStatus: ''})
				}
				else {
					configuration[row].push({type: 'rook_b', moveStatus: 'passive'})
				}
			}
		}
		this.boardConfiguration = configuration
	},
	methods: {
		updateConfig(newConfig) {
			this.boardConfiguration = newConfig
			this.$emit('updateAnswer', newConfig)
		},
		updateFiguresAmount(newValue) {
			if (this.dragFigures[newValue.index] !== 'inf') {
				this.$set(this.dragFigures[newValue.index], 'amount', newValue.amount)
			}
		}
	}
}
</script>