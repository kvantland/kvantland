<template>
	 <div class="svg_with_buttons">
    <svg
			ref="svg" version="1.1" class="display_svg" :viewBox="`0 0 0 0`"
				preserveAspectRatio="xMidYMid meet" 
				overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
			<Scales
				:scale="0.8" :left-cup-objects="cupWeights.left" :right-cup-objects="cupWeights.right" :move-to="newSide" 
				@svgHeight="getSvgHeight"
				@svgWidth="getSvgWidth" @moveFromCup="moveFromCup" @stopMove="stopWeight" />
			<DragContainer 
					:transform="`translate(0 ${weightHeight + gap})`" 
					item-image="weight.svg" :items-amount="5" :width="dragZoneWidth" />
		</svg>
		<History 
			:weighting-history="weightingHistory" 
			:weightings-amount="weightingsAmount"
			@clearWeights="clearWeights" @startWeight="startWeight"/>
	</div>
</template>

<script>
import Scales from '../components/Scales/Scales.vue';
import History from '../components/Scales/History.vue';
import DragContainer from '../components/Scales/containers/dragContainer.vue';

export default {
	components: {
		Scales, 
		History,
		DragContainer,
	},
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		}
	},
	data() {
		return {
			dragZoneWidth: 0,
			weightHeight: 0,
			gap: 50,
			cupWeights: {left: [], right: []},
			newSide: undefined,
			weightingHistory: [],
		}
	},
	computed: {
		weightingsAmount() {
			return this.weightings_amount
		}
	},
	methods: {
		getSvgWidth(width) {
			this.dragZoneWidth = width * 0.8
		},
		getSvgHeight(height) {
			this.weightHeight = height
		},
		moveFromCup() {
		},
		stopWeight(){
		},
		clearWeights(){
		},
		startWeight(){
		},
	}
}
</script>