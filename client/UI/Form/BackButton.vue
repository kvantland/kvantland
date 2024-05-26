<template>
    <button class="back_button" type="button" @click="back"> Назад </button>
</template>

<script>
export default {
    methods: {
        back() {
            history.back()
        }
    }
}
</script>

<style>
.back_button {
	align-self: stretch;
	display: flex;
	justify-content: center;
	align-items: center;
	height: 50px;
	color: #1E8B93;
	font-size: 14px;
	font-weight: 600;
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25); 
	border-radius: 6px;
	border: 1px #1E8B93 solid;
	background-color: white;
    font-family: Montserrat;
    cursor: pointer;
}
</style>