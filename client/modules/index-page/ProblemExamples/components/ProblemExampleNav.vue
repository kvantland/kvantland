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

<style scoped>
.examples_container .nav {
	height: 53px; 
    width: 100%;
	justify-content: space-between; 
	align-items: center; 
	display: inline-flex;
}

.nav img{
	width: 100px;
	height: 53px;
	cursor: pointer;
}

.nav .pages {
	align-self: center;
	gap: 40px; 
	display: flex;
}

.nav .page.selected {
	width: 20px; 
	height: 20px; 
	background: #1E8B93;
	border-radius: 4px;
}

.nav .page {
	width: 20px; 
	height: 20px; 
	border-radius: 4px; 
	border: 2px #1E8B93 solid;
}
</style>
