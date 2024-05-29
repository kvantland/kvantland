<template>
    <div class="content_box" v-if="cardInfo.type == 'personal'">
        <img class="photo" loading="lazy" :src="`/team_photos/${cardInfo.image}`" />
        <p class="name"> {{ cardInfo.name }} </p>
        <p v-html="cardInfo.desc"> </p>
    </div>
    <div class="content_box" v-else-if="cardInfo.type == 'list'">
        <div class="list">
            <template v-for="team_desc in cardInfo.desc">
                <div class="par">
                    <p class="header"> {{ team_desc.title }} </p>
                    <p v-for="member_name in team_desc.team_members"> {{ member_name }} </p>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    props: ["cardInfo"]
}
</script>

<style scoped>
.team_container .content_box {
	display: inline-flex;
	flex-direction: column;
    align-self: stretch;
	gap: 20px;
	padding: 30px;
	height: 516px;
	align-items: center;
	box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.25); 
	border-radius: 20px;
	border: 3px #1E8B93 solid;
	font-size: max(15px, min(20px, 1.5vw));
	font-family: Montserrat;
	font-weight: 400;
	overflow: hidden;
}

.team_container .content_box .name {
	font-weight: 600;
	align-self: center;
}

.team_container .content_box img {
	margin: 0 auto;
	max-height: 200px;
	max-width: 187px;
	width: 100%;
}

.team_container .content_box .list {
	display: inline-flex;
	align-self: center;	
	flex-direction: column;
	gap: 20px;
	height: 100%;
	justify-content: center;
	font-size:  max(15px, min(20px, 1.5vw));
	font-weight: 400;
}

.team_container .content_box .list .par {
	display: inline-flex;
	flex-direction: column;
	gap: 10px;
}

.team_container .content_box .list .par .header {
	color: #1E8B93;
	font-weight: 600;
}
</style>