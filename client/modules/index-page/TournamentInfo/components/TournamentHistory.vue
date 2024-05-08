<template>
    <div class="history">
        <div class="content">
            <div class="item" v-for="historyItem in tournamentHistory">
                <div class="text_cont">
                    <div class="header"> {{historyItem['event_date']}} </div>
                    <div class="text"> {{historyItem['event_name']}} </div>
                </div>
                <div class="rect"></div>
            </div>
        </div>
        <hr size="2" noshade="" color="white">
    </div>
</template>

<script>
export default {
    data() {
        return {
            tournamentHistory: {}
        }
    },

    async fetch() {
        const tournamentHistoryData = await this.$axios.$get('/tournament_history')
        this.tournamentHistory = tournamentHistoryData
    },
};
</script>
