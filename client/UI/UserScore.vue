<template>
    <div class="score_bar">
        <p class="name"> {{ $auth.user.name }} </p>
        <p class="score"> Счёт: {{ $auth.user.score }} </p>
    </div>
</template>

<style scoped>
.score_bar {
	display: none;
}

@media(max-width: 800px) {
	.score_bar {
		width: 100%;
		box-sizing: border-box;
		padding: 4px 0px;
		display: inline-flex;
		justify-content: center;
		gap: 20px;
		box-shadow: 0px 2px 14.8px 0px #00000033;
		border: 2px solid #1E8B93;
		border-radius: 6px;
		font-family: Montserrat Alternates;
		font-size: 14px;
		font-weight: 500;
		margin-bottom: 10px;
		background-color: white;
	}
}
</style>