<template>
    <div class="team_container" id="teamInfo">
        <p class="page_header"> Авторы и команда </p>
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