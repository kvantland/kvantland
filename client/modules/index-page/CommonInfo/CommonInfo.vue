<template>
    <div class="info_container section" id="commonInfo">
        <p class="page_header">О турнире</p>
        <div class="content">
                <CommonInfoCard :cardImage="infoCard.image" :cardDescription="infoCard.desc" 
                            v-for="(infoCard, key) in infoCards" :key="key" />
        </div>
    </div>
</template>

<script>
import CommonInfoCard from "./components/CommonInfoCard.vue"

export default {
    props: ['infoCards'],

    components: {
        CommonInfoCard,
    },
}
</script>

<style scoped>
.info_container {
	height: 983px; 
	flex-direction: column; 
	justify-content: flex-start; 
	align-items: flex-start; 
	gap: 40px; 
	display: flex;
}

.page_header {
	color: #1E8B93;
	font-size: 40px;
	font-family: Montserrat Alternates;
	font-weight: 600;
}

.info_container .content {
	display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    column-gap: 40px;
    row-gap: 30px;
}
</style>