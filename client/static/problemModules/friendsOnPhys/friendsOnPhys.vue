<template>
    <svg version="1.1" ref="svg" class="display_svg" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
            preserveAspectRatio="xMidYMid meet" 
            overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <g class="drag_container">
                <g class="content" :transform="`translate(0 ${containerHeaderHeight + containerHeaderMarginBottom})`">
                    <rect class="drag_container" :width="dragAreaWidth" :height="dragAreaHeight" x="0" y="0" fill="lightgrey" />
                    <g class="rows" :transform="`translate(0 ${boyGap})`">
                        <g v-for="(row, rowNum) in rows" class="row" :transform="`translate(${boyGap} ${(boyGap + boyWidth) * rowNum})`">
                            <g v-for="(boy, boyNum) in inRow" 
                                :transform="`translate(${boyCoordinates[boyNum + rowNum * inRow].x} ${boyCoordinates[boyNum + rowNum * inRow].y})`">
                                <g v-if="startAreaBoys[boyNum + rowNum * inRow]" 
                                @touchstart="moveFromStartArea(boyNum + rowNum * inRow, $event.touches[0])" 
                                @mousedown="moveFromStartArea(boyNum + rowNum * inRow, $event)"
                                :class="`boy boy_${boyNum + rowNum * inRow}`">
                                    <image x="0" y="0" :height="boyHeight" :width="boyWidth" :href="`/new-problem_assets/friend_on_phys/boy${boyNum + rowNum * inRow + 1}.png`" />
                                    <g class="board" :transform="`translate(0 ${boyHeight})`">
                                        <image class="board" x="0" y="0" :width="boardWidth" :height="boardHeight" href="/new-problem_assets/board.svg" />
                                        <text class="boardName" :x="boardWidth / 2" :y="boardHeight / 2" dy="0.35em"> {{ boardNames[boyNum + rowNum * inRow] }} </text>
                                    </g>
                                </g>
                            </g>
                        </g>
                    </g>
                </g>
            </g>
            <g class="answer_container" :transform="`translate(${containersGap + dragAreaWidth} 0)`" ref="ans_container">
                <g :transform="`translate(0 ${containerHeaderHeight + containerHeaderMarginBottom })`">
                    <rect class="answer_container" x="0" y="0" :width="answerAreaWidth" :height="answerAreaHeight" fill="lightgrey" />
                    <g :transform="`translate(${boyWidth / 2 + boyGap} ${boyHeight / 2 + boyGap})`">
                        <g class="boy" v-for="(boy, boyNum) in answerAreaBoys" @mousedown="moveFromAnsArea(boy)" @touchstart="moveFromAnsArea(boy)"
                            :transform="`translate(0 ${(boyGap + boyHeight) * boyNum})`" v-html="boy.html" />
                    </g>
                </g>
            </g>
        <g  v-if="dragMode" class="choiced" :transform="`translate(${targetBoy.x} ${targetBoy.y})`" ref="choiced">           
            <image :x="-boyWidth / 2" :y="-boyHeight / 2" :height="boyHeight" :width="boyWidth" :href="`/new-problem_assets/friend_on_phys/boy${targetBoy.index+1}.png`" />
            <g class="board" :transform="`translate(${-boyWidth / 2} ${boyHeight / 2})`">
                <image class="board" x="0" y="0" :width="boardWidth" :height="boardHeight" href="/new-problem_assets/board.svg" />
                <text class="boardName" :x="boardWidth / 2" :y="boardHeight / 2" dy="0.35em"> {{ boardNames[targetBoy.index] }} </text>
            </g>
        </g>
    </svg>
</template>

