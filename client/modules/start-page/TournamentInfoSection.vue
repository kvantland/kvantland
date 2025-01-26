<template>
	<section id="TournamentInfoSection" class="tournament-info-section">
		<p role="header" class="tournament-info-section__title"> Турниры </p>
		<p class="tournament-info-section__descr"> На нашей платформе ты можешь поучаствовать 
			в турнирах сразу по нескольким предметам: </p>
		<div class="info">
			<div></div>
			<div class="tournament-filters">
				<button
					v-for="filter, filterNum in filters.tournamentType.options"
					:key="`tournament-filter_type-${filter.value}`"
					:class="`filter-button filter-button_${filters.tournamentType.choosed === filterNum ? 'choosed': 'not-choosed'}`"
					@click="toggleFilter('tournamentType', filterNum)">
					{{ filter.title }}
				</button>
			</div>
			<div class="classes-filters">
				<button 
					v-for="filter, filterNum in filters.classes.options"
					:key="`tournament-filter_type-${filter.value}`"
					:class="`filter-button filter-button_${filters.classes.choosed === filterNum ? 'choosed': 'not-choosed'}`"
					@click="toggleFilter('classes', filterNum)">
					{{ filter.title }}
				</button>
			</div>
			<div class="search-results">
				<div 
					v-for="searchResult, searchResultNum in searchResults" 
					:key="`search-res_${searchResultNum}`"
					class="search-result">
					<div class="search-result__title" :style="`color: ${getTitleColor(searchResult)};`">
						<p class="search-result__title_text"> 
							{{ getTitle(searchResult) }} </p>
						<a class="search-result__title_link" :href="`${searchResult.link}`" target="_blank">
							<img class="search-result__title_link" src="/icons/link_arrow.svg" />
						</a>
					</div>
					<p class="search-result__date"> 
						Даты проведения: 
						<span class="bold-text"> {{ searchResult.dates }} </span>
					</p>
					<div class="search-result__tags">
						<div 
							v-for="tag, tagNum in searchResult?.tags"
							:key="`tag_${searchResult.id}_${tagNum}`"
							class="search-result__single-tag">
							{{ tag }}
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>
</template>

<script>
import tournamensListJson from "./tournaments.json"
export default {
	data() {
		return {
			filters: {
				classes: {
					choosed: null,
					options: [
						// {
						// 	title: "1-3 класс",
						// 	value: "1-3"
						// },
						{
							title: "4-6 класс",
							value: "4-6"
						},
						{
							title: "7-9 класс",
							value: "7-9"
						}
					]
				},
				tournamentType: {
					choosed: null,
					options: [
						{
							title: "Математика",
							value: "math"
						},
						{
							title: "Информатика",
							value: "IT"
						}
					]
				}
			},
			tournamentTypeDict: {
				math: {
					color: "rgba(182, 44, 90, 1)",
					title: "Математика"
				},
				IT: {
					color: "rgba(57, 70, 185, 1)",
					title: "Информатика"
				}
			},
			tournamensList: tournamensListJson.tournamentList
		}
	},
	computed: {
		searchResults() {
			return this.updateResults();
		}
	},
	methods: {
		setFilter(filerType, value) {
			this.$set(this.filters, filerType, value);
		},
		updateResults() {
			const classes = this.filters.classes
			const tournaments = this.filters.tournamentType

			return this.tournamensList.filter(tournament =>
				(tournament.classes === classes.options[classes.choosed]?.value || tournament.classes === "all" || classes.choosed === null)
					&& 
				(tournament.tournamentType === tournaments.options[tournaments.choosed]?.value || tournaments.choosed === null)
			)
		},
		getTitle(searchResult) {
			return this.tournamentTypeDict[searchResult.tournamentType].title;
		},
		getTitleColor(searchResult) {
			return this.tournamentTypeDict[searchResult.tournamentType].color;
		},
		toggleFilter(filterType, filterNum) {
			if (this.filters[filterType].choosed === filterNum) {
				this.$set(this.filters[filterType], "choosed", null);
				return;
			}
			this.$set(this.filters[filterType], "choosed", filterNum);
		}
	}
}
</script>

<style lang="scss" scoped>
.info {
	width: 100%;
	display: inline-grid;
	column-gap: 40px;
	row-gap: 30px;
	grid-template-columns: 1fr 5fr;
}

.filter-button {
	width: 100%;
	font-weight: 500;
	font-size: 24px;
	color: rgba(30, 139, 147, 1);
	border: 2px rgba(30, 139, 147, 1) solid;
	border-radius: 10px;
	text-align: center;
	padding: 10px 0px;
	background-color: white;
	cursor: pointer;
	transition: 0.3s;

	&_choosed {
		background-color: rgba(30, 139, 147, 1);
		color: white;
	}
}

.tournament-filters {
	justify-content: stretch;
	display: inline-flex;
	flex-direction: row;
	gap: 30px;
}

.classes-filters {
	display: inline-flex;
	flex-direction: column;
	justify-content: center;
	height: 354px;
	gap: 50px;
}

.tournament-info-section {
	width: 100%;
	display: inline-flex;
	flex-direction: column;
	gap: 30px;

	&__title {
		font-weight: 600;
		font-size: 40px;
		color: rgba(30, 139, 147, 1);
		font-family: Montserrat Alternates;
	}
	&__descr {
		font-size: 24px;
	}
}

.search-results {
	display: inline-grid;
	grid-template-columns: 1fr 1fr;
	column-gap: 30px;
	row-gap: 40px;
	height: 354px;
	overflow-y: scroll;
	scrollbar-gutter: stable;
	scrollbar-width: thin;
  scrollbar-color: rgba(30, 139, 147, 1) transparent;
	// box-sizing: border-box;
	padding-right: 20px;
	margin-right: -24px;
}
.search-results::-webkit-scrollbar {
	width: 4px;
}
.search-results::-webkit-scrollbar-track {
	background: transparent;
}
.search-results::-webkit-scrollbar-thumb {
	background-color: rgba(30, 139, 147, 1);
  border-radius: 20px;
	border: none;
}

.search-result {
	align-self: start;
	display: inline-flex;
	flex-direction: column;
	background-color: rgba(236, 249, 250, 1);
	border: 1px rgba(236, 249, 250, 1) solid;
	padding: 20px;
	border-radius: 20px;
	box-sizing: border-box;
	
	&__title {
		display: inline-flex;
		justify-content: space-between;
		font-weight: 700;
		font-size: 24px;
		margin-bottom: 12px;
	}
	&__title_link {
		cursor: pointer;
		width: 10px;
		height: 10px;
		color: black;
		filter: brightness(0);
	}
	&__date {
		font-size: 20px;
		margin-bottom: 24px;
	}
	&__tags {
		display: inline-flex;
		flex-direction: row;
		gap: 20px;
		height: 28px;
	}
	&__single-tag {
		height: 100%;
		display: inline-flex;
		align-items: center;
		text-align: center;
		border: 1px black solid;
		padding: 0px 10px;
		font-size: 16px;
		border-radius: 20px;
	}
}

.filter-button:hover {
	filter: brightness(0.8);
}
</style>