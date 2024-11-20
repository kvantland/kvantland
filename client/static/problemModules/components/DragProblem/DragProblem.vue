<template>
	<div style="width: 100%">
		<slot name="container">

			<slot class="drag-container">
				<div class="drag-container__elems">
					<div
						v-for="elem, elemNum in dragElems"
						:key="`drag-elem_num-${elemNum}`"
						class="drag-container__elem" 
						@touchstart="dragFromStartArea(elemNum)"
						@mousedown="dragFromStartArea(elemNum)"
						v-html="elem.html">
					</div>
				</div>
			</slot>

			<slot 
				v-for="container, containerNum in dropContainers"
				:name="`drop-container_num-${containerNum}`"
				class="drop-container">
				<div :key="`drop-container_num-${containerNum}`" class="drop-container__elems">
					<div
						v-for="elem, elemNum in container.elems"
						:key="`drop-container__elem_container-${containerNum}_num-${elemNum}`"
						:class="`drop-container__elem_container-${containerNum}_num-${elemNum}`"
						@touchstart="dragFromDropArea(containerNum, elemNum)"
						@mousedown="dragFromDropArea(containerNum, elemNum)"
						v-html="elem.html">
					</div>
				</div>
			</slot>

			<div 
				v-if="targetElem" 
				class="target-elem" 
				:style="`left: ${targetElem.x}px; top: ${targetElem.y}px;`"
				v-html="targetElem">
			</div>
		</slot>
	</div>
</template>

<script>
export default {
	props: {
		dropContainersNum: {
			type: Array,
			default: () => {return []}
		}
	},
	data() {
		const dropContainers = []
		for (let containerNum = 0; containerNum < dropContainersNum; containerNum++) {
			dropContainers.push([])
		}
		return {
			dropContainers,
			targetElem: undefined,
			dragMode: false,
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

		inRect(x, y, rect){
			if (x > rect.right || x < rect.left) {
				return false
			}
			if (y > rect.bottom || y < rect.top) {
				return false
			}
			return true
		},

		moveAt(x, y) {
			this.autoscroll()
			this.$set(this.targetElem, 'x', x)
			this.$set(this.targetElem, 'y', y)
			if (!this.inAllowedArea()) {
				this.endDrag()
			}
		},

		drag(event) {
			if (!this.dragMode) {
				return
			}
			if (this.targetElem === undefined)
				return
			console.log('drag', event)
			const x = event.clientX
			const y = event.clientY
		
			this.moveAt(x, y)
		},

		dragFromStartArea(elemNum) {
			this.targetElem = this.dragElems[elemNum].html
		},

		dragFromDropArea(containerNum, elemNum) {
			this.targetElem = this.dropContainers[containerNum][elemNum].html
			this.dropContainers[containerNum].splice(elemNum, 1)
		}
	}
}
</script>