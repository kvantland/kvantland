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
    components: {
        ProblemExample,
        ProblemExampleNav,
    },

    data() {
        return {
            problemExamples: {},
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

    async fetch() {
        const problemExamplesData = await this.$axios.$get('/problem_examples')
        this.problemExamples = problemExamplesData
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