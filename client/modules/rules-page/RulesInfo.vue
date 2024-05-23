<template>
<div class="content_box">
    <p class="header_page">Правила турнира</p>
    <div class="rules_content" id="rulesInfo">
        <div class="span_wrapper" v-for="item in rulesInfo">
            <p v-if="item.normal" class="span_text" v-html="item.normal"></p>
            <br v-if="item.bold" />
            <p v-if="item.bold" class="bold_text" v-html="item.bold"></p>
        </div>
    </div>
    <StartTournamentContainer/>
</div>
</template>

<script>
import StartTournamentContainer from "./components/StartTournamentContainer.vue"
export default {
   components: {
        StartTournamentContainer,
    },

    data() {
        return {
            contacts: {},
            rulesInfo:{},
        }
    },

    computed: {
        supportEmail() {
            try {
                let email = this.contacts.filter((contact) => contact.id == 'email')[0].source_link
                return { link: email, title: email.split(':')[1]}
            }
            catch {
                return { link: '', title: '' }
            }
        },
    },

    async fetch() {
        const contactsData = await this.$axios.$get('/api/contacts')
        this.contacts = contactsData
        const rulesInfoData = await this.$axios.$get('/api/rules_info')
        this.rulesInfo = rulesInfoData
    }
}
</script>
<style scoped>
.content_box {
    align-self: stretch;
    padding: 40px;
    border-radius: 40px;
    border: 3px #1E8B93 solid;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 40px;
    color: black;
    font-size: 20px;
    font-family: Montserrat;
    text-align: justify;
    word-wrap: break-word
}

.header_page {
    height: 49px;
    color: #1E8B93;
    font-size: 40px;
    font-family: Montserrat Alternates;
    font-weight: 600
}

.rules_content {
    align-self: stretch;
    flex-direction: column;
    gap: 40px;
    display: flex
}

.span_text {
    font-weight: 400;
}

.bold_text {
    font-weight: 600;
}

.mail_link {
    text-decoration: underline;
}
</style>