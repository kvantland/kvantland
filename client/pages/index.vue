<template>
    <div class="content_wrapper">
        <div class="tournament">
            <div class="curr_tournament">
                <img class="map" loading="lazy" src="/map_img/land.png" />
                <div class="text_container">
                    <div>
                        <p class="header">Турнир</p>
                        <p class="text">Твоя возможность проявить себя!</p>
                    </div>
                    <p class="text">Тебя ждут задачи из самых разных областей математики:  
                        Головоломки, Логика, Комбинаторика, Арифметика, Геометрия</p>
                    <a href={/start}>
                <div class="start_button"> Открыть турнир </div>
                    </a>
                </div>
            </div>
            <TournamentHistory :tournamentHistory="tournamentHistory"/>
        </div>
        <div class="info_container">
            <div class="page_header">О турнире</div>
                <div class="content">
                    <CommonInfoCard :cardImage="infoCard.image" :cardDescription="infoCard.desc" 
                                v-for="(infoCard, key) in infoCards" :key="key" />
                </div>
        </div>
        <div class="examples_container">
            <div class="page_header"> Примеры задач </div>
            <div class="content">
                <ProblemExample v-for="(problem, num) in problemExamples" 
                v-if="num == currentExampleProblemNum" :problemInfo="problem" 
                :key="problem.title" :num="num" />
            </div>
            <ProblemExampleNav :pageAmount="problemAmount" 
            :selectedNum="currentExampleProblemNum" />
        </div>
        <div class="team_container">
            <p class="page_header"> Примеры задач </p>
            <div class="content">
                <TeamInfoCard v-for="card in teamInfoCards" :cardInfo="card" :key="card.id"/>
            </div>
        </div>
        <div class="contacts_area">
            <p class="page_header"> Будем на связи </p>
            <p class="text"> В наших социальных сетях мы регулярно публикуем 
                            интересные новости о проекте, анонсы ближайших событий и 
                            нестандартные задачки для всех!  </br></br>  
                            Присоединяйтесь и будете всегда в курсе событий! </p>
            <div class="button_area">
                <ContactButton v-for="contact in contacts" :contactInfo="contact" :key="contact.id"/>
            </div>
                <p> Адрес техподдержки: 
                    <a  :href="supportEmail.link" target="_blank"> {{ supportEmail.title }} </a>
                </p>
        </div>
    </div>
</template>


<script>
    export default {
        head() {
            return {
                title: 'Квантландия'
            };
        },

        async asyncData({$axios}) {
            const tournamentHistoryData = await $axios.$get('/tournament_history')
            const infoCardsData = await $axios.$get('/info_cards')
            const probleExamplesData = await $axios.$get('/problem_examples')
            const teamInfoCardsData = await $axios.$get('/team_cards')
            const contactsData = await $axios.$get('/contacts')
            return {
                tournamentHistory: tournamentHistoryData,
                infoCards: infoCardsData,
                problemExamples: probleExamplesData,
                teamInfoCards: teamInfoCardsData,
                contacts: contactsData,
            };
        },

        data() {
            return {
                currentExampleProblemNum: 0
            };
        },

        computed: {
            problemAmount() {
                return this.problemExamples.length;
            },
            supportEmail() {
                let supportEmailLink = this.contacts.filter(
                    (contact) => contact.id == 'email')[0].source_link
                let supportEmail = supportEmailLink.split(':')[1]

                return {'title': supportEmail, 'link': supportEmailLink}
            },
        },
    };
</script>

<style>
@import "../assets/css/start_page.css";
</style>
