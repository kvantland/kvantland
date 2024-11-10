<template>
	<div class="buttons">
		<button class="weight_button" @click="startWeight"> Взвесить </button>
		<button class="clear_button" @click="clearScales"> Очистить весы </button>
		<div class="remaining_weightings"> Осталось взвешиваний: {{ weightingsAmount }}</div>
		<div v-if="weightingHistory.length" class="history">
			<p v-for="(item, itemNum) in weightingHistory" :key="`history-item_num-${itemNum}`"> 
				<span style="font-weight: 600;"> Взвешивание {{ itemNum + 1 }}: </span> <br/>
				{{ item }} 
			</p>
		</div>
  </div>
</template>

<script>
export default {
	props: {
		weightingsAmount: {
			type: String,
			default: '0'
		},
		weightingHistory: {
			type: Array,
			default: () => []
		}
	},
	methods: {
		startWeight() {
			this.$emit('startWeight')
		},
		clearScales() {
			this.$emit('clearWeights')
		}
	}
}
</script>