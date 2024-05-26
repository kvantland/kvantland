<template>
    <div>
        <div class="shadow"></div>
        <div v-if="['answer', 'solution'].includes(dialogType)" class="dialog dialogType" :num="dialogData.num">
            <div class="head">
                <p>{{ problemInfo.title }}</p>
                <img class="cross" loading="lazy" @click="closeDialog" src="/icons/cross.svg"/>
            </div>
            <div class="body" v-if="dialogType == 'answer'">
                <p v-if="problemInfo.answer">
                    <span class="bold_text"> Ответ: </span>
                    {{ problemInfo.answer }}
                </p>
                <img v-else-if="problemInfo.solution_image" 
                    loading="lazy" class="ans" :src="`/problem_example_ans_img/${problemInfo.solution_image}`" />
            </div>
            <div class="body" v-else-if="dialogType == 'solution'">
                <iframe loading="lazy" width="560" height="315"
			        :src="problemInfo.solution_video_link"
		        	frameborder="0"  allowfullscreen></iframe>
            </div>
            <div v-if="dialogType == 'answer'" class="button solution" @click="showSolution">
                Посмотреть решение
            </div>
            <div v-else-if="dialogType == 'solution'" class="button answer" @click="showAnswer">
                Посмотреть ответ
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ["dialogType", "dialogData"],

    computed: {
        problemInfo(){
            return this.dialogData.problemInfo
        }
    },

    methods: {
        closeDialog() {
            this.$emit('closeDialog')
        },
        showAnswer() {
            this.$emit('changeDialog', 'answer', {'num': this.dialogData.num, 'problemInfo': this.problemInfo})
        },
        showSolution() {
            this.$emit('changeDialog', 'solution', {'num': this.dialogData.num, 'problemInfo': this.problemInfo})
        },
    }
}
</script>