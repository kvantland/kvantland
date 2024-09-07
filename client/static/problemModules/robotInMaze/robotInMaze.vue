<template>
	<div class="game_plot">
		<div class="first_row">
			<div class="maze_border">
				<svg class="maze" version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`" 
				preserveAspectRatio="xMidYMid meet" 
				overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
					<g v-for="(row, rowNum) in maze" :key="`row_${rowNum}`" :transform="`translate(0 ${rowNum * mazeSide})`" >
						<g v-if="rowNum > 0">
							<line  v-for="(column, columnNum) in verticalWalls(row)"  :key="`vertical_line_${columnNum}`" 
								:class="column ? 'border' : 'usual'" :x1="columnNum * mazeSide" y1="0" :x2="columnNum * mazeSide" :y2="-mazeSide" />
						</g>
						<g v-for="(column, columnNum) in horizontalWalls(row)" :key="`horizontal_line_${columnNum}`">
							<line :class="column ? 'border' : 'usual'" :x1="columnNum * mazeSide" y1="0" :x2="(columnNum + 1) * mazeSide" y2="0" />
						</g>
					</g>
				</svg>
			</div>
			<div class="start_area">
				<p>C помощью команд и цикловой конструкции:</p>
				<div v-for="(block, blockNum) in commands" :key="`start_area_block_${blockNum}`" :class="['block', block.type]" 
					@mousedown="moveFromStartArea(block, $event)" 
					@touchstart="moveFromStartArea(block, $event.touches[0])">
					<p>{{ block.text }}</p>
					<div v-if="block.type === 'cycle'" class="insert_zone"></div>
				</div>
			</div>
		</div>
		<div class="description">
			<p><b>Соберите код, который поможет роботу дойти из клетки S в клетку F.</b></p>
			<p>Суммарно разрешено использовать не более 7 блоков (блоком считается и цикловая конструкция, и команда). 
			Также роботу следует выполнить не более 100 поворотов или шагов вперед.</p>
		</div>
		<div ref="answerArea" class="second_row answer_area">
			<p style="font-size: 30px; font-weight: 700;"> Код: </p>
			<div v-for="(block, blockNum) in answerAreaBlocks" :key="`block_with_num_${blockNum}`" class="block_with_num">
				<div class="block_num"> {{ blockNum + 1 }}. </div>
				<div :class="['block', block.type]" :block_id="block.id"  @mousedown="moveFromAnswerArea(block.id, $event)" 
				@touchstart="moveFromAnswerArea(block.id, $event.touches[0])"> 
					<p>{{ block.text }} </p>
						<div v-if="block.type === 'cycle'" class="insert_zone">
							<div v-for="(childBlock, childBlockNum) in block.children" :key="`child_block_${childBlockNum}_of_${block.id}`"
								:block_id="childBlock.id"
								:class="['block', childBlock.type]"  in_cycle="true"  @mousedown="moveFromAnswerArea(childBlock.id, $event)"
								@touchstart="moveFromAnswerArea(childBlock.id, $event.touches[0])">
								<p>{{ childBlock.text }} </p>
								<div v-if="childBlock.type === 'cycle'" class="insert_zone">
									<div v-for="(childChildBlock, childChildBlockNum) in childBlock.children" v-if="childChildBlock.type !== 'cycle'"
									:key="`child_child_block_${childChildBlockNum}_of_${childChildBlock.id}`" :block_id="childChildBlock.id"
									:class="['block', childChildBlock.type]"  in_cycle="true"  @mousedown="moveFromAnswerArea(childChildBlock.id, $event)"
									@touchstart="moveFromAnswerArea(childChildBlock.id, $event.touches[0])">
									<p>{{ childChildBlock.text }} </p>
									<div v-if="childChildBlock.type === 'cycle'" class="insert_zone"></div>
									</div>
								</div>
							</div>
						</div>
				</div>
			</div>
		</div>
		<div v-if="targetBlock" :class="['block', targetBlock.type, 'target_block']" 
			:style="`left: ${targetBlock.x}px; top: ${targetBlock.y}px	;`"> {{ targetBlock.text }} </div>
	</div>
</template>

<script>
export default {
	props: {
		problemParams:{
			type: Object,
			default() {
				return {}
			},
		}
	},

	data() {
		return {
			mazeSide: 30,
			answerAreaBlocks: [],
			dragMode: false,
			nearestPlaceToInsert: undefined,
			targetBlock: undefined,
			currentBlockId: 1,
		}
	},

	computed: {
		maze() {
			return this.problemParams.maze
		},
		svgHeight() {
			return (this.maze.length - 1) * this.mazeSide
		},
		svgWidth() {
			return (this.maze.length - 1) * this.mazeSide
		},
		commands() {
			return this.problemParams.commands
		}
	},

	mounted() {
		document.addEventListener('mousemove', this.drag, {passive: false})
		document.addEventListener('touchmove', this.drag, {passive: false})
		document.addEventListener('touchend', this.endDrag)
		document.addEventListener('mouseup', this.endDrag)
	},

	methods: {
		verticalWalls(row) {
			const walls = []
			for (const symb of row.toString()) {
				if (symb === '.') {
					walls.push(false)
				}
				else if (symb === '|') {
					walls.push(true)
				}
			}
			return walls
		},

		horizontalWalls(row) {
			const walls = []
			for (const symb of row.toString()) {
				if (symb === ' ') {
					walls.push(false)
				}
				else if (symb === '_') {
					walls.push(true)
				}
			}
			return walls
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

		findNewNearestPlaceToInsert(y) {
			let index = 0
			const blocks = document.querySelectorAll('.answer_area .block')
			let parentId = this.currentBlockId
			for (const block of blocks) {
				const blockRect = block.getBoundingClientRect()
				if (block.classList.contains('cycle') && !block.classList.contains('select')) {
					if (y >= blockRect.top && y <= blockRect.bottom) {
						index = 0
						const childrenBlocks = document.querySelectorAll(`.answer_area .cycle.block[block_id='${block.getAttribute('block_id')}'] .block`)
						for (const childBlock of childrenBlocks) {
							const childBlockRect = childBlock.getBoundingClientRect()
							if (childBlock.classList.contains('cycle') && !childBlock.classList.contains('select')) {
								if (y >= childBlockRect.top && y <= childBlockRect.bottom) {
									if (this.targetBlock.type === 'cycle') {
										return undefined
									}
									index = 0
									const childrenChildrenBlocks = document.querySelectorAll(`.answer_area .cycle.block[block_id='${childBlock.getAttribute('block_id')}'] .block`)
									for (const childChildBlock of childrenChildrenBlocks) {
										const childChildBlockRect = childChildBlock.getBoundingClientRect()
										if (y >= (childChildBlockRect.top + childChildBlockRect.bottom) / 2 && !childChildBlock.classList.contains('select')){
											index++
										}
									}
									parentId = childBlock.getAttribute('block_id')
									return {index, parent: parentId}
								}
							}
							if (y >= (childBlockRect.top + childBlockRect.bottom) / 2 && !childBlock.classList.contains('select')){
								index++
							}
						}
						parentId = block.getAttribute('block_id')
						return {index, parent: parentId}
					}
				}
				if (y >= (blockRect.top + blockRect.bottom) / 2 && !block.classList.contains('select')){
					index += 1
				}
			}
			return {index, parent: parentId}
		},

		removeSelectedBlock() {
			const answerAreaBlocksProto = JSON.parse(JSON.stringify(this.answerAreaBlocks))
			const newAnswerAreaBlocks = []
			for (const block of answerAreaBlocksProto) {
				const newBlock = JSON.parse(JSON.stringify(block))
				const newChildren = []
				if (block.children) {
					for (const childBlock of block.children) {
						const newChildBlock = JSON.parse(JSON.stringify(childBlock))
						const newChildrenChildren = []
						if (childBlock.children) {
							for (const childChildBlock of childBlock.children) {
								if (childChildBlock.type.split(' ')[0] !== 'select') {
									newChildrenChildren.push(childChildBlock)
								}
							}
							newChildBlock.children = newChildrenChildren
						}
						if (newChildBlock.type.split(' ')[0] !== 'select') {
							newChildren.push(newChildBlock)
						}
					}
					newBlock.children = newChildren
				}
				if (newBlock.type.split(' ')[0] !== 'select') {
					newAnswerAreaBlocks.push(newBlock)
				}
			}
			console.log('after remove: ', newAnswerAreaBlocks)
			this.answerAreaBlocks = newAnswerAreaBlocks
			this.$emit('updateAnswer', this.answerAreaBlocks)
		},

		updateNearestPlaceToInsert(x, y) {
			if (!this.inRect(x, y, this.$refs.answerArea.getBoundingClientRect())) {
				this.removeSelectedBlock()
				this.nearestPlaceToInsert = undefined
				return;
			}
			this.removeSelectedBlock()
			const newIndex = this.findNewNearestPlaceToInsert(y)
			if (!newIndex) {
				this.nearestPlaceToInsert = undefined
				this.endDrag()
				return
			}
			console.log('index to insert: ', newIndex)
			this.nearestPlaceToInsert = newIndex
			const newAnswerAreaBlocks = JSON.parse(JSON.stringify(this.answerAreaBlocks))
			if (newIndex.parent !== this.currentBlockId) {
				for (const block of newAnswerAreaBlocks) {
					if (block.id == this.nearestPlaceToInsert.parent) {
						if (!block.children) {
							block.children = [{text: this.targetBlock.text, type: `select ${this.targetBlock.type}`, parent: newIndex.parent, id: this.currentBlockId}]
						}
						else {
							block.children.splice(newIndex.index, 0, {text: this.targetBlock.text, type: `select ${this.targetBlock.type}`, parent: newIndex.parent, id: this.currentBlockId})
						}
						break
					}
					for (const childBlock of block.children) {
						if (childBlock.id == this.nearestPlaceToInsert.parent) {
							if (!childBlock.children) {
								childBlock.children = [{text: this.targetBlock.text, type: `select ${this.targetBlock.type}`, parent: newIndex.parent, id: this.currentBlockId}]
							}
							else {
								childBlock.children.splice(newIndex.index, 0, {text: this.targetBlock.text, type: `select ${this.targetBlock.type}`, parent: newIndex.parent, id: this.currentBlockId})
							}
							break
						}
					}
				}
			}
			else if (newIndex.index >= newAnswerAreaBlocks.length) {
					newAnswerAreaBlocks.push({text: this.targetBlock.text, type: `select ${this.targetBlock.type}`, id: this.currentBlockId})
				}
				else {
					newAnswerAreaBlocks.splice(newIndex.index, 0, {text: this.targetBlock.text, type: `select ${this.targetBlock.type}`, id: this.currentBlockId})
				}
			this.answerAreaBlocks = newAnswerAreaBlocks
			this.$emit('updateAnswer', this.answerAreaBlocks)
		},

		moveAt(x, y) {
			this.autoscroll()
			this.$set(this.targetBlock, 'x', x)
			this.$set(this.targetBlock, 'y', y)
			// console.log(this.targetBlock.x, this.targetBlock.y)
			if (!this.inAllowedArea()) {
				this.endDrag()
			}
		},

		moveFromStartArea(block, event) {
			this.targetBlock = block
			this.targetBlock.id = this.currentBlockId
			this.startDrag(event)
		},

		moveFromAnswerArea(blockNum, event) {
			if (this.targetBlock) {
				return
			}
			const answerAreaBlocksProto = JSON.parse(JSON.stringify(this.answerAreaBlocks))
			const newAnswerAreaBlocks = []
			for (const block of answerAreaBlocksProto) {
				const newBlock = JSON.parse(JSON.stringify(block))
				const newChildren = []
				if (block.children) {
					for (const childBlock of block.children) {
						if (childBlock.id !== blockNum) {
							newChildren.push(childBlock)
						}
						else {
							this.targetBlock = childBlock
						}
					}
					newBlock.children = newChildren
				}
				if (newBlock.id !== blockNum) {
					newAnswerAreaBlocks.push(newBlock)
				}
				else {
					this.targetBlock = block
				}
			}
			this.answerAreaBlocks = newAnswerAreaBlocks
			this.$emit('updateAnswer', this.answerAreaBlocks)
			this.startDrag(event)
		},

		startDrag(event) {
			const x = event.clientX
			const y = event.clientY
			this.dragMode = true
			this.moveAt(x, y)
		},

		drag(event) {
			if (!this.dragMode) {
				return
			}
			if (this.targetBlock === undefined)
				return
			let x, y
			if (event.touches) {
				event.preventDefault()
				x = event.touches[0].clientX
				y = event.touches[0].clientY
			}
			else {
				x = event.clientX
				y = event.clientY
			}
			this.moveAt(x, y)
			this.updateNearestPlaceToInsert(x, y)
		},

		endDrag() {
			if (!this.dragMode) {
				return
			}
			if (this.nearestPlaceToInsert !== undefined) {
				this.targetBlock.parent = this.nearestPlaceToInsert.parent
				if (this.nearestPlaceToInsert.parent !== this.currentBlockId) {
					for (const block of this.answerAreaBlocks) {
						if (block.id == this.nearestPlaceToInsert.parent) {
							if (!block.children) {
								block.children = [this.targetBlock]
							}
							else {
								block.children.splice(this.nearestPlaceToInsert.index, 0, this.targetBlock)
							}
						}
						if (block.children) {
							for (const childBlock of block.children) {
								if (childBlock.id == this.nearestPlaceToInsert.parent) {
									if (!childBlock.children) {
										childBlock.children = [this.targetBlock]
									}
									else {
										childBlock.children.splice(this.nearestPlaceToInsert.index, 0, this.targetBlock)
									}
								}
							}
						}
					}
				}
				else {
					this.$set(this.answerAreaBlocks, this.nearestPlaceToInsert.index, this.targetBlock)
				}
				this.removeSelectedBlock()
				this.$emit('updateAnswer', this.answerAreaBlocks)
				this.currentBlockId += 1
			}
			this.dragMode = false
			this.targetBlock = undefined
			this.nearestPlaceToInsert = undefined
		}
	},
}
</script>