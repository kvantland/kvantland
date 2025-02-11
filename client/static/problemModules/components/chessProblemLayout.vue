<template>
    <svg version="1.1" overflow="visible" ref="svg"
        style="-webkit-user-select: none; user-select: none;"
        preserveAspectRatio="xMidYMid meet" 
        :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
        xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <g class="board">
            <g class="row" v-for="(row, rowIndex) in boardSide" :transform="`translate(0 ${rowIndex * boardItemSide})`">
                <g class="item" v-for="(column, columnIndex) in boardSide" :transform="`translate(${columnIndex * boardItemSide} 0)`" 
                    :row="rowIndex" :column="columnIndex">
                    <rect v-if="(rowIndex + columnIndex) % 2 == 0" fill="white" stroke="black" :width="boardItemSide" :height="boardItemSide" x="0" y="0" />
                    <rect v-else fill="orange" stroke="black" :width="boardItemSide" :height="boardItemSide" x="0" y="0" />
                    <image v-if="boardArrayConfiguration[rowIndex][columnIndex].type" 
                        :class="`dragFigure ${boardArrayConfiguration[rowIndex][columnIndex].moveStatus}`"
                        @touchstart="moveFromBoard(boardArrayConfiguration[rowIndex][columnIndex].type, $event, rowIndex, columnIndex)" 
                        @mousedown="moveFromBoard(boardArrayConfiguration[rowIndex][columnIndex].type, $event, rowIndex, columnIndex)"
                        :href="`/problem_assets/chess/${boardArrayConfiguration[rowIndex][columnIndex].type}.png`"
                        :width="dragFigureWidth" :height="dragFigureWidth" :x="figureMarginTop" :y="figureMarginTop" />
                </g>
            </g>
        </g>
        <g class="interactiveZone" :transform="`translate(${boardWidth + gap} 0)`">
            <g v-for="(dragFigure, dragFigureIndex) in dragFigures" 
                :transform="`translate(0 ${boardItemSide * dragFigureIndex})`">
                <template v-if="dragFigure.amount != 'inf'">
                    <image :class="[dragFigure.amount > 0 ? 'active' : 'passive', 'dragFigure']" :width="dragFigureWidth" 
                        @touchstart="moveFromDragZone(dragFigure.type, dragFigureIndex, $event)" 
                        @mousedown="moveFromDragZone(dragFigure.type, dragFigureIndex, $event)"
                        :height="dragFigureHeight" x="0" y="0" :href="`/problem_assets/chess/${dragFigure.type}.png`"/>
                    <text v-if="dragFigure.amount != 'inf'" style="font-size: 11px; font-weight: 600;" :transform="`translate(0 ${dragFigureHeight + dragFigureTextHeight})`"> Осталось: {{ dragFigure.amount }} </text>
                </template>
                <image v-else class="dragFigure active" :width="dragFigureWidth" 
                    :height="dragFigureHeight" :x="figureMarginTop" 
                    @touchstart="moveFromDragZone(dragFigure.type, dragFigureIndex, $event)" 
                    @mousedown="moveFromDragZone(dragFigure.type, dragFigureIndex, $event)"
                    :y="figureMarginTop" :href="`/problem_assets/chess/${dragFigure.type}.png`" />
            </g>
        </g>
        <image v-if="dragMode" class="targeted" :href="`/problem_assets/chess/${target.type}.png`" 
            :x="target.x" :y="target.y"
            :width="dragFigureWidth" :height="dragFigureHeight"  />
    </svg>
</template>

