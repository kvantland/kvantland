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
            return {
                tournamentHistory: tournamentHistoryData,
                infoCards: infoCardsData,
                problemExamples: probleExamplesData,
                teamInfoCards: teamInfoCardsData,
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
            }
        },
    };
</script>

<style>
@import "../assets/css/start_page.css";
</style>
