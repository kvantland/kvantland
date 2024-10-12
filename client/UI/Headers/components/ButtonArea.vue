<template>
    <div class="button_area">
        <slot></slot>
    </div>
</template>

<style scoped>
    .button_area {
	justify-content: flex-start; 
	align-items: center; 
	gap: 20px; 
	display: inline-flex;
	height: min(5vw, 44px);
}
@media(max-width: 800px) {
	.button_area {
		height: 30px;
		gap: 10px;
	}
}
</style>