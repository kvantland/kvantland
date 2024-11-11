<template>
	<g class="drag-container drag-container_usual">
		<rect 
			class="drag-container__wrapper" 
			:width="width" :height="height"
			x="0" y="0"
			style="fill: lightgrey;
					stroke-width: 1px;
					stroke: grey;"/>
		<g class="drag-items" :transform="`translate(${padding[0]} ${padding[1]})`">
			<g 
				v-for="_, rowNum in items" :key="`items-row_num-${rowNum}`"
				:transform="`translate(0 ${rowNum * (itemSide + gap)})`">
				<g 
					v-for="itemExists, itemNum in items[rowNum]" :key="`drag-item_num-${itemNum}_row-${rowNum}`"
					v-if="itemExists"
					:transform="`translate(${itemNum * (gap + itemSide)} 0)`"
					:class="`drag-items__item drag-items__item_row-${rowNum}_item-${itemNum}`"
					style="cursor: grab;"
					@mousedown="startDrag(rowNum, itemNum, $event)"
					@touchstart="startDrag(rowNum, itemNum, $event)">
					<image class="drag-item__image" :href="`/problem_assets/scales/${itemImage}`" x="0" y="0" :width="itemSide" :height="itemSide"/>
					<text 
						class="drag-item__text" 
						:x="itemSide / 2" :y="itemSide / 2" 
						dy="0.35em"
						style="font-size: 1.5em; text-anchor: middle; font-weight: 600;"> {{ alph[itemNum] }} </text>
				</g>
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
		},
		dragMode: {
			type: Boolean,
			default: false
		},
		targetItemUsed: {
			type: Boolean,
			default: false
		}
	},
	data()  {
		return {
			inRow: 5,
			alph: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
			items: [],
			target: [], // row and column nums of currently dragging object
		}
	},
	computed: {
		padding() {
			const leftPadding = this.width * 0.05
			const topPadding = this.width * 0.05
			return [leftPadding, topPadding];
		},
		itemsInRow() {
			return Math.min(this.itemsAmount, this.inRow)
		},
	 	gap() {
			return (this.width - this.padding[0] * 2) / (this.itemsInRow * 9 + this.itemsInRow - 1);
		},
		itemSide() {
			const itemSide = (this.width - this.padding[0] * 2) / (this.itemsInRow + (this.itemsInRow - 1) * 0.1)
			return itemSide
		},
		rowsAmount() {
			return Math.floor(this.itemsAmount / this.inRow)
		},
		height() {
			const height = (this.itemSide + this.gap) * this.rowsAmount - this.gap + this.padding[1] * 2
			this.$emit('svgHeight', height)
			return height
		},
	},
	watch: {
		dragMode(isDrag) {
			console.log('drag mode changed!')
			console.log(this.targetItemUsed)
			if (!isDrag && this.target.length && !this.targetItemUsed) {
				this.$set(this.items[this.target[0]], this.target[1], true)
			}
		}
	},
	created() {
		const items = []
		let remainingItemsAmount = this.itemsAmount
		for (let row = 0; row < this.rowsAmount; row++) {
			items.push([])
			for (let column = 0; column < Math.min(remainingItemsAmount, this.inRow); column++) {
				items[row].push(true)
			}
			remainingItemsAmount -= this.inRow
		}
		this.items = items
	},
	methods: {
		startDrag(rowNum, itemNum, event) {
			if (this.dragMode) {
				return
			}
			this.$set(this.items[rowNum], itemNum, false)
			this.target = [rowNum, itemNum]
			this.$emit('setItemSide', document.querySelector('.drag-items__item').getBoundingClientRect().width)
			this.$emit('startDrag', document.querySelector(`.drag-items__item_row-${rowNum}_item-${itemNum}`).innerHTML, event)
		}
	}
}
</script>