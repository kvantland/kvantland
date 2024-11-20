<template>
	<div class="predictions-problem">
		<div class="drag-container">
			<div 
				v-for="block, blockNum in dragBlocks" :key="`block_name-${blockNum}`"
				:class="['drag-block', `drag-block_active-${block.active}`]"
				@touchstart="dragFromStartArea(blockNum, $event)"
				@mousedown="dragFromStartArea(blockNum, $event)">
				{{ block.name }}
			</div>
		</div>
		<div class="drop-containers">
				<div ref="boys" class="drop-container drop-container_boys">
					<div class="drop-container__content">
						<h2 class="drop-container__title"> Мальчики </h2>
						<div 
							v-for="boyName, boyNum in boysChoosed"
							:key="`boy_num-${boyNum}`"
							class="drag-block"
							@touchstart="dragFromDropArea(boyNum, 'boys', $event)"
							@mousedown="dragFromDropArea(boyNum, 'boys', $event)">
							{{ boyName }}
						</div>
						<div
							v-if="nearestContainer === 'boys'"
							class="drag-block drag-block_active-false">
							{{ targetBlock.name }}
						</div>
					</div>
					<img class="drop-container__image" src="/problem_assets/predictions/boy.svg"/>
				</div>

				<div ref="girls" class="drop-container drop-container_girls">
					<div class="drop-container__content">
						<h2 class="drop-container__title"> Девочки </h2>
						<div 
							v-for="girlName, girlNum in girlsChoosed"
							:key="`girl_num-${girlNum}`"
							class="drag-block"
							@touchstart="dragFromDropArea(girlNum, 'girls', $event)"
							@mousedown="dragFromDropArea(girlNum, 'girls', $event)">
							{{ girlName }}
						</div>
						<div
							v-if="nearestContainer === 'girls'"
							class="drag-block drag-block_active-false">
							{{ targetBlock.name }}
						</div>
					</div>
					<img class="drop-container__image" src="/problem_assets/predictions/girl.svg"/>
				</div>
		</div>
		<div 
			v-if="targetBlock !== undefined && dragMode"
			class="drag-block drag-block_target"
			:style="`left: ${targetBlock.x}px; top: ${targetBlock.y}px;`"
			> {{ targetBlock.name }}
		</div>
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
			dragBlocks: [
				{name: 'Валя', active: true}, 
				{name: 'Женя', active: true}, 
				{name: 'Саша', active: true}],
			boysChoosed: [],
			girlsChoosed: [],
			targetBlock: undefined,
			dragMode: false,
			nearestContainer: undefined,
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
			this.$set(this.targetBlock, 'x', x)
			this.$set(this.targetBlock, 'y', y)
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
			if (this.targetBlock === undefined)
				return
			const x = event.clientX
			const y = event.clientY
			this.moveAt(x, y)
		},

		endDrag() {
			if (this.nearestContainer === undefined && this.targetBlock !== undefined) {
				this.backToStartArea()
			}
			else {
				this.dropToContainer(this.nearestContainer)
			}
			this.dragMode = false
			this.targetBlock = undefined
			this.nearestContainer = undefined
		},

		dragFromStartArea(blockNum, event) {
			const targetBlock = this.dragBlocks[blockNum]
			if (!targetBlock.active) return;
			this.$set(targetBlock, 'active', false)
			this.targetBlock = {}
			this.$set(this.targetBlock, 'name', targetBlock.name)
			this.startDrag(event)
		},

		dragFromDropArea(blockNum, containerName, event) {
			let container
			switch(containerName) {
				case 'boys': 
					container = this.boysChoosed
					break;
				case 'girls':
					container = this.girlsChoosed
					break;
			}
			this.targetBlock = {}
			console.log(container)
			console.log(container[blockNum])
			this.targetBlock.name = container[blockNum]
			container.splice(blockNum, 1)
			this.startDrag(event)
			this.$emit('updateAnswer', {boysChoosed: this.boysChoosed, girlsChoosed: this.girlsChoosed})
		},

		backToStartArea() {
			let blockIndex
			for (let blockNum = 0; blockNum < this.dragBlocks.length; blockNum++) {
				if (this.dragBlocks[blockNum].name === this.targetBlock.name) {
					blockIndex = blockNum
					break;
				}
			}
			this.$set(this.dragBlocks[blockIndex], 'active', true)
		},

		dropToContainer(containerName) {
			switch (containerName) {
				case 'boys':
					this.boysChoosed.push(this.targetBlock.name)
					break;
				case 'girls':
					this.girlsChoosed.push(this.targetBlock.name)
					break;
			}
			this.$emit('updateAnswer', {boysChoosed: this.boysChoosed, girlsChoosed: this.girlsChoosed})
		},

		updateNearestContainer() {
			const boysContainer = this.$refs.boys.getBoundingClientRect()
			const girlsContainer = this.$refs.girls.getBoundingClientRect()
			const [targetX, targetY] = [this.targetBlock.x, this.targetBlock.y]

			if (this.inRect(targetX, targetY, boysContainer)) {
				this.nearestContainer = 'boys'
			}
			else if (this.inRect(targetX, targetY, girlsContainer)) {
				this.nearestContainer = 'girls'
			}
			else {
				this.nearestContainer = undefined
			}
		}

	}
}
</script>