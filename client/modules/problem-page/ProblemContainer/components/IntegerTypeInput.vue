<template>
    <div class="problem_input">
        <InputArea @sendAnswer="sendAnswer" />
        <HintButton v-if="hasHint" @getHint="getHint" />
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
}
</style>