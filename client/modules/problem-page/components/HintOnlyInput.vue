<template>
    <div class="problem_input">
        <HintButton />
    </div>
</template>

<script>
import HintButton from './components/HintButton.vue';

export default {
    components: {
        HintButton,
    },
}
</script>

<style scoped>
.problem_input {
    display: inline-flex;
    align-self: stretch;
    justify-content: flex-end;
}
</style>