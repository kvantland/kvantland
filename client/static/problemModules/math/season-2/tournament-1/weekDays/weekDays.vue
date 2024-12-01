<template>
	<div class="week-grid">
		<div 
			v-for="day, dayNum in days"
			:key="`week-day_num-${dayNum}`"
			:class="['week-day', `week-day_choosed-${day.choosed}`]"
			@click="chooseDay(dayNum)">
			<div class="left-decoration"></div>
			<div class="right-decoration"></div>
			<div class="week-day__title">
				{{ day.title }}
			</div>
			<p class="month-day"> {{ monthDay }} </p>
		</div>
	</div>
</template>

<script>
export default {
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
			days: [
				{title: 'Понедельник', choosed: false},
				{title: 'Вторник', choosed: false},
				{title: 'Среда', choosed: false},
				{title: 'Четверг', choosed: false},
				{title: 'Пятница', choosed: false},
				{title: 'Суббота', choosed: false},
				{title: 'Воскресенье', choosed: false}
			]
		}
	},
	computed: {
		monthDay() {
			return this.problemParams.month_day
		}
	},
	methods: {
		chooseDay(dayNum) {
			this.days[dayNum].choosed = !this.days[dayNum].choosed
			this.$emit('updateAnswer', this.days)
		}
	}
}
</script>