<template>
	<g class="drag-container drag-container_usual">
		<rect class="drag-container__wrapper" :width="width" :height="height" x="0" y="0"/>
		<g class="drag-items" :transform="`translate(${padding[0]} ${padding[1]})`">
			<g 
				v-for="_, itemNum in itemsAmount" :key="`drag-item_num-${itemNum}`"
				:transform="`translate(${itemNum * (gap + itemSide)} 0)`"
				class="drag-items__item">
				<image class="drag-item__image" :href="`/problem-assets/${itemImage}`" x="0" y="0" :width="itemSide" :height="itemSide"/>
				<text class="drag-item__text"> {{ alph[itemNum] }} </text>
			</g>
		</g>
	</g>
</template>

<script>
export default {
	props: {
		width: {
			type: Number,
			default: 0,
		},
		itemsAmount: {
			type: Number,
			default: 0,
		},
		itemImage: {
			type: String,
			default: undefined
		}
	},
	data()  {
		return {
			inRow: 5,
			alph: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
		}
	},
	computed: {
		padding() {
			const leftPadding = this.width * 0.05
			const topPadding = this.width * 0.05
			return [leftPadding, topPadding];
		},
	 	gap() {
			return (this.width - this.padding[0] * 2) / Math.min(this.itemsAmount, this.inRow) * 0.1;
		},
		itemSide() {
			return (this.width - this.padding[0] * 2) / Math.min(this.inRow, this.itemsAmount) - this.gap
		},
		rowsAmount() {
			return Math.floor(this.itemsAmount / this.inRow)
		},
		height() {
			return (this.itemSide + this.gap) * this.itemsAmount - this.gap + this.padding[1] * 2
		}
	}
}
</script>