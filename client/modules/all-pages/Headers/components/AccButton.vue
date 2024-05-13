<template>
    <NuxtLink to="/acc">
        <div class="acc_button_container">
        <img class="acc_button_image" src="/icons/acc.svg" />
        </div>
    </NuxtLink>
</template>

<style>
.acc_button_image {
	width: 70px; 
	height: 44px;
}

.acc_button_container {
	display: flex;
	width: 60px;
	height: 44px;
	border-radius: 10px; 
	background-color: rgba(0, 0, 0, 0);
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25)
}
</style>