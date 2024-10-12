<template>
	<NuxtLink to="/login" style="height: 100%;">
		<div class="login_button"> Войти </div>
	</NuxtLink>
</template>

<style scoped>
.login_button {
	height: 100%;
	display: flex;
	align-items: center;
	padding: 0 20px;
	background: #1E8B93; 
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25); 
	border-radius: 10px;
	color: white; 
	font-size: min(2vw, 20px); 
	font-family: Montserrat Alternates; 
	font-weight: 600;
	cursor: pointer;
}
@media(max-width: 800px) {
	.login_button {
		border-radius: 4px;
		font-size: 14px;
	}
}
</style>