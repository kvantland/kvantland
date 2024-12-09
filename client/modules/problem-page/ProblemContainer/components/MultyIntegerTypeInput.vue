<template>
	<div class="problem-input">
		<MultyInputArea @sendAnswer="sendAnswer" />
		<HintButton v-if="hasHint" :hint-cost="hintCost" @getHint="getHint" />
	</div>
</template>

<script>
import MultyInputArea from './components/MultyInputArea.vue';
import HintButton from './components/HintButton.vue';

export default {
	components: {
		MultyInputArea,
		HintButton,
	},
	props: {
		hasHint: {default: false},
		hintCost: {default: "1 квантик"},
	},
	methods: {
		sendAnswer(answer) {
			this.$emit('sendAnswer', answer)
		},
		getHint() {
			this.$emit('getHint')
		}
	}
}
</script>

<style scoped>
.problem-input {
	display: inline-flex;
	justify-content: space-between;
	width: 100%;
}
</style>