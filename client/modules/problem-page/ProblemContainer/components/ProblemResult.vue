<template>
    <div class="result_area">
        <div :class="answerStatus ? 'correct' : 'incorrect'"> {{ answerStatus ? 'Верно': 'Heверно' }} </div>
        <div class="answer"> Ваш ответ: {{ answer }} </div>
    </div>
</template>

<script>
export default {
    props: {
        answer: {default: ''},
        answerStatus: {default: false},
    }
}
</script>

<style scoped>
.result_area{
    display: inline-flex;
    flex-direction: column;
    align-items: stretch;
    align-self: stretch;
    gap: 10px;
    font-size: 21px;
	font-family: Montserrat Alternates;
	font-weight: 700;
}

.result_area div {
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
</style>