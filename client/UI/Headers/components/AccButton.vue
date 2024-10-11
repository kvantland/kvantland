<template>
    <NuxtLink to="/acc/previewInfo" style="height: 100%;">
        <div class="acc_button_container"> </div>
    </NuxtLink>
</template>

<style>
.acc_button_container {
	height: 100%;
	width: min(7vw, 60px);
	background-size: min(60px, 7vw) auto;
	border-radius: 10px; 
	background-image: url("/icons/acc.svg");
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25)
}
</style>