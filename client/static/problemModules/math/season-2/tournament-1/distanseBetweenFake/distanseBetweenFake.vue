<template>
	 <div class="svg_with_buttons">
    <svg
			ref="svg" version="1.1" class="display_svg" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
				preserveAspectRatio="xMidYMid meet" 
				overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
			<Scales
				:scale="1" :left-cup-objects="cupWeights.left" :right-cup-objects="cupWeights.right" :move-to="newSide" 
				:target="target.dom"
				:item-side="itemSide"
				:object-scale="{x: 0.9, y: 0.4}"
				@updateNearestCup="updateNearestCup"
				@svgHeight="getScalesHeight"	@svgWidth="getScalesWidth" 
				@moveFromCup="moveFromCup" @stopMove="stopWeight" />
			<DragContainer 
				:transform="`translate(${(svgWidth - dragZoneWidth) / 2} ${scalesHeight + gap})`"
				item-image="coin.svg"
				:drag-mode="dragMode"
				:return-objects="returnObjects"
				:items-amount="5" :width="dragZoneWidth" 
				@svgHeight="getDragContainerHeight"
				@startDrag="startDrag"
				@setItemSide="setItemSide" />
			<g 
				v-if="dragMode" 
				ref="target" class="target" 
				:transform="`translate(${target.svg.x} ${target.svg.y})`"
				style="cursor: grabbing;"
				v-html="target.html" />
		</svg>
		<History 
			:weighting-history="weightingHistory" 
			:weightings-amount="weightingsAmount"
			@clearWeights="clearWeights" @startWeight="startWeight"/>
	</div>
</template>

<script>
import Scales from '~/static/problemModules/components/Scales/Scales.vue';
import History from '~/static/problemModules/components/Scales/History.vue';
import DragContainer from '~/static/problemModules/components/Scales/containers/dragContainer.vue';

export default {
	components: {
		Scales, 
		History,
		DragContainer,
	},
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		},
		xhrData: {
			type: Object,
			default: () => {}
		},
		newXhr: {
			type: Boolean,
			default: false
		},
		confirmActionResult:{
			type: Boolean,
			default: undefined,
		}
	},
	data() {
		return {
			dragZoneWidth: 0,
			scalesHeight: 0,
			gap: 50,
			cupWeights: {left: [], right: []},
			newSide: undefined,
			svgWidth: 0,
			svgHeight: 0,
			itemSide: 0,

			dragMode: false,
			target: {
				html: undefined,
				rowNum: undefined,
				itemNum: undefined,
				svg: {x: 0, y: 0},
				dom: {x: 0, y: 0}
			},
			nearestCup: undefined,
			returnObjects: undefined,
		}
	},
	computed: {
		weightingsAmount() {
			return this.problemParams.weightings_amount
		},
		weightingHistory() {
			return this.problemParams?.history
		},
		confirmResult() {
			return this.confirmActionResult
		}
	},
	watch: {
		newXhr(isNew) {
			if (isNew) {
				this.$emit('xhrGet')
				console.log(this.xhrData)
				if (this.xhrData.xhr_answer.message) {
					this.$emit('showXhrDialog', this.xhrData.xhr_answer.message)
				}
				this.newSide = this.xhrData.xhr_answer.move_side
			}
		},
		confirmResult(result) {
			if (result) {
				this.$emit('xhrRequest', {weights: this.cupWeights})
			}
		}
	},
	mounted() {
		document.addEventListener('pointermove', this.drag, {passive: false})
		document.addEventListener('pointerup', this.endDrag)
	},
	destroyed() {
		document.removeEventListener('pointermove', this.drag, {passive: false})
		document.removeEventListener('pointerup', this.endDrag)
	},
	methods: {
		getScalesWidth(width) {
			this.dragZoneWidth = width * 0.8
			this.svgWidth = width
		},
		getScalesHeight(height) {
			this.scalesHeight = height
			this.svgHeight += height
		},
		getDragContainerHeight(height) {
			this.svgHeight += height + this.gap
		},
		updateNearestCup(cupName) {
			console.log('nearest cup: ', cupName)
			this.nearestCup = cupName
		},
		startDrag(targetItem, event) {
			this.dragMode = true
			this.target.html = targetItem.html
			this.target.rowNum = targetItem.rowNum
			this.target.itemNum = targetItem.itemNum

			let coordinates = event
			event.preventDefault()
			if (event.touches) {
				coordinates = event.touches[0]
			}
			const x = coordinates.clientX
			const y = coordinates.clientY
			this.moveAt(x, y)
		},
		drag(event) {
			if (!this.dragMode) {
				return
			}
			if (this.target.html === undefined)
				return
			const x = event.clientX
			const y = event.clientY
		
			this.moveAt(x, y)
		},
		endDrag() {
			if (!this.dragMode) {
				return;
			}
			if (!this.nearestCup) {
				this.backToDrag()
			}
			else {
				this.cupWeights[this.nearestCup].push(JSON.parse(JSON.stringify(this.target)))
			}
			this.dragMode = false
		},
		backToDrag() {
			if (this.target.html) {
				this.returnObjects = JSON.parse(JSON.stringify([this.target]))
			}
		},
		setItemSide(side) {
			this.itemSide = side
		},
		moveFromCup(data) {
			this.cupWeights[data.cup].splice(data.itemIndex, 1)
			this.nearestCup = undefined
			this.startDrag(data.item, window.event)
		},
		stopWeight(){
		},
		clearWeights(){
			const returnObjects = []
			for (const object of this.cupWeights.left) {
				returnObjects.push(object)
			}
			for (const object of this.cupWeights.right) {
				returnObjects.push(object)
			}
			this.cupWeights = {
				left: [],
				right: []
			}
			this.dragMode = false
			this.returnObjects = returnObjects
			this.newSide = "equal"
		},
		startWeight(){
			this.$emit('showConfirmDialog', {
				content: "Вы уверены, что хотите совершить взвешивание?", 
				acceptText: "Да", 
				refuseText: "Нет"})
		},
		convertDOMtoSVG(x, y) {
			try {
				const pt = new DOMPoint(x, y)
				const svgP = pt.matrixTransform(this.$refs.svg.getScreenCTM().inverse())
				return {x: svgP.x, y: svgP.y}
			}
			catch(e) {
				return false
			}
		},
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
		moveAt(x, y) {
			const newCursorCoordinates = this.convertDOMtoSVG(x - this.itemSide / 2, y - this.itemSide / 2)
			if (!newCursorCoordinates)
					return
			this.autoscroll()
			this.$set(this.target.svg, 'x', newCursorCoordinates.x)
			this.$set(this.target.svg, 'y', newCursorCoordinates.y)
			this.$set(this.target.dom, 'x', x)
			this.$set(this.target.dom, 'y', y)
			if (!this.inAllowedArea()) {
					this.endDrag()
			}
		},
		inAllowedArea() { // if target object in allowed aarea
			const targetX = window.event.clientX
			const targetY = window.event.clientY
			if (targetX < 0 || targetX > window.innerWidth)
					return false
			if (targetY < 0 || targetY > window.innerHeight)
					return false
			return true
		},
	}
}
</script>