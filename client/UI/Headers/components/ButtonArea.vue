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
</style>