<template>
	<div>
		<StartHeader />
		<div class="content_wrapper_start">
			<Nuxt />
			<InfoFooter/>
		</div>
	</div>
</template>

<style scoped>
.content_wrapper_start {
	margin-top: 130px;
	display: inline-flex;
	flex-direction: column;
	box-sizing: border-box;
	padding: 0 max(40px, min(5vw, 80px));
	width: 100%;
}
@media (max-width: 800px) {
	.content_wrapper_start {
		margin-top: 80px;
		padding: 16px;
	}
}
</style>