<template>
    <div class="tournament section">
        <div class="curr_tournament">
            <img class="map" loading="lazy" src="/map_img/land.png" />
            <div class="text_container">
                <div>
                    <p class="header">Турнир</p>
                    <p class="text">Возможность проявить себя!</p>
                </div>
                <p class="text">Вас ждёт увлекательное путешествие по городам Квантландии, 
					где встретятся интерактивные задачи из следующих разделов: Игры, Алгоритмы, 
					Программирование, Блоки.</p>
                <NuxtLink to="/rules">
                    <div class="start_button"> Открыть турнир </div>
                </NuxtLink>
            </div>
        </div>
        <TournamentHistory :tournament-history="tournamentHistory" />
    </div>
</template>

<script>
import TournamentHistory from "./components/TournamentHistory.vue"

export default {

    components: {
        TournamentHistory,
    },
    props: ['tournamentHistory']
}
</script>

<style scoped>
.tournament {
	padding: 60px;
	background: #1E8B93;
	border-radius: 20px;
	justify-content: space-between;
	gap: 60px;
	box-sizing: border-box;
	display: inline-flex;
	flex-direction: column;
}

.tournament .curr_tournament {
	gap: 60px;
	display: inline-flex;
	align-items: center;
	justify-content: space-between;
}


.tournament img {
	overflow: hidden;
	width: 70%;
	max-width: 733px;
	box-shadow: 12px 12px 14px rgba(0, 0, 0, 0.25);
	border-radius: 20px;
	border: 2px white solid;
}

.tournament .text_container {
	max-width: 40%;
	display: inline-flex;
	gap: 10px;
	flex-direction: column; 
	justify-content: space-between; 
	align-items: stretch; 
	display: inline-flex;
    align-self: stretch;
}

.tournament .text {
	color: white;
	font-size: max(15px, min(30px, 1.8vw));
	font-weight: 400; 
}

.tournament .header {
	color: white;
	font-family: Montserrat Alternates;
	font-size: 40px;
	font-weight: 500; 
}

.start_button {
    flex: 1 1 0;
	font-weight: 600;
	font-size:24px;
	text-align: center;
	padding: 10px 0;
	background: linear-gradient(180deg, #FCFCFC 16%, white 20%, #FFFFFF 55%, #EFEFEF 80%); 
	box-shadow: 7px 7px 6.699999809265137px #1A5866; 
	border-radius: 10px;
	align-self: stretch;
	white-space: nowrap;
}

@media(max-width: 850px) {
	.tournament .curr_tournament {
		flex-direction: column;
		gap: 16px;
	}	
	.tournament img {
		width: 100%;
	}
	.tournament .text_container {
		max-width: 100%;
	}
}

@media(max-width: 650px) {
	.tournament.section {
		padding: 4vw 4vw;
		gap: 20px;
	}
	.start_button {
		font-size: min(16px, 6vw);
	}
	.tournament .text {
		font-size: 14px;
	}
	.tournament .header {
		font-size: 20px;
	}
}
</style>