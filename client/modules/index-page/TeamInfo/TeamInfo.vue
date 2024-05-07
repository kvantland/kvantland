<template>
    <div class="team_container">
        <p class="page_header"> Примеры задач </p>
        <div class="content">
            <TeamInfoCard v-for="card in teamInfoCards" :cardInfo="card" :key="card.id"/>
        </div>
    </div>
</template>

<script>
import TeamInfoCard from "./components/TeamInfoCard.vue"

export default {
    components: {
        TeamInfoCard,
    },

    data(){
        return {
            teamInfoCards: {},
        }
    },

    async fetch() {
        const teamInfoCards = await this.$axios.$get('/team_cards')
        this.teamInfoCards = teamInfoCards
    },
}
</script>