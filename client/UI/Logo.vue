<template>
	<NuxtLink to="/">
		<div class="logo_area">
			<img class="logo" loading="lazy" src="/icons/logo.svg" />
			<p class="logo_name"> КВАНТ<br/>ЛАНДИЯ </p>
		</div>
	</NuxtLink>
</template>

<style>
.logo_area {
	gap: 10px; 
	display: inline-flex;
	align-items: center;
}

.logo {
	width: min(5vw, 52px); 
	height: min(5vw, 52px);
}

.logo_name {
	color: #1E8B93; 
	font-size: min(2vw, 20px); 
	font-family: Montserrat Alternates; 
	font-weight: 600;
}
</style>