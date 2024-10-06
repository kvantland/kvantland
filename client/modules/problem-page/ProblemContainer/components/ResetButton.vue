<template>
	<button class="test_mode_reset_button" @click="resetProblem">
		Сбросить
	</button>
</template>

<script>
export default {
	methods: {
		resetProblem() {
			this.$emit('resetProblem')
		}
	}
}
</script>

<style scoped>
.test_mode_reset_button {
	width: 100%;
	height: 60px;
	border-radius: 10px;
	background-color: lightcoral;
	font-weight: 700;
	font-size: 24px;
	border: 2px solid red;
	cursor: pointer;
}
</style>