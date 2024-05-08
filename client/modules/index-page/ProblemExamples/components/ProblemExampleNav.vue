<template>
    <div class="nav">
        <img class="left_arrow" src="/icons/left_arrow.svg" @click="showPrevProblem"/>
        <div class="pages">
            <div v-for="(page, num) in pageAmount" 
                :class="num == selectedNum ? 'selected page' : 'page'" :num="num"></div>
        </div>
        <img class="right_arrow" src="/icons/right_arrow.svg" @click="showNextProblem"/>
    </div>
</template>

<script>
export default {
    props: ["pageAmount", "selectedNum"],

    methods: {
        showPrevProblem() {
            let curNum =  ((this.selectedNum - 1) + this.pageAmount) % this.pageAmount
            this.$emit('changeProblem', curNum)
        },

        showNextProblem() {
            let curNum =  ((this.selectedNum + 1) + this.pageAmount) % this.pageAmount
            this.$emit('changeProblem', curNum)
        }
    }
}
</script>
