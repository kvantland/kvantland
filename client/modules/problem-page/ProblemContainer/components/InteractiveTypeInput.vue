<template>
    <div class="problem_input">
        <form id="problem_form" method="post">
            <input type="hidden" name="progress" />
            <input type="hidden" name="answer" />
            <AnswerButton />
        </form>
        <HintButton v-if="hasHint" />
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
    }
}
</script>

<style scoped>
.problem_input {
    display: inline-flex;
    align-self: stretch;
    justify-content: space-between;
}
</style>
