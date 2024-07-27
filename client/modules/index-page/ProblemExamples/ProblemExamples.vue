<template>
    <div class="examples_container" id="problemExamples">
        <p class="page_header"> Примеры задач </p>
        <div class="content">
            <ProblemExample v-for="(problem, num) in problemExamples" 
            v-if="num == currentExampleProblemNum" :problemInfo="problem" 
            :key="problem.title" :num="num" @showDialog="showDialog" />
        </div>
        <ProblemExampleNav :pageAmount="problemAmount" 
        :selectedNum="currentExampleProblemNum" @changeProblem="updateCurrentProblemNum"/>
    </div>
</template>

<script>
import ProblemExample from "./components/ProblemExample.vue"
import ProblemExampleNav from "./components/ProblemExampleNav.vue"

export default {
    props: ['problemExamples'],

    components: {
        ProblemExample,
        ProblemExampleNav,
    },

    data() {
        return {
            currentExampleProblemNum: 0,
            dialogType: null,
            dialogData: null,
        }
    },

    computed: {
        problemAmount() {
            return this.problemExamples.length
        }
    },

    methods: {
        updateCurrentProblemNum(curNum) {
            this.currentExampleProblemNum = curNum
        },
        showDialog(dialogType, dialogData) {
            this.dialogType = dialogType
            this.dialogData = dialogData
            this.$emit('showDialog', this.dialogType, this.dialogData)
        }
    },
}
</script>

<style scoped>
.examples_container {
	flex-direction: column; 
	justify-content: flex-start; 
	align-items: flex-start; 
	gap: 40px; 
	display: flex;
}

.examples_container .content {
	flex-direction: column; 
	justify-content: flex-start; 
	align-items: flex-start; 
	gap: 20px; 
	display: flex;
}

.page_header {
	color: #1E8B93;
	font-size: 40px;
	font-family: Montserrat Alternates;
	font-weight: 600;
}
</style>