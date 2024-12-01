<template>
	<p class="description" style="white-space: pre-line;">
		В поезде нечётное количество вагонов, причём между средним и {{wagon}}-м по счёту – {{ distance }} вагона. 

		Сколько всего вагонов может быть в этом поезде? Укажите все варианты. Новый ответ можно добавить кнопкой “+”.
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
		wagon() {
			return this.problemParams.wagon
		},
		distance() {
			return this.problemParams.distance
		}
	}
}
</script>