<script>
export default {
    props: {
        boardSide: {default: 8},
        boardItemSide: {default: 60},
        boardConfiguration: {default: 'empty'},
        gap: {default: 20},
        dragFigures: {default() {return []}},
        dragFigureTextHeight: {default: 11},
    },
    data() {
        return {
            target: {type: undefined, x:0, y:0},
            dragMode: false, // is drag?
        }
    },
    computed: {
        boardArrayConfiguration() {
					console.log(this.boardConfiguration)
            let configuration = []
            if (this.boardConfiguration === 'empty') {
                for (let row = 0; row < this.boardSide; row++) {
                    configuration.push([])
                    for (let column = 0; column < this.boardSide; column++) {
                        configuration[row].push({type: '', moveStatus: ''})
                    }
                }
                return configuration
            }
            else {
                return this.boardConfiguration
            }
        },
        boardWidth() {
            return this.boardSide * this.boardItemSide
        },
        dragFigureWidth() {
            return this.boardItemSide - this.dragFigureTextHeight
        },
        dragFigureHeight() {
            return this.boardItemSide - this.dragFigureTextHeight
        },
        figureMarginTop() {
            return this.dragFigureTextHeight / 2
        },
        svgHeight() {
            return this.boardSide * this.boardItemSide
        },
        svgWidth() {
            return this.boardWidth + this.gap + this.dragFigureWidth
        }
    },
    mounted() {
			document.addEventListener('pointermove', this.drag, { passive: false })
			document.addEventListener('pointerup', this.endDrag)
				
    },
    methods: {
        convertDOMtoSVG(x, y) {
            try {
                const pt = new DOMPoint(x, y)
	            const svgP = pt.matrixTransform(this.$refs['svg'].getScreenCTM().inverse())
                return {x: svgP.x, y: svgP.y}
            }
            catch(e) {
                return false
            }
        },
        inAllowedArea(targetX, targetY) { // if target object in allowed aarea
            if (targetX < 0 || targetX > window.innerWidth)
                return false
            if (targetY < 0 || targetY > window.innerHeight)
                return false
            return true
        },
        autoscroll(targetX, targetY) {
            // const targetX = window.event.clientX
            // const targetY = window.event.clientY
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
			inRect(x, y, rect) {
				if (x === undefined || y === undefined)
					return false;
				if (x > rect.right || x < rect.left) {
					return false;
				}
				if (y > rect.bottom || y < rect.top) {
					return false;
				}
				return true;
        },
        moveAt(x, y, event) {
            const newCursorCoordinates = this.convertDOMtoSVG(x, y)
            if (!newCursorCoordinates)
                return
            this.autoscroll(x, y)
            this.$set(this.target, 'x', newCursorCoordinates.x - this.dragFigureWidth / 2)
					this.$set(this.target, 'y', newCursorCoordinates.y - this.dragFigureHeight / 2)
						console.log("herrrrr")
					if (!this.inAllowedArea(x, y)) {
						console.log("not in allowed area!");
                this.endDrag(event)
            }
        },
			startDrag(type, event, fromRow = undefined, fromColumn = undefined) {
				console.log('start drag');
            if (fromRow !==undefined && fromColumn !== undefined) {
                if (this.boardArrayConfiguration[fromRow][fromColumn].moveStatus === 'passive') {
                    return
                }
            }
            let x, y
				if (event.changedTouches) {
					console.log("touches");
					console.log(event.type);
                event.preventDefault()
                x = event.changedTouches[0].clientX
                y = event.changedTouches[0].clientY
            }
            else {
                x = event.clientX
                y = event.clientY
            }
            this.$set(this.target, 'type', type)
            if (fromRow !== undefined && fromColumn !== undefined) {
                let currentConfig = this.boardArrayConfiguration
                currentConfig[fromRow][fromColumn].type = ''
                currentConfig[fromRow][fromColumn].moveStatus = ''
                this.$emit('updateConfig', currentConfig)
            }
				this.moveAt(x, y, event)
						console.log("moved!")
            this.dragMode = true
        },
			drag(event) {
					console.log("drag!")
            if (!this.dragMode) {
                return
            }
            if (this.target.type === undefined)
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
            this.moveAt(x, y, event)
        },
        endDrag(event) {
					if (!this.dragMode) {
						return;
					}
					let x, y;
					if (event.touches) {
						event.preventDefault()
						x = event.changedTouches[0].clientX
						y = event.changedTouches[0].clientY
					}
					else {
						x = event.clientX
						y = event.clientY
					}
            const boardItems = document.querySelectorAll('.item')
            let backToDragZone = true
            for (const boardItem of boardItems) {
							const itemRect = boardItem.getBoundingClientRect()
							const rowIndex = boardItem.getAttribute('row')
              const columnIndex = boardItem.getAttribute('column')
                if (this.inRect(x, y, itemRect)) {
                    
                    const currentConfig = this.boardArrayConfiguration
                    if (currentConfig[rowIndex][columnIndex].moveStatus === 'passive' || currentConfig[rowIndex][columnIndex].moveStatus === 'active') {
                        break;
                    }
                    currentConfig[rowIndex][columnIndex].type = this.target.type
                    currentConfig[rowIndex][columnIndex].moveStatus = 'active'
                    backToDragZone = false
                    this.$emit('updateConfig', currentConfig)
                    break;
                }
            }
            if (backToDragZone) {
                console.log('here!')
                for(let index = 0; index < this.dragFigures.length; index++) {
                    if (this.dragFigures[index].type === this.target.type) {
                        this.$emit('updateFiguresAmount', {index, amount: this.dragFigures[index].amount + 1})
                    }
                }
            }
            this.dragMode = false
        },
        moveFromDragZone(type, index, event) {
            console.log(index, this.dragFigures[index])
            if (this.dragFigures[index].amount > 0) {
                console.log('update amount')
                this.$emit('updateFiguresAmount', {index, amount: this.dragFigures[index].amount - 1})
                this.startDrag(type, event)
            }
			},
			moveFromBoard(type, event, fromRow, fromColumn) {
				this.startDrag(type, event, fromRow, fromColumn)
			}
    }
}
</script>

<style scoped>
.dragFigure.active{
    cursor: grab;
}
.targeted {
    cursor: grabbing;
}
</style>