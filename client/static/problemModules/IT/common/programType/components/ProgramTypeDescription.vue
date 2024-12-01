<template>
	<div class="description">
		<slot />
		<TestGroupsTable v-if="testGroups.length" :table-rows="testGroups" />
		<InputExamplesTable v-if=inputExamples.length :input-examples="inputExamples" />
	</div>
</template>

<script lang="ts">
import InputExamplesTable from './InputExamplesTable.vue';
import TestGroupsTable from './TestGroupsTable.vue';

export default {
	components: {
		InputExamplesTable,
		TestGroupsTable,
	},
	props: {
		inputExamples: {
			type: Array,
			default: () => [],
		},
		testGroups: {
			type: Array,
			default: () => []
		}
	},
	setup(props: any) {
		return props.inputExamples
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
