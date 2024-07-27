<template>
    <div class="content_wrapper">
        <TournamentInfo :tournamentHistory="tournamentHistoryData"/>
        <CommonInfo :infoCards="infoCardsData"/>
        <ProblemExamples :problemExamples="problemExamplesData" @showDialog="displayDialog" />
        <TeamInfo :teamInfoCards="teamInfoCards" />
        <ContactsArea :contacts="contactsData" />
        <ProblemExampleDialog v-if="activeDialog" :dialogType="dialogType" 
            :dialogData="dialogData" @closeDialog="hideDialog" 
            @changeDialog="displayDialog" />
    </div>
</template>


<script>
import TournamentInfo from '../modules/index-page/TournamentInfo/TournamentInfo.vue'
import CommonInfo from '../modules/index-page/CommonInfo/CommonInfo.vue';
import ContactsArea from '../modules/index-page/ContactsArea/ContactsArea.vue';
import ProblemExamples from '../modules/index-page/ProblemExamples/ProblemExamples.vue';
import TeamInfo from '../modules/index-page/TeamInfo/TeamInfo.vue';

    export default {
        layout: 'start-page',
        head() {
            return {
                title: 'Квантландия'
            };
        },

        components: {
            CommonInfo,
            ContactsArea,
            ProblemExamples,
            TeamInfo,
            TournamentInfo,
        },

        data() {
            return {
                activeDialog: false,
                dialogType: null,
                dialogData: null,
            };
        },

        async asyncData({$axios}) {
            const tournamentHistoryData = await $axios.$get('/api/tournament_history')
            const problemExamplesData = await $axios.$get('/api/problem_examples')
            const teamInfoCards = await $axios.$get('/api/team_cards')
            const contactsData = await $axios.$get('/api/contacts')
            const infoCardsData = await $axios.$get('/api/info_cards')
            return {
                tournamentHistoryData: tournamentHistoryData,
                problemExamplesData: problemExamplesData,
                teamInfoCards: teamInfoCards,
                contactsData: contactsData,
                infoCardsData: infoCardsData,
            }
        },

        async mounted() {
            switch(this.$route.query.request) {
                case 'registration':
                    let userInfo
                    try {
                        await this.$axios.$post('/api/registration', {email_confirm_token: this.$route.query.email_confirm_token})
                        .then((resp) => { userInfo = resp })
                    }
                    catch(e) {console.log('Registration error:', e)}
                    try {
                        await this.$auth.loginWith('local', {data: userInfo})
                            .then((resp) => {
                                this.$auth.setUserToken(resp.data.tokens.access_token, resp.data.tokens.refresh_token)
                                this.$auth.setUser(resp.data.user)
                            })
                    }
                    catch(e) {console.log('Login error:', e)}
                case 'update_acc':
                    if (this.$auth.loggedIn) {break}
                    try {
                        await this.$axios.$post('/api/email_update', {email_confirm_token: this.$route.query.email_confirm_token})
                        .then((resp) => {
                            console.log(resp)
                            if (resp.status && resp.tokens) {
                                this.$auth.strategy.token.set(resp.tokens.access_token)
                                this.$auth.strategy.refreshToken.set(resp.tokens.refresh_token)
                                this.$auth.fetchUser()
                            }
                        })
                    }
                    catch(e) {console.log('Acc update error:', e)}
            }
        },

        methods: {
            displayDialog(dialogType, dialogData) {
                this.activeDialog = true
                this.dialogType = dialogType
                this.dialogData = dialogData
            },
            hideDialog() {
                this.activeDialog = false
                this.dialogType = null
                this.dialogData = null
            },
        },
    };
</script>

<style scoped>
.content_wrapper {
	width: 100%;
	padding: 0 max(40px, min(5vw, 80px)) 70px max(40px, min(5vw, 80px));
	margin-top: 130px;
	box-sizing: border-box;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 60px;
	display: inline-flex;
}
</style>
