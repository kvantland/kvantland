<template>
    <div class="content_box">
    <div class="rules_box">
    <div class="header_page">Правила турнира</div>
    <div class="rules_content" id="rulesInfo">
    <div class="rules_wrapper">
    <div class="span_position"><span class="span_text">Игрок путешествует по стране Квантландия, оказываясь в разных городах и областях (Головоломск, Остров Лжецов, Республика Комби, Чиселбург, Геома), и зарабатывает виртуальную валюту «квантик» за решение задач соответствующей темы: Головоломки, Логика, Комбинаторика, Арифметика, Геометрия. <br/><br/></span><span>Цель игры — получить как можно больше квантиков.</span></div>
    </div>
    <div class="rules_wrapper">
    <div class="span_position"><span class="span_text">В начале игры каждому дается 10 квантиков, которые можно тратить на подсказки к задачам. Для того чтобы получить задачу, нужно выбрать одну из монет в соответствующем городе или области (кликнуть на монету). На монете указывается количество квантиков, которое дается за ее правильное решение. <br/><br/></span><span>Есть задачи проще (1 или 2 квантика за решение) и сложнее (3 или 4 квантика за решение).</span></div>
    </div>
    <div class="span_wrapper"><span class="span_text">Можно свободно возвращаться к карте города или страны. Но если вы уже давали ответ на задачу, то задача становится неактивной и пройти ее повторно нельзя. <br/><br/></span><span>Поэтому не торопитесь и внимательно проверяйте, прежде чем отправить ответ. </span></div>
    <div class="span_wrapper"><span class="span_text">Обратите внимание, что некоторые задачи интерактивны. В них требуется произвести действия, которые описаны в условии, чтобы получить нужный результат. <br/><br/></span><span>Читайте условия внимательно! </span></div>
    <div class="span_wrapper"><span class="span_text">Для решения задач вам понадобится компьютер и компьютерная мышь или ноутбук с тачпадом (не планшет), чтобы перетаскивать и выделять объекты. <br/><br/></span><span>Если возникла техническая проблема, то можно написать в техподдержку </span><u><NuxtLink  to="supportEmail.link" target="_blank">{{ supportEmail.title }}</NuxtLink></u><span> с описанием проблемы и скриншотом компьютера.</span></div>
    <div class="span_wrapper span_text">Выберите время в любой день до окончания турнира, чтобы вас ничего не отвлекало. Итоги соревнования подводятся по числу квантиков, которое у вас на счету к концу игры. Это число всегда отображается в вверху экрана по центру. Удачи!</div>
    </div>
    <AgreeContainer/>
    </div>
    </div>
</template>

<script>
import AgreeContainer from "./components/AgreeContainer.vue"
export default {
   components: {
        AgreeContainer,
    },

    data() {
        return {
            contacts: {},
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
    }
}
</script>
<style>
.rules_box {
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

.rules_wrapper {
    align-self: stretch;
    justify-content: center;
    align-items: center;
    gap: 100px;
    display: inline-flex;
}

.span_position {
    flex: 1 1 0;
    text-align: justify;
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