<template>
	<ChessProblemLayout 
				style="width: 57%"
				:drag-figures="dragFigures" 
				:board-configuration="boardConfiguration" 
        @updateConfig="updateConfig"
        @updateFiguresAmount="updateFiguresAmount" />
</template>

<script>
import ChessProblemLayout from '~/static/problemModules/components/chessProblemLayout.vue';

export default {
	components: {
		ChessProblemLayout,
	},
	model: {
			prop: 'answer',
			event: 'updateAnswer'
	},
	props: ['problemParams'],
	data() {
			return {
					boardConfiguration: [],
					dragFigures: [{type: 'horse_b', amount: 'inf'}, {type: 'horse_w', amount: 'inf'}],
			}
	},
	created() {
		const positions = this.problemParams.startConfig
		const configuration = []

		for (let row = 0; row < 8; row++) {
			configuration.push([])
			for (let column = 0; column < 8; column++) {
				if (positions.white[0] === row && positions.white[1] === column) {
					configuration[row].push({type:'horse_w', moveStatus: 'passive'})
				}
				else if (positions.black[0] === row && positions.black[1] === column) {
					configuration[row].push({type: 'horse_b', moveStatus: 'passive'})
				}
				else {
					configuration[row].push({type: '', moveStatus: ''})
				}
			}
		}
		this.boardConfiguration = configuration
	},
	methods: {
			updateConfig(newConfig) {
					console.log(newConfig)
					this.boardConfiguration = newConfig
					this.$emit('updateAnswer', newConfig)
			},
			updateFiguresAmount(newValue) {
					console.log(newValue)
					if (this.dragFigures[newValue.index].amount !== 'inf') {
						this.$set(this.dragFigures[newValue.index], 'amount', newValue.amount)
					}
			}
	}
}
</script>