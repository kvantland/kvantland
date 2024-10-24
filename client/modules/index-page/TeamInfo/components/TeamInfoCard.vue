<template>
	<div v-if="cardInfo.type == 'personal'" class="content_box">
		<img class="photo" loading="lazy" :src="`/team_photos/${cardInfo.image}`" />
		<p class="name"> {{ cardInfo.name }} </p>
		<p v-html="cardInfo.desc"> </p>
	</div>
	<div v-else-if="cardInfo.type == 'list'" class="content_box">
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

@media(max-width: 900px) {
	.team_container {
		gap: 3vw;
	}
	.team_container .content_box{
		justify-self: stretch;
		min-width: 200px;
		width: 200px;
		height: auto;
		overflow: visible;
		align-self: none;
		font-size: 12px;
		padding: 16px;
		margin-bottom: 30px;
	}
	.team_container .content_box img {
		width: 130px;
	}
	.team_container .content_box .list {
		font-size: 12px;
	}
	.team_container .content_box .list .par .header {
		font-size: 13px;
	}
}
</style>