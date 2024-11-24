<template>
	<p class="description">
		В {{ firstMonth }} было больше {{ dayType }}, чем в {{ secondMonth }} того же года. 
		Каким днём недели было {{ monthDay }} этого года? Выберите все варианты ниже.
	</p>
</template>

<script>
export default {
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		}
	},
	computed: {
		firstMonth() {
			return this.problemParams.first_month
		},
		secondMonth() {
			return this.problemParams.second_month
		},
		dayType() {
			return this.problemParams.day_type
		},
		monthDay() {
			return this.problemParams.month_day
		}
	}
}
</script>