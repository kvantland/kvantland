<template>
	<div>
		У ученого есть робот для переливания жидкостей, 
			а также колбы с жидкостями, содержащие \({{startConfig[0]}}\)&nbsp;мл, \({{startConfig[1]}}\)&nbsp;мл, 
			\({{startConfig[2]}}\)&nbsp;мл, \({{startConfig[3]}}\)&nbsp;мл и \({{startConfig[4]}}\)&nbsp;мл особого раствора. 
			Он хочет уравнять объемы в колбах за как можно меньшее число переливаний. Как это сделать? 
			За одно переливание выделяем две колбы - откуда и куда переливаем, вводим целое число мл, 
			которое хотим перелить, и нажимаем кнопку “Enter”.
			Каждая колба вмещает не более \(12\)&nbsp;мл. 
			Кнопку “Отправить” нужно нажать лишь после того, как уравняли объёмы во всех колбах.
	</div>
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
		startConfig() {
			return this.problemParams.default.current_config
		}
	}
}
</script>