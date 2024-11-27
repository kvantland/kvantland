<template>
	<div class="game-plot">
		<div class="tries">
			<template
				v-for="tryRow, tryRowNum in tries">
				<div 
					v-for="tryItem, tryItemNum in tryRow"
					:key="`try-item_row-${tryRowNum}_num-${tryItemNum}`"
					class="try__item">
					{{ tryItem }}
				</div>
				<div :key="`try__result_num-${tryRowNum}`" class="try__result">
					<p v-if="results[tryRowNum]?.number" class="result__number"> {{ results[tryRowNum].number }} </p>
					<div :class="['circle', `circle_${results[tryRowNum].color}`]"></div>
				</div>
			</template>
		</div>
	<Safe 
		:slots-amount="3" 
		:start-values="['*', '*', '*']"
		style="width: 25%; height: 30%;" 
		@changeConfig="changeConfig">
	</Safe>
	</div>
	
</template>

<script>
import Safe from '../components/Safe.vue';

export default {
	components: {
		Safe,
	},
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
			results: [
				{number: 1, color: 'green'},
				{number: 1, color: 'yellow'},
				{number: 2, color: 'yellow'},
				{color: 'red'},
				{number: 1, color: 'yellow'},
			]
		}
	},
	computed: {
		tries() {
			return this.problemParams?.tries
		}
	},
	methods: {
		changeConfig(newValue) {
			const ans = []
			for (const slot of newValue) {
				ans.push(slot[1])
			}
			this.$emit('updateAnswer', ans)
		}
	}
}
</script>