<template>
    <a class="contact_button" :href="contactInfo.source_link" target="_blank">
        <img class="contact_icon" loading="lazy" :src="`/icons/${contactInfo.image}`" />
    </a>
</template>

<script>
export default {
    props: ["contactInfo"]
}
</script>

<style scoped>
.contact_button {
	flex: 1 1 0; 
	align-self: stretch; 
	padding: 10px; 
	background: #1E8B93; 
	box-shadow: 6px 6px 10px rgba(0, 0, 0, 0.25); 
	border-radius: 10px; 
	justify-content: center; 
	align-items: center; 
	gap: 10px; 
	display: flex;
}

.contact_icon {
	width: 31.25px; 
	height: 25px; 
}
@media(max-width: 800px) {
	.contact_button {
		border-radius: 4px;
	}
}
</style>