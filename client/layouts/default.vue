<template>
    <div style="height: 100vh;">	
        <DefaultHeader />
		<div class="content_wrapper_default">
			<UserScore v-if="$auth.loggedIn"/>
			<Nuxt />
			<InfoFooter class="down"/>
		</div>
    </div>
</template>

<style scoped>
.content_wrapper_default {
	display: inline-flex;
	flex-direction: column;
	box-sizing: border-box;
	width: 100%;
	height: 100%;
}
@media (max-width: 800px) {
	.content_wrapper_default {
		margin-top: 80px;
		padding: 16px;
	}
	.down {
		margin-top: auto;
	}
}
</style>