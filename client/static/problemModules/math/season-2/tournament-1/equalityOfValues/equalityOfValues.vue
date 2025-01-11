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
			<img :src="`/problem_assets/equalityOfValues/${srcImg}`" alt="board" />
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
			srcImg: "board.png",
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
		// TODO в дальнейшем, если нужно, можно использовать autoscroll
		autoscroll() {
			const targetX = window.event.clientX
			const targetY = window.event.clientY
			const xDiff = 100
			const yDiff = 100
			let [scrollX, scrollY] = [0, 0]
			if (targetX + xDiff > window.innerWidth) {
				scrollX = targetX + xDiff - window.innerWidth
			}
			else if (targetX - xDiff < 0) {
				scrollX = targetX - xDiff
			}
			if (targetY + yDiff > window.innerHeight) {
				scrollY = targetY + yDiff - window.innerHeight
			}
			else if (targetY - yDiff < 0) {
				scrollY = targetY - yDiff
			}
			scrollBy(scrollX, scrollY)
		},
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
			this.$emit('updateAnswer', { signs: this.signsForAnswer() })
		},
		signsForAnswer() {
			const updatenForAnswerSigns = [];
			for (const sign of this.signs) {
				let updatedSign;
				switch (sign) {
					case '+':
						updatedSign = "+";
						break;
					case '−':
						updatedSign = "-";
						break;
					case '×':
						updatedSign = "*";
						break;
				}
				updatenForAnswerSigns.push(updatedSign)
			}
			return updatenForAnswerSigns;
		}
	},
}


</script>
