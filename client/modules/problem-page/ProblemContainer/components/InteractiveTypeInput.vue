<template>
    <div class="problem_input">
        <AnswerButton @sendAnswer="sendAnswer"/>
        <HintButton v-if="hasHint" @getHint="getHint" :hintCost="hintCost" />
    </div>
</template>

<script>
import AnswerButton from './components/AnswerButton.vue'
import HintButton from './components/HintButton.vue'

export default {
    components: {
        AnswerButton,
        HintButton,
    },
    
    props: {
        hasHint: {default: false},
        hintCost: {default: "1 квантик"},
    },

    methods: {
        getHint() {
            this.$emit('getHint')
        },
        sendAnswer() {
            this.$emit('sendAnswer')
        }
    },
}
</script>

<style scoped>
.problem_input {
    display: inline-flex;
    align-self: stretch;
    justify-content: space-between;
    align-items: center;
}
@media(max-width: 800px) {
	.problem_input {
		flex-direction: column;
		align-items: stretch;
		gap: 10px;
		font-size: 12px;
	}
}
</style>
