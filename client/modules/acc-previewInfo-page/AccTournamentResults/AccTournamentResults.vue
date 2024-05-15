<template>
    <div class="tournament_results">
        <p class="header"> Ваши результаты </p>
        <AccTournamentResult v-for="tournamentResult in tournamentResults"  :key="tournamentResult.title"
            :title="tournamentResult.title" :score="tournamentResult.score"/>
    </div>
</template>

<script>
import AccTournamentResult from './components/AccTournamentResult.vue'

export default {
    props: ['tournamentResults'],
    components: {AccTournamentResult},
}
</script>

<style>
.header {
    display: inline-flex;
    justify-content: center;
    gap: 20px;
    font-weight: 700;
    font-size: 16px;
    text-transform: uppercase;
}

.tournament_results {
    display: inline-flex;
    flex-direction: column;
    gap: 21px;
}
</style>