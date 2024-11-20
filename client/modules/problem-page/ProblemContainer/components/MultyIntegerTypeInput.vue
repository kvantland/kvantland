<template>
	<div class="problem-input">
		<MultyInputArea @sendAnswer="sendAnswer" />
		<HintButton v-if="hasHint" @getHint="getHint" :hintCost="hintCost" />
	</div>
</template>

<script>
import MultyInputArea from './components/MultyInputArea.vue';

export default {
	components: {
		MultyInputArea,
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