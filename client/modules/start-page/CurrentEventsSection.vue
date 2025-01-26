<template>
	<section class="news-section">
		<p role="header" class="news-section__header"> События </p>
		<div class="single-new">
			<div class="single-new__title">
				<div class="single-new__title_num-block"> №{{ newNum + 1 }} </div>
				<p class="single-new__title_text">{{ currentNew.title }}</p>
			</div>
			<div class="single-new__body">
				<img class="single-new__image" loading="lazy" :src="`/news_images/${currentNew.image}`" />
				<div class="single-new__description">
					<div class="single-new__description_text">
						<p class="single-new__description_title"> {{ currentNew.descrTitle }} </p>
						<p class="single-new__description_body"> {{ currentNew.descrBody }} </p>
					</div>
					<div class="single-new__buttons">
						<a 
							v-for="buttonInfo, buttonInfoNum in currentNew.buttons" 
							:key="`${currentNew.title}__button_num-${buttonInfoNum}`"
							:href="buttonInfo.link" target="_blank">
							<div class="start-button"> {{ buttonInfo.title }} </div>
						</a>
					</div>
				</div>
			</div>
		</div>
		<!-- Хорошо бы навигацию потом перенести в UI и переименовать -->
		<ProblemExampleNav 
			:page-amount="newsDescription.length" 
			:selected-num="newNum" 
			@changeProblem="updateCurrentProblemNum" /> 
	</section>
</template>

<script>
import ProblemExampleNav from '../index-page/ProblemExamples/components/ProblemExampleNav.vue';
import eventsJson from "./currentEvents.json";
export default {
	components: {
		ProblemExampleNav,
	},
	data() {
		return {
			newNum: 0,
			newsDescription: eventsJson.events
		}
	},
	computed: {
		currentNew() {
			return this.newsDescription[this.newNum];
		}
	},
	methods: {
		updateCurrentProblemNum(num) {
			this.newNum = num
		}
	}
}
</script>

<style lang="scss" scoped>
.news-section {
	display: inline-flex;
	flex-direction: column;
	gap: 20px;
	&__header {
		color: rgba(30, 139, 147, 1);
		font-weight: 600;
		font-size: 40px;
		font-family: Montserrat Alternates;
	}
}
.single-new {
	display: inline-flex;
	flex-direction: column;
	gap: 20px;
	padding: 60px;
	background-color: rgba(30, 139, 147, 1);
	border-radius: 20px;

	&__title {
		display: inline-flex;
		flex-direction: row;
		align-items: center;
		gap: 20px;
		align-self: flex-start;
		font-size: 40px;
		font-weight: 600;
		color: white;
	}
	&__title_num-block {
		background-color: rgba(119, 199, 205, 1);
		border-radius: 10px;
		padding: 10px 30px;

	}

	&__body {
		display: inline-flex;
		flex-direction: row;
		gap: 60px;
	}

	&__image {
			overflow: hidden;
			width: 70%;
			max-width: 733px;
			box-shadow: 12px 12px 14px rgba(0, 0, 0, 0.25);
			border-radius: 20px;
			border: 2px white solid;
	}

	&__description {
		display: inline-flex;
		flex-direction: column;
		justify-content: space-between;
		max-width: 40%;
	}
	&__description_text {
		display: inline-flex;
		flex-direction: column;
		gap: 20px;
		color: white;
	}
	&__description_title {
		font-size: 36px;
	}
	&__description_body {
		font-size: 24px;
	}

	&__buttons {
		display: inline-flex;
		flex-direction: column;
		gap: 18px;
	}
}
.start-button {
		font-weight: 600;
		font-size: 24px;
		text-align: center;
		padding: 10px 0;
		background: linear-gradient(180deg, #FCFCFC 16%, white 20%, #FFFFFF 55%, #EFEFEF 80%); 
		box-shadow: 7px 7px 6.699999809265137px #1A5866; 
		border-radius: 10px;
		align-self: stretch;
		white-space: nowrap;
}


@media(max-width: 850px) {
	.single-new__body {
		flex-direction: column;
		gap: 16px;
	}	
	.single-new__image {
		width: 100%;
	}
	.single-new__description {
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