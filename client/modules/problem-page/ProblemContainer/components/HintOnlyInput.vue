<template>
    <div class="problem_input">
        <HintButton v-if="hasHint" :hint-cost="hintCost" @getHint="getHint" />
    </div>
</template>

<script>
import HintButton from './components/HintButton.vue';

export default {
    
    components: {
        HintButton,
    },
    props: {
        hintCost: {
			default: "1 квантик",
			type: String,
		},
		hasHint: {
			default: true,
			type: Boolean,
		}
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