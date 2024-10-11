<template>
    <div class="button_area">
        <NuxtLink to="/login">
            <div class="login_button"> Войти </div>
        </NuxtLink>
    </div>
</template>

<style scoped>
.login_button {
	text-align: center;
	padding: 10px 20px;
	background: #1E8B93; 
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25); 
	border-radius: 10px; 
	overflow: hidden; 
	justify-content: center; 
	align-items: center; 
	gap: 10px; 
	display: inline-flex;
	color: white; 
	font-size: 20px; 
	font-family: Montserrat Alternates; 
	font-weight: 600;
	cursor: pointer;
}
</style>