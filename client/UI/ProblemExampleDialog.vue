<template>
    <DialogShadowScreen>
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
    </DialogShadowScreen>
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

<style scoped>
.dialog {
	position: fixed;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	-webkit-transform: translate(-50%, -50%);
	padding: 40px 60px;
	gap: 40px;
	border-radius: 20px;
	background: #1E8B93;
	flex-direction: column;
	justify-content: flex-start;
	z-index: 4;
    display: inline-flex;
    animation: show 0.2s;
}

.dialog .body {
	box-shadow: 12px 12px 14px rgba(0, 0, 0, 0.25);
	border-radius: 16px;
	justify-content: center;
	align-items: center;
	font-size: 24px;
	padding: 10px 10px;
	background-color: white;
	display: inline-flex;
	flex-direction: row;
	gap: 10px;
}

.dialog .body .bold_text {
	font-weight: 600;
}

.dialog .head {
	display: inline-flex;
	flex-direction: row;
	justify-content: space-between;
	color: white;
	font-size: 24px;
	font-weight: 600;
}

.dialog .head p {
	font-family: Montserrat Alternates;
}

.dialog .cross {
	user-select: none;
	-webkit-user-select: none;
	cursor: pointer;
	width: 20px;
	height: 20px;
}

.dialog img.ans {
	height: 298px;
}

.dialog .button{
	user-select: none;
	-webkit-user-select: none;
	cursor: pointer;
	width: 580px;
	box-sizing: border-box;
	padding: 10px 20px;
	background: linear-gradient(180deg, #FCFCFC 16%, white 20%, #FFFFFF 55%, #EFEFEF 80%); 
	box-shadow: 7px 7px 6.699999809265137px #1A5866; 
	border-radius: 10px;
	font-size: 24px;
	font-weight: 600;
	text-align: center;
	justify-content: center;
	display: inline-flex;
}
</style>