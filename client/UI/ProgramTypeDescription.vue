<template>
	<div class="description">
		<slot />
		<InputExamplesTable v-if=inputExamples.length :input-examples="inputExamples" />
	</div>
</template>

<script>
export default {
	props: {
		inputExamples: {
			type: Array,
			default() {return []},
		}
	}
}
</script>

<style scoped>
.description {
	display: flex;
	flex-direction: column;
	gap: 10px;
}
</style>
