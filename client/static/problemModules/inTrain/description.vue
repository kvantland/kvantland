<template>
	<p class="description" style="white-space: pre-line;">
		В поезде нечётное количество вагонов, причём между средним и {{wagon}}-м по счёту – {{ distance }} вагонов. 

		<b>Сколько всего вагонов может быть в этом поезде? Укажите все варианты.</b>
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