<template>
	<div class="game-plot">
		<div class="vessels">
			<div 
				v-for="vessel, vesselNum in vesselConfig" 
				:key="`vessel_num-${vesselNum}`" 
				class="vessel-with-sign">
					<div class="animation-section">
						<img 
							v-if="mode==='animation' && vesselNum === animationObjects.to"
							:class="['animation-vessel', `animation-vessel_${animationSide}`]"
							src="/problem_assets/transfusions/animation-vessel.svg" />
						<div 
							v-if="mode==='animation' && vesselNum === animationObjects.to"
							:class="['input-field', `input-field_${animationSide}`]">
							<p>Перелить:</p>
							<form @submit.prevent="setLiquidAddAmount">
								<input v-model="liquidAmount" />
							</form>
						</div>
					</div>
					<VesselWithLiquid 
						:visible="mode !== 'animation' || animationObjects.from !== vesselNum"
						:current-height=vessel 
						:choosed="choosed[vesselNum]" 
						:add-liquid="Number(mode === 'animation') * addLiquid * Number(vesselNum === animationObjects.to)"
						:max-height="maxHeight"
						@choose="choose(vesselNum)"
						/>
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
		vesselConfig: {
			type: Array,
			default: () => {return []}
		},
		maxHeight: {
			type: Number,
			default: 12
		},
		newXhr: {
			type: Boolean,
			default: false
		},
		xhrData: {
			type: Object,
			default: () => {return {}}
		}
	},
	data() {
		return {
			mode: 'choose',
			choosed: this.vesselConfig ? new Array(this.vesselConfig.length).fill(false) : [],
			animationSide: undefined,
			animationObjects: {
				from: undefined,
				to: undefined,
			},
			liquidAmount: 0,
			addLiquid: 0,
		}
	},
	watch: {
		newXhr(isNew) {
			this.$emit('xhrGet')
			if (isNew && this.xhrData.xhr_answer === 'success') {
				setTimeout(function() {this.stopAnimation()}.bind(this), 400)
			}
			else if (this.xhrData.xhr_answer === 'unsuccess' && isNew) {
				this.$emit('showXhrDialog', "Невозможное действие!")
				this.stopAnimation()
			}
		}
	},
	methods: {
		choose(vesselNum) {
			if (this.mode === 'animation' || this.animationObjects.from === vesselNum) {
				return;
			}
			this.$set(this.choosed, vesselNum, !this.choosed[vesselNum])
			if (this.choosed.filter(item => item).length === 2) {
				this.$set(this.animationObjects, 'to', vesselNum)
				this.animationSide = 
					this.animationObjects.to - this.animationObjects.from > 0 ? 'left' : 'right'
				this.mode = 'animation'
			}
			else {
				this.$set(this.animationObjects, 'from', vesselNum)
			}
		},
		setLiquidAddAmount() {
			console.log('here!')
			this.$emit('transfusion', {objects: this.animationObjects, liquid: this.liquidAmount})
		},
		stopAnimation() {
			this.mode = 'choose'
			this.liquidAmount = 0
			this.animationObjects =
			{
				to: undefined,
				from: undefined
			}
			this.choosed = new Array(this.vesselConfig.length).fill(false)
		}
	}
}
</script>

<style lang="scss" scoped>
.vessels {
	width: 100%;
	display: inline-flex;
	justify-content: space-between;
	padding: 0 160px;
	box-sizing: border-box;
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

.animation-section {
	height: 50px;
}

.animation-vessel {
	position: absolute;
	&_left {
		margin-top: -4%;
		margin-left: -7%;
		animation: showLeft 1s;
	}
	&_right {
		transform: scale(1, -1) rotate(180deg);
		margin-top: -4%;
		margin-left: 3%;
		animation: showRight 1s;
	} 
}


@keyframes showLeft {
	from {
		transform: translate(-10px, 20px);
		opacity: 0;
		rotate: (-45deg);
	}
	to {
		transform: translate(0, 0);
		opacity: 1;
		rotate: (0);
	}
}

@keyframes showRight {
	from {
		transform: scale(1, -1) translate(-10px, 20px);
		opacity: 0;
		rotate: (230deg);
	}
	to {
		transform: scale(1, -1) translate(0, 0);
		opacity: 1;
		rotate: (180deg);
	}
}

.input-field {
	display: inline-flex;
	flex-direction: column;
	position: absolute;
	animation: show 0.3s;
	&_left {
		margin-left: 5%;
	}
	&_right {
		transform: translate(-90%, 0);
	}
	margin-top: -1%;
	gap: 5px;
	align-items: center;
	>p {
		color: rgba(30, 139, 147, 1);
		font-family: Montserrat ALternates;
		font-weight: 600;
	}
	input {
		background-color: rgba(30, 139, 147, 1);
		align-self: stretch;
		width: 160px;
		color: white;
		font-size: 24px;
		font-family: Montserrat Alternates;
		font-weight: 700;
		box-sizing: border-box;
		text-align: center;
		padding: 10px 0px;
		outline: none;
		border: none;
		border-radius: 10px;
	}
}
</style>