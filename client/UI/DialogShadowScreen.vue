<template>
    <div class="shadow">
        <slot />
    </div>
</template>

<style scoped>
.shadow {
	position: fixed;
	top: 0;
	left: 0	;
	width: 100%;
	min-height: 100vh;
	z-index: 10;
	background-color: rgba(0, 0, 0, 0.25)
}
</style>