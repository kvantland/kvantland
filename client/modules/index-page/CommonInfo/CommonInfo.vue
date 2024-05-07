<template>
    <div class="info_container">
            <div class="page_header">О турнире</div>
                <div class="content">
                    <CommonInfoCard :cardImage="infoCard.image" :cardDescription="infoCard.desc" 
                                v-for="(infoCard, key) in infoCards" :key="key" />
            </div>
    </div>
</template>

<script>
import CommonInfoCard from "./components/CommonInfoCard.vue"

export default {
    components: {
        CommonInfoCard,
    },

    data() {
        return {
            infoCards: {},
        }
    },

    async fetch() {
        const infoCardsData = await this.$axios.$get('/info_cards')
        this.infoCards = infoCardsData
    }
}
</script>