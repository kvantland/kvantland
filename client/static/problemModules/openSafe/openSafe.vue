<template>
	<div class="game-plot">
		<div class="tries">
			<table
				v-for="tryTable, tryTableNum in tries" 
				:key="`try-table_num-${tryTableNum}`"
				class="try-table">
				<tbody>
					<tr>
						<td 
							v-for="key, keyNum in tryTable" 
							:key="`try__item_num-${keyNum}`"
							class="try__item">
							{{ key }}
						</td>
						<td class="description">
							{{ results[tryTableNum] }}
						</td>
					</tr>
				</tbody>
			</table>
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
				'одна цифра верна и на месте',
				'одна цифра верна, но не на месте',
				'две цифры верны, но не на месте',
				'нет верных цифр',
				'одна цифра верна, но не на месте'
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