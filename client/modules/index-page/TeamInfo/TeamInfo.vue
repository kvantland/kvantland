<template>
    <div class="team_container" id="teamInfo">
        <p class="page_header"> Авторы и команда </p>
        <div class="content">
            <TeamInfoCard v-for="card in teamInfoCards" :cardInfo="card" :key="card.id"/>
        </div>
    </div>
</template>

<script>
import TeamInfoCard from "./components/TeamInfoCard.vue"

export default {
    props: ['teamInfoCards'],

    components: {
        TeamInfoCard,
    },
}
</script>

<style scoped>
.team_container {
	flex-direction: column;
  	justify-content: flex-start;
  	align-items: flex-start;
  	gap: 40px;
  	display: flex;
}

.team_container .page_header {
	color: #1E8B93;
	font-size: 40px;
	font-family: Montserrat Alternates;
	font-weight: 600;
}

.team_container .content {
	display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-column-gap: 25px;
    grid-row-gap: 30px;
}
</style>