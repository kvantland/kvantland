<template>
    <div class="problem" :num="`${num}`">
        <div class="head">
            <div class="name"> {{ problemInfo.title }} </div>
            <div class="cost"> {{ problemInfo.cost }} </div>
        </div>

        <div class="body">
            <div class="text_container">
                <div v-html="problemInfo.desc"></div>
            </div>
            <img class="image" loading="lazy" :src="`/problem_example_img/${problemInfo.image}`" />
        </div>

        <div v-if="problemInfo.answer || problemInfo.solution_video_link" class="button_area">
            <div v-if="problemInfo.answer" class="button answer" @click="showAnswer"> Посмотреть ответ </div>
            <div v-if="problemInfo.solution" class="button solution" @click="showSolution"> Посмотреть решение </div>
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

<style scoped>
.problem { 
    display: flex;
	padding: 40px 60px; 
	background: #1E8B93; 
	border-radius: 20px; 
	flex-direction: column; 
	align-items: flex-start; 
	gap: 40px; 
}

.problem .head {
    width: 100%;
	justify-content: space-between; 
	align-items: center; 
	display: inline-flex;
}

.problem .name {
	color: white; 
	font-size: max(30px, min(40px, 2.6vw)); 
	font-family: Montserrat Alternates; 
	font-weight: 500;
}

.problem .cost {
	user-select: none;
	-webkit-user-select: none;
	align-self: center;
	padding: 10px 50px;
	border-radius: 10px; 
	border: 2px white solid; 
	color: white; 
	font-size: 24px; 
	font-family: Montserrat Alternates; 
	font-weight: 500;
	white-space: nowrap;
}

.problem img {
    align-self: center;
	max-height: 298px;
	max-width: 40% !important;
}

.problem .body {
	 padding: 40px; 
	 background: white; 
	 box-shadow: 12px 12px 14px rgba(0, 0, 0, 0.25); 
	 border-radius: 16px; 
	 justify-content: center; 
	 align-items: center; 
	 gap: 40px; 
	 display: inline-flex;
     min-height: 298px;
}

.problem .body .text_container {
	display: flex;
	flex-direction: column;
	justify-content: center;
	text-align: justify;
    font-size: max(15px, min(22px, 1.7vw)); 
	font-weight: 500;
}

>>> .bold_text {
	color: black;
	font-size: max(15px, min(22px, 1.7vw)); 
	font-weight: 700;
}

.problem .button_area {
	justify-content: flex-start; 
	align-items: center; 
	gap: 40px; 
	display: inline-flex;
    align-self: stretch;
}

.problem .button {
	user-select: none;
	-webkit-user-select: none;
	cursor: pointer;
	flex: 1 1 0; 
	padding: 10px 20px 10px 20px;
	background: linear-gradient(180deg, #FCFCFC 16%, white 20%, #FFFFFF 55%, #EFEFEF 80%); 
	box-shadow: 7px 7px 6.699999809265137px #1A5866; 
	border-radius: 10px; 
	overflow: hidden; 
	justify-content: center; 
	align-items: center; 
	text-align: center;
	color: black; 
	font-size:  max(15px, min(24px, 1.8vw));
	white-space: nowrap; 
	font-weight: 600;
}
</style>