<script>
export default {
    props: ['problemParams'],
    model: {
        prop: 'answer',
        event: 'updateAnswer'
    },
    data() {
        return {
            cursorX: 0,
            cursorY: 0,
            boyCoordinates: [], 
            boardNames: ['Алёша', 'Боря', 'Вася', 'Гриша'],
            names: [1, 2, 3, 4],
            nameYPad: 17,
            boardHeight: 30,
            dragAreaMarginTop: 30,
            inRow: 2,
            rows: 2,
            boyGap: 15,
            boyHeight: 65,
            boyWidth: 65,
            containerHeaderHeight: 30,
            containerHeaderMarginBottom: 5,
            containersGap: 20,
            dropAllowDistance: 70,
            targetBoy: {x: 0, y:0, index: undefined},

            startAreaBoys: {},   
            answerAreaBoys: [],

            newSide: 'equal',
            weightMode: false,
            dragMode: false, //is drag?
        }
    },
    computed: {
        boardWidth() {
            return this.boyWidth
        },
        weightingHistory() {
            if (!this.problemParams.history)
                return []
            return this.problemParams.history
        },
        dragAreaWidth() {
            return this.inRow * (this.boyWidth + this.boyGap) + this.boyGap
        },
        dragAreaHeight() {
            return this.rows * (this.boyHeight + this.boyGap + this.boardHeight) + this.boyGap
        },
        answerAreaWidth() {
            return this.boyGap * 2 + this.boyWidth
        },
        answerAreaHeight(){
            return this.boyGap * 3 + this.boyWidth * 2
        },
        containersAreaWidth() {
            return this.dragAreaWidth + this.answerAreaWidth + this.containersGap
        },
        svgHeight() {
            return this.dragAreaHeight + this.dragAreaMarginTop + this.containerHeaderHeight + this.containerHeaderMarginBottom
        },
        svgWidth() {
            return this.dragAreaWidth
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
        stopWeight(currentSide) {
            this.weightMode = false
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
            this.$set(this.targetBoy, 'x', newCursorCoordinates.x)
            this.$set(this.targetBoy, 'y', newCursorCoordinates.y)
            if (!this.inAllowedArea()) {
                this.endDrag()
            }
        },
        startDrag(index, event) {
            let x, y
            console.log(index)
            if (event.touches) {
                x = event.touches[0].clientX
                y = event.touches[0].clientY
            }
            else {
                x = event.clientX
                y = event.clientY
            }
            this.dragMode = true
            this.$set(this.targetBoy, 'index', index)
            this.moveAt(x, y)
        },
        drag(event) {
            if (!this.dragMode) {
                return
            }
            if (this.targetBoy.index == undefined)
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
            const AnsContainerRect = this.$refs['ans_container'].getBoundingClientRect()
            if (this.inRect(window.event.x, window.event.y, AnsContainerRect)) {
                console.log('drop to ans area')
                this.dropToAnsArea()
            }
            else {
                console.log('drop to drag area')
                this.backToStartArea()
            }
            this.dragMode = false
        },
        dropToAnsArea() {
            let newanswerAreaBoys = JSON.parse(JSON.stringify(this.answerAreaBoys))
            newanswerAreaBoys.push({
                index: this.targetBoy.index,
                html: this.$refs.choiced.innerHTML
            })
            console.log(newanswerAreaBoys)
            this.answerAreaBoys = newanswerAreaBoys
            let newanswerAreaBoysIndex = []
            for (const boy of newanswerAreaBoys) {
                newanswerAreaBoysIndex.push(boy.index)
            }
            this.$emit('updateAnswer', newanswerAreaBoysIndex)
        },
        backToStartArea() {
            const dragIndex = this.targetBoy.index
            this.startAreaBoys[dragIndex] = true
        },
        moveFromStartArea(index, event) {
            this.$set(this.startAreaBoys, index, false)
            this.startDrag(index, event)
        },
        moveFromAnsArea(boy) {
            console.log(boy)
            let newanswerAreaBoys = []
            for (const answerBoy of this.answerAreaBoys) {
                console.log(answerBoy.index, boy.index)
                if (answerBoy.index != boy.index) {
                    newanswerAreaBoys.push(answerBoy)
                }
            }
            this.answerAreaBoys = newanswerAreaBoys
            this.startDrag(boy.index, window.event)
        }
    },
    created() {
        let coordinates = []
        let startBoys = {}
        for (let row = 1; row <= this.rows; row++) {
            for (let column = 1; column <= this.inRow; column++) {
                coordinates.push({x: (column - 1) * (this.boyGap + this.boyWidth), y: this.boardHeight * (row - 1)})
                startBoys[(column - 1) + this.inRow * (row - 1)] = true
            }
        }
        this.boyCoordinates = coordinates
        this.startAreaBoys = startBoys
    },
    mounted() {
        document.addEventListener('mousemove', this.drag, {passive: false})
        document.addEventListener('touchmove', this.drag, {passive: false})
        document.addEventListener('touchend', this.endDrag)
        document.addEventListener('mouseup', this.endDrag)
    }
}
</script>
