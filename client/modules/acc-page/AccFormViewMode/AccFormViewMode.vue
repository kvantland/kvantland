<template>
    <div class="acc_form">
        <AccPreviewInfo :userInfo="previewInfo" @changeToEditMode="$emit('changeToEditMode')"/>
        <hr>
        <AccTournamentResults :tournamentResults="tournamentResults" />
        <hr>
        <button class="back_button" @click="back"> Назад </button>
    </div>
</template>

<script>
import AccPreviewInfo from './components/AccPreviewInfo.vue';
import AccTournamentResults from './components/AccTournamentResults/AccTournamentResults.vue'

export default {
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

    methods: {
        back() {
            history.back()
        }
    }
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

.back_button {
	align-self: stretch;
	display: flex;
	justify-content: center;
	align-items: center;
	height: 50px;
	color: #1E8B93;
	font-size: 14px;
	font-weight: 600;
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25); 
	border-radius: 6px;
	border: 1px #1E8B93 solid;
	background-color: white;
    font-family: Montserrat;
    cursor: pointer;
}
</style>