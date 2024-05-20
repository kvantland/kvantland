<template>
<div class="content_box">
    <p class="header_page">Правила турнира</p>
    <div class="rules_content" id="rulesInfo">
        <div class="span_wrapper" v-for="item in rulesInfo">
            <p class="span_text" v-html="item.normal"></p><br/>
            <p v-html="item.bold"></p>
        </div>
        <div class="span_wrapper span_text">Выберите время в любой день до окончания турнира, чтобы вас ничего не отвлекало. Итоги соревнования подводятся по числу квантиков, которое у вас на счету к концу игры. Это число всегда отображается в вверху экрана по центру. Удачи!</div>
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
<style>
.content_box {
    align-self: stretch;
    padding: 40px;
    border-radius: 40px;
    border: 3px #1E8B93 solid;
    flex-direction: column;
    justify-content: center;
    align-items: flex-end;
    gap: 40px;
    display: flex;
    color: black;
    font-size: 20px;
    font-family: Montserrat;
    font-weight: 600;
    word-wrap: break-word
}

.header_page {
    align-self: stretch;
    height: 49px;
    color: #1E8B93;
    font-size: 40px;
    font-family: Montserrat Alternates;
}

.rules_content {
    align-self: stretch;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 40px;
    display: flex
}

.span_wrapper {
    align-self: stretch; text-align: justify
}

.span_text {
    font-weight: 400;
}

.mail_link {
    text-decoration: underline;
}
</style>