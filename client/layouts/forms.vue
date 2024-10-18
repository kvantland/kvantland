<template>
    <div class="background" style="background-color: #D2E8E9; min-height: 100vh;">
        <DefaultHeader />
		<div class="content_wrapper">
			<UserScore v-if="$auth.loggedIn" />
			<Nuxt />
			<InfoFooter class="down"/>
		</div>
    </div>
</template>

<style scoped>
.form_footer {
	width: 100%;
	position: absolute;
	bottom: 0%;
}
.content_wrapper {
	display: inline-flex;
	flex-direction: column;
	box-sizing: border-box;
	width: 100%;
	height: 100%;
	padding: 0 max(40px, min(5vw, 80px));
}
@media (max-width: 800px) {
	.content_wrapper {
		margin-top: 80px;
		padding: 16px;
	}
	.down {
		margin-top: auto;
	}
}
</style>