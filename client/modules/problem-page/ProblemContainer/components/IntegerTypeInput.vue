<template>
    <div class="problem_input">
        <InputArea @sendAnswer="sendAnswer" />
        <HintButton v-if="hasHint" @getHint="getHint" :hintCost="hintCost" />
    </div>
</template>

<script>
import InputArea from './components/InputArea.vue';
import HintButton from './components/HintButton.vue';

export default {
    components: {
        InputArea,
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
.problem_input {
    display: inline-flex;
    align-self: stretch;
    justify-content: space-between;
    align-items: center;
}
</style>