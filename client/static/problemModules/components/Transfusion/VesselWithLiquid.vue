<template>
	<div :class="['vessel', `vessel_choosed-${choosed}`, `vessel_visible-${visible}`]" @click="$emit('choose')">
		<div class="vessel__liquid" :style="`height: ${(currentHeight + addLiquid) / maxHeight * 100}%`"></div>
		<img class="vessel__mask" src="/problem_assets/transfusions/mask.svg" />
		<img  class="vessel__image" src="/problem_assets/transfusions/empty_vessel.svg">
	</div>
</template>

<script>
export default {
	props: {
		maxHeight: {
			type: Number,
			default: 12
		},
		currentHeight:  {
			type: Number,
			default: 0
		},
		choosed: {
			type: Boolean,
			default: false
		},
		visible: {
			type: Boolean,
			default: true
		},
		addLiquid: {
			type: Number,
			default: 0
		}
	},
}
</script>

<style lang="scss" scoped>
.vessel {
	background-color: rgba(177, 224, 218, 1);
	overflow: hidden;
	position: relative;
	display: inline-flex;
	flex-direction: column;
	justify-content: end;
	transition: 0.3s all;
	cursor: pointer;

	&_visible-false {
		opacity: 0;
	}

	&_choosed-true {
		background-color: rgb(152, 194, 190);
	}

	&_choosed-true > .vessel__liquid {
		background-color: rgb(71, 139, 172);
	}

	&__liquid {
		display: flex;
		background-color: rgba(94, 186, 231, 1);
		width: 100%;
		position: absolute;
		margin-bottom: 0;
		transition: 0.3s all;
	}

	&__image {
		z-index: 1;
		width: 100%;
		height: 100%;
	}
	&__mask {
		overflow: hidden;
		position: absolute;
	};
}
</style>