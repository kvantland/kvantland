<template>
    <div class="problem_input">
        <InputArea />
        <HintButton />
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