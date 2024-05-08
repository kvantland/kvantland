<template>
    <div class="problem" :num="`${num}`">
        <div class="head">
            <div class="name"> {{ problemInfo.title }} </div>
            <div class="cost"> {{ problemInfo.cost }} </div>
        </div>

        <div class="body">
            <div class="text_container">
                <p v-html="problemInfo.desc"></p>
            </div>
            <img class="image" loading="lazy" :src="`/problem_example_img/${problemInfo.image}`" />
        </div>

        <div class="button_area">
            <div class="button answer" @click="showAnswer"> Посмотреть ответ </div>
            <div class="button solution" @click="showSolution"> Посмотреть решение </div>
	    </div>
	 </div>
</template>

<script>
export default {
    props: ["problemInfo", "num"],

    methods: {
        showAnswer() {
            this.$emit('showDialog', 'answer', {'num': this.num, 'problemInfo': this.problemInfo})
        },
        showSolution() {
            this.$emit('showDialog', 'solution', {'num': this.num, 'problemInfo': this.problemInfo})
        },
    }
};
</script>