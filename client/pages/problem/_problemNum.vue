<template>
    <div class="content_wrapper">
        <ProblemContainer :title="title" :description="description" :cost="cost" />
    </div>
</template>

<script>
import ProblemContainer from '../../modules/problem-page/ProblemContainer.vue'

export default {
    components: {
        ProblemContainer,
    },

    data() {
        return {
            title: 'TEst',
            description: 'TESt',
            cost: 34,
        }
    }
}
</script>

<style scoped>
.content_wrapper{
	margin-top: 130px;
	box-sizing: border-box;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 40px;
	display: inline-flex;
	padding-bottom: 80px;
	width: 100%;
    padding-left: max(40px, min(5vw, 80px));
    padding-right: max(40px, min(5vw, 80px));
}
</style>