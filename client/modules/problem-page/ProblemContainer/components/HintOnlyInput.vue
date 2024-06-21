<template>
    <div class="problem_input">
        <HintButton @getHint="getHint" :hintCost="hintCost" />
    </div>
</template>

<script>
import HintButton from './components/HintButton.vue';

export default {
    props: {
        hintCost: {default: "1 квантик"},
    },
    
    components: {
        HintButton,
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