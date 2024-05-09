<template>
    <div>
        <StartHeader />
        <div class="content_wrapper">
            <TournamentInfo />
            <CommonInfo />
            <ProblemExamples @showDialog="displayDialog" />
            <TeamInfo />
            <ContactsArea />
            <Dialog v-if="activeDialog" :dialogType="dialogType" 
                :dialogData="dialogData" @closeDialog="hideDialog" 
                @changeDialog="displayDialog" />
        </div>
    </div>
</template>


<script>
import TournamentInfo from '../modules/index-page/TournamentInfo/TournamentInfo.vue'
import CommonInfo from '../modules/index-page/CommonInfo/CommonInfo.vue';
import ContactsArea from '../modules/index-page/ContactsArea/ContactsArea.vue';
import ProblemExamples from '../modules/index-page/ProblemExamples/ProblemExamples.vue';
import TeamInfo from '../modules/index-page/TeamInfo/TeamInfo.vue';
import Dialog from '../UI/Dialog.vue'
import StartHeader from '../modules/all-pages/Headers/StartHeader.vue'

    export default {
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
            Dialog,
            StartHeader,
        },

        data() {
            return {
                activeDialog: false,
                dialogType: null,
                dialogData: null,
            };
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

<style>
@import "../assets/css/start_page.css";
</style>
