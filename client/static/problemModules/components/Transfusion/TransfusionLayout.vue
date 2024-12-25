<template>
	<div class="game-plot">
		<VesselWithLiquid 
			v-for="vessel, vesselNum in config"
			:key="`vessel_num-${vesselNum}`"
			:current-height = vessel>
		</VesselWithLiquid>
	</div>
</template>

<script>
import VesselWithLiquid from './VesselWithLiquid.vue';

export default {
	components: {
		VesselWithLiquid,
	},
	props: {
		config: {
			type: Array,
			default: () => {return []}
		}
	}
}
</script>

<style lang="scss" scoped>
.game-plot {
	width: 100%;
	display: inline-flex;
	justify-content: space-between;
}
</style>