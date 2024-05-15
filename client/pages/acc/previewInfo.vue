<template>
    <Form>
        <p class="header"> Личный кабинет </p>
        <div class="acc_form">
            <AccPreviewInfo :userInfo="previewInfo" />
            <hr>
            <AccTournamentResults :tournamentResults="tournamentResults" />
            <hr>
            <BackButton />
        </div>
    </Form>
</template>

<script>
import AccPreviewInfo from '../../modules/acc-previewInfo-page/AccPreviewInfo.vue';
import AccTournamentResults from '../../modules/acc-previewInfo-page/AccTournamentResults/AccTournamentResults.vue'

export default {
    layout: "forms",

    head() {
        return {
            title: 'Личный кабинет — Квантландия'
        }
    },

    components: {
        AccPreviewInfo,
        AccTournamentResults,
    },

    data() {
        return {
            previewInfo: {},
            tournamentResults: [],
        }
    },

    async fetch() {
        const tournamentResultsData = await this.$axios.$get('/api/tournament_results')
        this.previewInfo = this.$auth.user
        console.log(this.previewInfo)
        this.tournamentResults = tournamentResultsData
    },
}
</script>

<style>
.acc_form{
    display: inline-flex;
    flex-direction: column;
    gap: 21px;
}

hr {
    width: 100%;
    border-top: 1px solid black;
}
</style>