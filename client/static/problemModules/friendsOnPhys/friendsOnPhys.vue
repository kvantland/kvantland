<template>
    <svg version="1.1" ref="svg" class="display_svg" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
            preserveAspectRatio="xMidYMid meet" 
            overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <g class="drag_container">
                <g class="content" :transform="`translate(0 ${containerHeaderHeight + containerHeaderMarginBottom})`">
                    <rect class="drag_container" :width="dragAreaWidth" :height="dragAreaHeight" x="0" y="0" fill="lightgrey" />
                    <g class="rows" :transform="`translate(0 ${weightGap})`">
                        <g v-for="(row, rowNum) in rows" class="row" :transform="`translate(${weightGap} ${(weightGap + weightWidth) * rowNum})`">
                            <g v-for="(weight, weightNum) in inRow" 
                                :transform="`translate(${weightCoordinates[weightNum + rowNum * inRow].x} ${weightCoordinates[weightNum + rowNum * inRow].y})`">
                                <g v-if="startAreaWeights[weightNum + rowNum * inRow]" 
                                @touchstart="moveFromStartArea(weightNum + rowNum * inRow, $event.touches[0])" 
                                @mousedown="moveFromStartArea(weightNum + rowNum * inRow, $event)"
                                :class="`weight weight_${weightNum + rowNum * inRow}`">
                                    <image x="0" y="0" :height="weightHeight" :width="weightWidth" href="/icons/weight.svg" />
                                    <text class="name" :x="weightWidth / 2" :y="weightHeight / 2 + nameYPad"> {{ names[weightNum + rowNum * inRow] }} </text>
                                </g>
                                <g class="board" :transform="`translate(0 ${weightHeight})`">
                                    <image class="board" x="0" y="0" :width="boardWidth" :height="boardHeight" href="/new-problem_assets/board.svg" />
                                    <text class="boardName" :x="boardWidth / 2" :y="boardHeight / 2" dy="0.35em"> {{ boardNames[weightNum + rowNum * inRow] }} </text>
                                </g>
                            </g>
                        </g>
                    </g>
                </g>
            </g>
            <g class="answer_container" :transform="`translate(${containersGap + dragAreaWidth} 0)`" ref="ans_container">
                <g :transform="`translate(0 ${containerHeaderHeight + containerHeaderMarginBottom })`">
                    <rect class="answer_container" x="0" y="0" :width="answerAreaWidth" :height="answerAreaHeight" fill="lightgrey" />
                    <g :transform="`translate(${weightWidth / 2 + weightGap} ${weightHeight / 2 + weightGap})`">
                        <g class="weight" v-for="(weight, weightNum) in answerAreaWeights" @mousedown="moveFromAnsArea(weight)" @touchstart="moveFromAnsArea(weight)"
                            :transform="`translate(0 ${(weightGap + weightHeight) * weightNum})`" v-html="weight.html" />
                    </g>
                </g>
            </g>
        <g  v-if="dragMode" class="choiced" :transform="`translate(${targetWeight.x} ${targetWeight.y})`" ref="choiced">
            <image :x="-weightWidth / 2" :y="-weightHeight / 2" :height="weightHeight" :width="weightWidth" href="/new-problem_assets/weight.svg" />
            <text class="name" x="0" :y="nameYPad"> {{ names[targetWeight.index] }} </text>
        </g>
    </svg>
</template>

<script>
export default {
    props: ['problemParams', 'xhrData', 'newXhr'],
    model: {
        prop: 'answer',
        event: 'updateAnswer'
    },
    data() {
        return {
            cursorX: 0,
            cursorY: 0,
            weightCoordinates: [], //not important, declared in methods
            boardNames: ['Алёша', 'Боря', 'Вася', 'Гриша'],
            names: [1, 2, 3, 4],
            nameYPad: 17,
            boardHeight: 30,
            dragAreaMarginTop: 30,
            inRow: 2,
            rows: 2,
            weightGap: 15,
            weightHeight: 65,
            weightWidth: 65,
            containerHeaderHeight: 30,
            containerHeaderMarginBottom: 5,
            containersGap: 20, //distance between containers in svg
            dropAllowDistance: 70, //svg distance
            targetWeight: {x: 0, y:0, index: undefined}, //current dragging object

            startAreaWeights: {},   
            answerAreaWeights: [],
            cupWeights: {'left': [], 'right': []},

            newSide: 'equal',
            weightMode: false,
            dragMode: false, //is drag?
        }
    },
    computed: {
        boardWidth() {
            return this.weightWidth
        },
        weightingHistory() {
            if (!this.problemParams.history)
                return []
            return this.problemParams.history
        },
        dragAreaWidth() {
            return this.inRow * (this.weightWidth + this.weightGap) + this.weightGap
        },
        dragAreaHeight() {
            return this.rows * (this.weightHeight + this.weightGap + this.boardHeight) + this.weightGap
        },
        answerAreaWidth() {
            return this.weightGap * 2 + this.weightWidth
        },
        answerAreaHeight(){
            return this.weightGap * 3 + this.weightWidth * 2
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
            this.$set(this.targetWeight, 'x', newCursorCoordinates.x)
            this.$set(this.targetWeight, 'y', newCursorCoordinates.y)
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
            this.$set(this.targetWeight, 'index', index)
            this.moveAt(x, y)
        },
        drag(event) {
            if (!this.dragMode) {
                return
            }
            if (this.targetWeight.index == undefined)
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
            if (this.answerAreaWeights.length >= 2) {
                return
            }
            let newAnswerAreaWeights = JSON.parse(JSON.stringify(this.answerAreaWeights))
            newAnswerAreaWeights.push({
                index: this.targetWeight.index,
                html: this.$refs.choiced.innerHTML
            })
            console.log(newAnswerAreaWeights)
            this.answerAreaWeights = newAnswerAreaWeights
            let newAnswerAreaWeightsIndex = []
            for (const weight of newAnswerAreaWeights) {
                newAnswerAreaWeightsIndex.push(weight.index)
            }
            this.$emit('updateAnswer', newAnswerAreaWeightsIndex)
        },
        backToStartArea() {
            const dragIndex = this.targetWeight.index
            this.startAreaWeights[dragIndex] = true
        },
        moveFromStartArea(index, event) {
            this.$set(this.startAreaWeights, index, false)
            this.startDrag(index, event)
        },
        moveFromAnsArea(weight) {
            console.log(weight)
            let newAnswerAreaWeights = []
            for (const answerWeight of this.answerAreaWeights) {
                console.log(answerWeight.index, weight.index)
                if (answerWeight.index != weight.index) {
                    newAnswerAreaWeights.push(answerWeight)
                }
            }
            this.answerAreaWeights = newAnswerAreaWeights
            this.startDrag(weight.index, window.event)
        }
    },
    created() {
        let coordinates = []
        let startWeights = {}
        for (let row = 1; row <= this.rows; row++) {
            for (let column = 1; column <= this.inRow; column++) {
                coordinates.push({x: (column - 1) * (this.weightGap + this.weightWidth), y: this.boardHeight * (row - 1)})
                startWeights[(column - 1) + this.inRow * (row - 1)] = true
            }
        }
        this.weightCoordinates = coordinates
        this.startAreaWeights = startWeights
    },
    mounted() {
        document.addEventListener('mousemove', this.drag, {passive: false})
        document.addEventListener('touchmove', this.drag, {passive: false})
        document.addEventListener('touchend', this.endDrag)
        document.addEventListener('mouseup', this.endDrag)
    }
}
</script>
