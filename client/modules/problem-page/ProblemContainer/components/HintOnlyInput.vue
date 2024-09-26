<template>
    <div class="problem_input">
        <HintButton :hintCost="hintCost" @getHint="getHint" />
    </div>
</template>

<script>
import HintButton from './components/HintButton.vue';

export default {
    
    components: {
        HintButton,
    },
    props: {
        hintCost: {default: "1 квантик"},
    },

    methods: {
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
    justify-content: flex-end;
    align-items: center;
}
</style>