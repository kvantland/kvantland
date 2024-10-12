<template>
    <div class="content_box">
        <img class="icon" loading="lazy" :src="`/icons/${cardImage}`" />
        <p v-html="cardDescription"></p>
	</div>
</template>

<script>
export default {
    props: ['cardImage', 'cardDescription']
}
</script>

<style scoped>
.content_box {
    height: 432px;
    align-self: stretch;
	padding: 40px; 
	background: white; 
	box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.25); 
	border-radius: 20px; 
	overflow: hidden; 
	border: 3px #1E8B93 solid; 
	flex-direction: column; 
	align-items: center; 
	gap: 60px; 
	display: inline-flex;
    box-sizing: border-box;
    font-size: max(15px, min(20px, 1.5vw));
    font-weight: 400;
}

.content_box .icon {
	max-width: 100px; 
	max-height: 100px;
	width: 100%;
	margin: 0 auto 0 auto;
	align-self: none;
}

>>> .bold_text {
	font-weight: 600;
}
@media(max-width: 800px) {
	.content_box {
		justify-self: stretch;
		min-width: 195px;
		width: 195px;
		height: auto;
		overflow: visible;
		align-self: none;
		font-size: 12px;
		padding: 16px;
		gap: 16px;
		margin-bottom: 30px;
	}
	.content_box .icon {
		width: 40%;
	}
}
</style>