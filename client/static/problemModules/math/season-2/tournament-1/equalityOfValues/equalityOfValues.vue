<template>
	<div class="board">
		<div class="number-container">
			<div class="inner-container">
				<!-- Левая часть -->
				<NumberSection side='left' :data="dataInit" :signs="signs" :current-drop-index="currentDropIndex"
					@drop="handleDrop" @dragover="handleDragOver" @dragstart="handleDragStart"
					@dragend="handleDragEnd" />
				<span class="empty-space">=</span>
				<!-- Правая часть -->
				<NumberSection side='right' :data="dataInit" :signs="signs" :current-drop-index="currentDropIndex"
					@drop="handleDrop" @dragover="handleDragOver" @dragstart="handleDragStart"
					@dragend="handleDragEnd" />
			</div>
			<img :src='srcImg' alt="board" />
		</div>

		<ul class="group-signs">
			<li v-for="(sign, index) in availableSigns" :key="'available-sign-' + index" class="item-sign">
				<span draggable="true" @dragstart="handleDragStart(-1, sign)" @dragend="handleDragEnd"> {{ sign
					}}</span>
			</li>
		</ul>
	</div>
</template>


<script>

import NumberSection from '~/static/problemModules/components/NumberWithSign.vue';

export default {
	components: {
		NumberSection
	},

	model: {
		prop: 'answer',
		event: 'updateAnswer'
	},

	props: {
		problemParams: {
			type: Object,
			default: () => { }
		}
	},


	data() {
		return {
			srcImg: "https://s3-alpha-sig.figma.com/img/7ca0/670c/f4b4280b1a9e9774c40a8ca87a4e0607?Expires=1735516800&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4&Signature=AeHfPHoXC3qDQ3h~tYrR1kGRAqVdPkm7dXrq9wJcmWMzKKWJddADc-jZJCUd~5bsnigqvVdPfFxVafXSAml3h6lnx1Xj8ZGkLKCDzggJlOk0M8rj8d~R2KOTCxcXRNM52CGbzbmPV1eind4gHL1noTJhnuRVKu02ON658ZVXA~UXvgb9C63ck3urJJn~WPbAF0OprlDUFmC7yf9w-B82tnr~OrkB5I7Pqobezy2v2AI1cdVIhPrE-6Tgu8r0UH1aLK8NYFXjUoW0yw91TEAu0OLgr1ry5GSfvyINlYAvikdk2voxkxutl3LUTBwjkHL7WD6ncnU3votWDev4fsW2SA__",
			availableSigns: ['+', '−', '×'],
			signs: Array(6).fill(null), // Инициализация для всех чисел 
			draggedSign: null,
			draggedIndex: null,
			currentDropIndex: null,

		};
	},
	computed: {
		dataInit() {
			return this.problemParams.variant
		}
	},

	methods: {
		handleDragStart(index, sign = null) {
			this.draggedIndex = index;
			this.draggedSign = sign || this.signs[index];

			// Установка стиля для перетаскиваемого элемента
			const draggedElement = event.target; // Получаем элемент, который перетаскивается
			draggedElement.style.opacity = 0.5; // Уменьшаем непрозрачность
		},
		handleDragEnd() {
			this.draggedIndex = null;
			this.draggedSign = null;
			this.currentDropIndex = null;

			const draggedElement = event.target; // Получаем элемент, который был перетаскиваемым
			draggedElement.style.opacity = ''; // Сбрасываем стиль


		},
		handleDragOver(index) {

			if (typeof index === 'number') {
				this.currentDropIndex = index; // Установка текущей зоны
			}

		},
		handleDrop(index) {
			if (this.draggedSign !== null) {
				if (this.draggedIndex === -1) {
					// Перетаскивание из доступных знаков
					this.signs[index] = this.draggedSign; // Установка нового знака
				} else {
					// Удаление предыдущего знака
					this.signs[this.draggedIndex] = null; // Удаление старого знака
					// Установка нового знака
					this.signs[index] = this.draggedSign;
				}

			}
			this.currentDropIndex = null; // Сброс текущей зоны после завершения перетаскивания
			this.$emit('updateAnswer', { data: this.dataInit, signs: this.signs })
		}
	},

}


</script>
