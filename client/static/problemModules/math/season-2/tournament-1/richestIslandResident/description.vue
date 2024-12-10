<template>
	<p class="description" style="white-space: pre-line;">
		Жители острова Дональд, Билл и Илон как-то обсуждали, кто из них самый богатый. 
		{{ names[0] }}: <i>«{{ names[1] }} не самый богатый».</i>
		{{ names[1] }}: <i>«Я богаче, чем {{ names[0] }}.</i>
		{{ names[2] }}: <i>«{{ names[1] }} богаче меня».</i>
		Известно, что самый богатый житель острова солгал, а остальные сказали правду.
		Расположите жителей в порядке убывания богатства.
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
		names() {
			return this.problemParams.names
		}
	}
}
</script>