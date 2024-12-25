<template>
	<div class="game-plot">
		<div class="vessels">
			<div v-for="vessel, vesselNum in config" :key="`vessel_num-${vesselNum}`" class="vessel-with-sign">
					<VesselWithLiquid :current-height = vessel />
					<div class="vessel__sign"> {{ vessel }} мл</div>
			</div>
		</div>
		<div class="table"></div>
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
.vessels {
	width: 100%;
	display: inline-flex;
	justify-content: space-between;
}

.vessel-with-sign {
	display: inline-flex;
	flex-direction: column;
	gap: 30px;
}

.vessel__sign {
	padding: 5px 0px;
	text-align: center;
	background-color: white;
	border: 2px rgba(30, 139, 147, 1) solid;
	border-radius: 10px;
	color: rgba(30, 139, 147, 1);
	font-size: 24px;
}

.game-plot {
	display: inline-flex;
	flex-direction: column;
	width: 100%;
}

.table {
	height: 10px;
	width: 100%;
	background-color: black;
	position: relative;
	top: -75px;
}
</style>