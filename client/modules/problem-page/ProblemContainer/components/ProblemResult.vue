<template>
    <div class="result_area">
        <p :class="answerStatus ? 'correct' : 'incorrect'"> {{ answerStatus ? 'Верно': 'Heверно' }} </p>
        <p v-if="isInteger" class="answer"> Ваш ответ: {{ answer }} </p>
    </div>
</template>

<script>
export default {
    props: {
        answer: {default: ''},
        answerStatus: {default: false},
        isInteger: {default: false}
    }
}
</script>

<style scoped>
.result_area{
    display: inline-flex;
    flex-direction: column;
    align-items: stretch;
    align-self: stretch;
    font-size: 21px;
	font-family: Montserrat Alternates;
	font-weight: 700;
    padding-top: 23px;
	padding-bottom: 23px;
	background: white;
	box-shadow: 2.3333334922790527px 2.3333334922790527px 10.850001335144043px rgba(0, 0, 0, 0.25);
	border-radius: 12px;
	overflow: hidden;
	justify-content: center;
	align-items: center;
	gap: 5.83px;
	display: flex;
	flex-direction: column;
}

.incorrect {
    color: #B62C5A;
}

.correct {
    color: #17A814;
}

.answer {
    color: black;
    font-size: 24px;
    font-family: Montserrat;
    font-weight: 500;
}
</style>