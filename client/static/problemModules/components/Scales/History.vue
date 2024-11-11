<template>
	<div 
		class="buttons" 
		style="display: inline-flex;
    flex-direction: column;
    gap: 15px;
    max-width: 20%;
    align-items: stretch;
    font-size: max(14px, 1.5vw);
    font-family: Montserrat;">
		<button
			class="weight_button" 
			style="border-radius: 5px;
			display: inline-flex;
			align-items: center;
			justify-content: center;
			padding: 10px 20px;
			font: inherit;
			cursor: pointer;" 
			@click="startWeight">
			 Взвесить 
		</button>
		<button 
			class="clear_button" 
			style="padding: 10px 20px;
				border-radius: 5px;
				font: inherit;
				display: inline-flex;
				align-items: center;
				justify-content: center;
				cursor: pointer;"
			@click="clearScales"> 
				Очистить весы 
		</button>
		<div 
			class="remaining_weightings"
			style="display: inline-flex; justify-content: center; align-items: center; text-align: center; padding: 30px 10px; font: inherit; border-radius: 8px; background-color: white; border: 1px black solid;"> 
		Осталось взвешиваний: {{ weightingsAmount }}
		</div>
		<div 
			v-if="weightingHistory.length" 
			class="history" 
			style="padding: 1vh 5%;
				gap: max(15px, 1.8vw);
				display: inline-flex;
				flex-direction: column;
				font-size: 1.1vw;
				background-color: white;
				border: 1px black solid;
				border-radius: 8px;
				justify-content: center;">
			<p 
				v-for="(item, itemNum) in weightingHistory" :key="`history-item_num-${itemNum}`"
				style="display: inline-block;
					flex-direction: column;
					font-size: max(8px, 0.9vw);
					white-space: nowrap;"> 
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