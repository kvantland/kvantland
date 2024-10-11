<template>
    <div class="content_wrapper">
        <TournamentInfo :tournament-history="tournamentHistoryData"/>
        <CommonInfo :info-cards="infoCardsData"/>
        <ProblemExamples :problem-examples="problemExamplesData" @showDialog="displayDialog" />
        <TeamInfo :team-info-cards="teamInfoCards" />
        <ContactsArea :contacts="contactsData" />
        <ProblemExampleDialog
v-if="activeDialog" :dialog-type="dialogType" 
            :dialog-data="dialogData" @closeDialog="hideDialog" 
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

        components: {
            CommonInfo,
            ContactsArea,
            ProblemExamples,
            TeamInfo,
            TournamentInfo,
        },
        layout: 'start-page',

        async asyncData({$axios}) {
            const tournamentHistoryData = await $axios.$get('/api/tournament_history')
            const problemExamplesData = await $axios.$get('/api/problem_examples')
            const teamInfoCards = await $axios.$get('/api/team_cards')
            const contactsData = await $axios.$get('/api/contacts')
            const infoCardsData = await $axios.$get('/api/info_cards')
            return {
                tournamentHistoryData,
                problemExamplesData,
                teamInfoCards,
                contactsData,
                infoCardsData,
            }
        },

        data() {
            return {
                activeDialog: false,
                dialogType: null,
                dialogData: null,
            };
        },
        head() {
            return {
				script: [
					{
						body: true,
						defer: true,
						innerHTML: "Promise.resolve().then(()=>{  setInterval(() => {    MathJax.typesetPromise();  }, 1000);})",
					}
				],
                title: 'Квантландия'
            };
        },

        async mounted() {
			let userInfo
            switch(this.$route.query.request) {
                case 'registration':
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
					break;
                case 'update_acc':
                    console.log('update acc attempt!')
                    try {
                        await this.$axios.$post('/api/email_update', {email_confirm_token: this.$route.query.email_confirm_token, request_type: 'updateInfo'})
                        .then((resp) => {
                            console.log(resp)
                            this.$auth.fetchUser()
                        })
                    }
                    catch(e) {console.log('Acc update error:', e)}
					break;
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
