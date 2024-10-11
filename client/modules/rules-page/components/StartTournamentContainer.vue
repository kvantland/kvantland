<template>
<div class="conformation_box">
	<p class="conformation_text">С правилами ознакомился(-лась) и готов(а) приступить!</p>
	<NuxtLink  to="/land" class="start_button_wrapper">
		<div class ="start_button"> Открыть турнир </div>
	</NuxtLink>
</div>
</template>
<style scoped>
.conformation_box {
	align-self: stretch;
	padding-left: 40px;
	padding-right: 40px;
	padding-top: 30px;
	padding-bottom: 30px;
	background: #1E8B93;
	border-radius: 20px;
	justify-content: space-between;
	align-items: center;
	gap: 10px;
	display: flex;
}

.conformation_text {
	font-weight: 600;
	color: white;
	font-size: max(15px, min(20px, 1.5vw));
}

.start_button {
	display: inline-flex;
	height: 50px;
	padding: 0 80px;
	background: linear-gradient(180deg, #FCFCFC 16%, white 20%, #FFFFFF 55%, #EFEFEF 80%);
	box-shadow: 7px 7px 6.699999809265137px #1A5866;
	border-radius: 10px;
	justify-content: center;
	align-items: center;
	gap: 10px;
	display: flex;
	text-align: center;
	color: black;
	font-size: max(17px, min(24px, 1.8vw));
	font-weight: 600;
}

@media(max-width: 800px) {
	.conformation_text {
		font-size: 14px;
	}
	.conformation_box {
		padding: 4vw 4vw;
		display: flex;
		flex-direction: column;
	}
	.start_button {
		height: 29px;
		white-space: nowrap;
	}
	.start_button_wrapper {
		width: 100%;
	}

}
</style>