<template>
	<div class="problem-plot">
		<div class="drop-container">
			<img class="drop-container__background" src="/problem_assets/richest_island_resident/background.svg" />
			<div class="drop-container__content">
				<div ref="second" class="place place_second">
					<img 
						v-if="choosedElements.second !== undefined"
						class="drag-person"
						:src="`/problem_assets/richest_island_resident/${choosedElements.second.img}`"
						@touchstart="dragFromDropArea('second', $event)"
						@mousedown="dragFromDropArea('second', $event)" />
					<img 
						v-if="nearestContainer === 'second'"
						class="drag-person drag-person_placeholder"
						:src="`/problem_assets/richest_island_resident/${targetPerson.img}`" />
				</div>
				<div ref="first" class="place place_first">
					<img 
						v-if="choosedElements.first !== undefined"
						class="drag-person"
						:src="`/problem_assets/richest_island_resident/${choosedElements.first.img}`"
						@touchstart="dragFromDropArea('frist', $event)"
						@mousedown="dragFromDropArea('first', $event)" />
					<img 
						v-if="nearestContainer === 'first'"
						class="drag-person drag-person_placeholder"
						:src="`/problem_assets/richest_island_resident/${targetPerson.img}`" />
				</div>
				<div ref="third" class="place place_third">
					<img 
						v-if="choosedElements.third !== undefined"
						class="drag-person"
						:src="`/problem_assets/richest_island_resident/${choosedElements.third.img}`"
						@touchstart="dragFromDropArea('third', $event)"
						@mousedown="dragFromDropArea('third', $event)" />
					<img 
						v-if="nearestContainer === 'third'"
						class="drag-person drag-person_placeholder"
						:src="`/problem_assets/richest_island_resident/${targetPerson.img}`" />
				</div>
			</div>
		</div>
		<div class="drag-container">
			<img
				v-for="dragElement, dragElementNum in dragElementsNotChoosed"
				:key="`drag-element_num-${dragElementNum}`"
				class="drag-person"
				:src="`/problem_assets/richest_island_resident/${dragElement.img}`"
				@touchstart="dragFromStartArea(dragElement, $event)"
				@mousedown="dragFromStartArea(dragElement, $event)">
			</img>
		</div>
		<img 
			v-if="targetPerson !== undefined && dragMode"
			class="drag-person drag-person_target" 
			:src="`/problem_assets/richest_island_resident/${targetPerson.img}`"
			:style="`left: ${targetPerson.x}px; top: ${targetPerson.y}px;`" />
	</div>
</template>

<script>
export default {
	model: {
		prop: 'answer',
		event: 'updateAnswer'
	},
	data() {
		return {
			dragElements: [
				{img: 'Donald.svg', index: 0, choosed: false},
				{img: 'Ilon.svg', index: 1, choosed: false},
				{img: 'Bill.svg', index: 2, choosed: false}],
			choosedElements: {first: undefined, second: undefined, third: undefined},
			dragMode: false,
			nearestContainer: undefined,
			targetPerson: undefined
		}
	},
	computed: {
		dragElementsNotChoosed() {
			const dragElements = []
			for (const element of this.dragElements) {
				if (!element.choosed) {
					dragElements.push(element)
				}
			}
			return dragElements
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

		inRect(x, y, rect){
			if (x > rect.right || x < rect.left) {
				return false
			}
			if (y > rect.bottom || y < rect.top) {
				return false
			}
			return true
		},

		inAllowedArea() { // if target object in allowed aarea
			const targetX = window.event.clientX
			const targetY = window.event.clientY
			// console.log(targetX, targetY)
			if (targetX < 0 || targetX > window.innerWidth)
				return false
			if (targetY < 0 || targetY > window.innerHeight)
				return false
			return true
		},

		moveAt(x, y) {
			this.autoscroll()
			this.$set(this.targetPerson, 'x', x)
			this.$set(this.targetPerson, 'y', y)
			this.updateNearestContainer()
			if (!this.inAllowedArea()) {
				this.endDrag()
			}
		},

		startDrag(event) {
			let coordinates = event
			event.preventDefault()
			if (event.touches) {
				coordinates = event.touches[0]
			}
			const x = coordinates.clientX
			const y = coordinates.clientY
			this.dragMode = true
			this.moveAt(x, y)
		},

		drag(event) {
			if (!this.dragMode) {
				return
			}
			if (this.targetPerson === undefined)
				return
			const x = event.clientX
			const y = event.clientY
			this.moveAt(x, y)
		},

		endDrag() {
			console.log(this.nearestContainer)
			if (this.nearestContainer === undefined && this.targetPerson !== undefined) {
				this.backToStartArea()
			}
			else {
				this.dropToContainer(this.nearestContainer)
			}
			this.dragMode = false
			this.targetPerson = undefined
			this.nearestContainer = undefined
		},

		dragFromStartArea(person, event) {
			this.dragElements[person.index].choosed = true
			this.targetPerson = person
			this.startDrag(event)
		},

		dragFromDropArea(container, event) {
			this.targetPerson = this.choosedElements[container]
			this.choosedElements[container] = undefined
			this.startDrag(event)
			this.$emit('updateAnswer', [
				this.choosedElements.first?.index, 
				this.choosedElements.second?.index,
				this.choosedElements.third?.index])
		},

		backToStartArea() {
			for (const person of this.dragElements) {
				if (person.img === this.targetPerson.img) {
					this.dragElements[person.index].choosed = false
					break;
				}
			}
		},

		dropToContainer(container) {
			this.choosedElements[container] = this.targetPerson
			this.$emit('updateAnswer', [
				this.choosedElements.first?.index, 
				this.choosedElements.second?.index,
				this.choosedElements.third?.index])
		},

		updateNearestContainer() {
			const firstContainer = this.$refs.first.getBoundingClientRect()
			const secondContainer = this.$refs.second.getBoundingClientRect()
			const thirdContainer = this.$refs.third.getBoundingClientRect()
			const [targetX, targetY] = [this.targetPerson.x, this.targetPerson.y]

			if (this.inRect(targetX, targetY, firstContainer) && this.choosedElements.first === undefined) {
				this.nearestContainer = 'first'
			}
			else if (this.inRect(targetX, targetY, secondContainer) && this.choosedElements.second === undefined) {
				this.nearestContainer = 'second'
			}
			else if (this.inRect(targetX, targetY, thirdContainer) && this.choosedElements.third === undefined) {
				this.nearestContainer = 'third'
			}
			else {
				this.nearestContainer = undefined
			}
		}
	}
}
</script>