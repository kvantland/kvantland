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
    middleware: "auth",

    head() {
        return {
            title: 'Личный кабинет — Квантландия'
        }
    },

    components: {
        AccPreviewInfo,
        AccTournamentResults,
    },

    async asyncData({$axios, $auth}) {
        const tournamentResultsData = await $axios.$get('/api/tournament_results')
        await $auth.fetchUser()
        const previewInfoData = $auth.user
        return {previewInfo: previewInfoData, tournamentResults: tournamentResultsData}
    },
}
</script>

<style scoped>
.acc_form{
    display: inline-flex;
    flex-direction: column;
    gap: 21px;
}

hr {
    width: 100%;
    border-top: 1px solid black;
}

.header {
    display: inline-flex;
    justify-content: center;
    gap: 20px;
    font-weight: 700;
    font-size: 16px;
    text-transform: uppercase;
}
</style>