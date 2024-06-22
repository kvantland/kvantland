<template>
    <svg version="1.1" overflow="visible" ref="svg"
        preserveAspectRatio="xMidYMid meet" 
        :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
        xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <g class="board">
            <g class="row" v-for="(row, rowIndex) in boardSide" :transform="`translate(0 ${rowIndex * boardItemSide})`">
                <g class="item" v-for="(column, columnIndex) in boardSide" :transform="`translate(${columnIndex * boardItemSide} 0)`">
                    
                    <rect v-if="(rowIndex + columnIndex) % 2 == 0" fill="white" stroke="black" :width="boardItemSide" :height="boardItemSide" x="0" y="0" />
                    <rect v-else fill="orange" stroke="black" :width="boardItemSide" :height="boardItemSide" x="0" y="0" />
                </g>
            </g>
        </g>
        <g class="interactiveZone" :transform="`translate(${boardWidth + gap} 0)`">
            <g v-for="(dragFigure, dragFigureIndex) in dragFigures" 
                :transform="`translate(0 ${(dragFigureHeight + dragFigureTextHeight) * dragFigureIndex})`">
                <template v-if="dragFigure.amount != 'inf'">
                    <image class="dragFigure" :width="dragFigureWidth" 
                        :height="dragFigureHeight" x="0" y="0" :href="`/problem_assets/chess/${dragFigure.type}.png`"/>
                    <text v-if="dragFigure.amount != 'inf'" style="font-size: 11px; font-weight: 600;" :transform="`translate(0 ${dragFigureHeight})`"> Осталось: {{ dragFigure.amount }} </text>
                </template>
                <image v-else class="dragFigure" :width="dragFigureWidth" 
                    :height="dragFigureHeight" :x="figureMarginTop" 
                    @touchstart="startDrag(dragFigure.type, $event)" 
                    @mousedown="startDrag(dragFigure.type, $event)"
                    :y="figureMarginTop" :href="`/problem_assets/chess/${dragFigure.type}.png`" />
            </g>
        </g>
        <image v-if="target.type" class="targeted" :href="`/problem_assets/chess/${target.type}.png`" 
            :x="target.x - dragFigureWidth / 2" :y="target.y - dragFigureHeight / 2"
            :width="dragFigureWidth" :height="dragFigureHeight"  />
    </svg>
</template>

<script>
export default {
    props: {
        boardSide: {default: 8},
        boardItemSide: {default: 60},
        startConfiguration: {default: 'empty'},
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
    watch: {
        dragFigures(newValue) {
            console.log(newValue)
        }
    },
    computed: {
        startBoardConfiguration() {
            let configuration = []
            if (this.startConfiguration === 'empty') {
                for (let row = 0; row < this.boardSide; row++) {
                    configuration.push([])
                    for (let column = 0; column < boardSide; column++) {
                        configuration[row].push('')
                    }
                }
            }
            else {
                return this.startConfiguration
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
        inAllowedArea() { // if target object in allowed aarea
            const targetX = window.event.clientX
            const targetY = window.event.clientY
            console.log(targetX, targetY)
            if (targetX < 0 || targetX > window.innerWidth)
                return false
            if (targetY < 0 || targetY > window.innerHeight)
                return false
            return true
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
            const newCursorCoordinates = this.convertDOMtoSVG(x, y)
            if (!newCursorCoordinates)
                return
            this.autoscroll()
            this.$set(this.target, 'x', newCursorCoordinates.x)
            this.$set(this.target, 'y', newCursorCoordinates.y)
            if (!this.inAllowedArea()) {
                this.endDrag()
            }
        },
        startDrag(type, event) {
            let x, y
            if (event.touches) {
                x = event.touches[0].clientX
                y = event.touches[0].clientY
            }
            else {
                x = event.clientX
                y = event.clientY
            }
            this.dragMode = true
            this.$set(this.target, 'type', type)
            this.moveAt(x, y)
        },
        drag(event) {
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
            this.moveAt(x, y)
        },
        endDrag() {
            if (!this.dragMode) {
                return
            }
            const boardItems = document.querySelectorAll('.item')
            let num = 0
            for (let boardItem of boardItems) {
                const itemRect = boardItem.getBoundingClientRect()
                //console.log(itemRect)
                if (this.inRect(window.event.x, window.event.y, itemRect)) {
                    console.log(itemRect, num)
                    this.$set(this.target, 'x', boardItem.getAttribute('x'))
                    this.$set(this.target, 'y', boardItem.getAttribute('y'))
                    break;
                }
                num++
            }
            this.dragMode = false
        }
    },
    mounted() {
        document.addEventListener('mousemove', this.drag, {passive: false})
        document.addEventListener('touchmove', this.drag, {passive: false})
        document.addEventListener('touchend', this.endDrag)
        document.addEventListener('mouseup', this.endDrag)
    }
}
</script>

<style scoped>
.dragFigure {
    cursor: grab;
}
.targeted {
    cursor: grabbing;
}
</style>