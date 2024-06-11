<template>
    <div class="svg_with_buttons">
    <svg version="1.1" ref="svg" class="display_svg" :viewBox="`0 0 ${svgWidth} ${svgHeight}`" 
            :width="svgWidth" :height="svgHeight"
            overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <Scales @svgHeight="getSvgHeight" @svgWidth="getSvgWidth" @moveFromCup="moveFromCup" :scale="0.8" 
            :leftCupObjects="cupWeights.left" :rightCupObjects="cupWeights.right" />
        <g class="containers" :transform="`translate(${(scalesWidth - containersAreaWidth) / 2} ${scalesHeight + dragAreaMarginTop})`">
            <g class="drag_container">
                <rect class="drag_container" :width="dragAreaWidth" :height="dragAreaHeight" x="0" y="0" fill="lightgrey" />
                <g class="rows" :transform="`translate(0 ${weightGap})`">
                    <g v-for="(row, rowNum) in rows" class="row" :transform="`translate(${weightGap} ${(weightGap + weightWidth) * rowNum})`">
                        <image v-for="(weight, weightNum) in inRow" 
                            v-if="startAreaWeights[weightNum + rowNum * inRow]"
                            :x="weightCoordinates[weightNum + rowNum * inRow].x" 
                            :y="weightCoordinates[weightNum + rowNum * inRow].y" 
                            @touchstart="moveFromStartArea(weightNum + rowNum * inRow, $event.touches[0])" 
                            @mousedown="moveFromStartArea(weightNum + rowNum * inRow, $event)"
                            :class="`weight weight_${weightNum + rowNum * inRow}`" 
                            :height="weightHeight" :width="weightWidth" 
                            href="/icons/weight.svg" />
                    </g>
                </g>
            </g>
            <g class="answer_container" :transform="`translate(${containersGap + dragAreaWidth} 0)`" ref="ans_container">
                <rect class="answer_container" x="0" y="0" :width="answerAreaWidth" :height="answerAreaHeight" fill="lightgrey" />
                <g :transform="`translate(${weightWidth / 2 + weightGap} ${weightHeight / 2 + weightGap})`">
                    <g class="weight" v-for="(weight, weightNum) in answerAreaWeights" @mousedown="moveFromAnsArea(weight)" @touchstart="moveFromAnsArea(weight)"
                        :transform="`translate(0 ${(weightGap + weightHeight) * weightNum})`" v-html="weight.html" />
                </g>
            </g>
        </g>
        <g class="choiced" :transform="`translate(${targetWeight.x} ${targetWeight.y})`" ref="choiced">
            <image v-if="dragMode" :x="-weightWidth / 2" :y="-weightHeight / 2" :height="weightHeight" :width="weightWidth" href="/icons/weight.svg" />
        </g>
    </svg>
    <div class="buttons">
        <button class="weight_button"> Взвесить </button>
        <button class="clear_button" @click="clearScales"> Очистить весы </button>
        <div class="remaining_weightings"> Осталось взвешиваний: {{ problemParams.weightings_amount }}</div>
        <div class="history" v-if="weightingHistory.length">
            <p v-for="item in weightingHistory"> {{ item }} </p>
        </div>
    </div>
    </div>
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
            svgX: 0,
            svgY: 0,
            svgHeight: 0,
            svgWidth: 0,
            scalesHeight: 0,
            scalesWidth: 0,
            cupCoordinates: {},
            weightCoordinates: [], //not important, declared in methods and mounted

            dragAreaMarginTop: 30,
            inRow: 5,
            rows: 2,
            weightGap: 15,
            weightHeight: 65,
            weightWidth: 65,
            containersGap: 20, //distance between containers in svg
            dropAllowDistance: 70, //svg distance
            
            targetWeight: {x: 0, y:0, index: undefined}, //current dragging object

            startAreaWeights: {},   
            answerAreaWeights: [],
            cupWeights: {'left': [], 'right': []},

            dragMode: false, //is drag?
        }
    },
    computed: {
        weightingHistory() {
            if (!this.problemParams.history)
                return []
            return this.problemParams.history
        },
        dragAreaWidth() {
            return this.inRow * (this.weightWidth + this.weightGap) + this.weightGap
        },
        dragAreaHeight() {
            return this.rows * (this.weightHeight + this.weightGap) + this.weightGap
        },
        answerAreaWidth() {
            return this.weightGap * 2 + this.weightWidth
        },
        answerAreaHeight(){
            return this.weightGap * 3 + this.weightWidth * 2
        },
        containersAreaWidth() {
            return this.dragAreaWidth + this.answerAreaWidth + this.containersGap
        }
    },
    methods: {
        getSvgHeight(scalesHeight) {
            this.svgHeight = scalesHeight + this.dragAreaHeight + this.dragAreaMarginTop
            this.scalesHeight = scalesHeight
        },
        getSvgWidth(scalesWidth) {
            this.scalesWidth = scalesWidth
            this.svgWidth = Math.max(scalesWidth, this.dragAreaWidth)
        },
        clearScales() {
            this.dragMode = false
            this.$set(this.cupWeights, 'left', [])
            this.$set(this.cupWeights, 'right', [])
            for (let weight in this.startAreaWeights) {
                this.$set(this.startAreaWeights, weight, true)
            }
        },
        inRect(x, y, rect){
            if (x + this.svgX > rect.right || x + this.svgX < rect.left) {
                return false
            }
            if (y + this.svgY > rect.bottom || y + this.svgY < rect.top) {
                return false
            }
            return true
        },
        moveAt(x, y) {
            this.$set(this.targetWeight, 'x', x - this.svgX),
            this.$set(this.targetWeight, 'y', y - this.svgY)
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
            let cupToDrop = undefined
            let minDist = 10 ** 18
            for (const [cup, cupCoordinates] of Object.entries(this.cupCoordinates)) {
                const xDiff = Math.abs(cupCoordinates.x - this.targetWeight.x)
                const yDiff = Math.abs(cupCoordinates.y - this.targetWeight.y)
                const dist = Math.sqrt(xDiff ** 2 + yDiff ** 2)
                if (dist < minDist) {
                    minDist = dist
                    if (dist < this.dropAllowDistance) {
                        cupToDrop = cup
                    }
                }
            }
            const AnsContainerRect = this.$refs['ans_container'].getBoundingClientRect()
            if (this.inRect(this.targetWeight.x, this.targetWeight.y, AnsContainerRect)) {
                console.log('drop to ans area')
                this.dropToAnsArea()
            }

            else if(cupToDrop) {
                console.log('drop to cup')
                this.dropToCup(cupToDrop)
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
        },
        backToStartArea() {
            const dragIndex = this.targetWeight.index
            this.startAreaWeights[dragIndex] = true
        },
        dropToCup(cup) {
            let curCupWeights = this.cupWeights[cup]
            curCupWeights.push({
                html: this.$refs['choiced'].innerHTML, 
                payload: {index: this.targetWeight.index}
            })
            this.$set(this.cupWeights, cup, curCupWeights)
        },
        moveFromStartArea(index, event) {
            this.$set(this.startAreaWeights, index, false)
            this.startDrag(index, event)
        },
        moveFromCup(data) {
            const index = data.payload.index
            const cup = data.cup
            let newCupWeights = []
            for (const weightInfo of this.cupWeights[cup]) {
                if (weightInfo.payload.index != index) {
                    newCupWeights.push(weightInfo)
                }
            }
            this.$set(this.cupWeights, cup, newCupWeights)
            this.startDrag(index, window.event)
        },
        moveFromAnsArea(weight) {
            console.log(weight)
            let newAnswerAreaWeights = []
            for (const answerWeight of this.answerAreaWeights) {
                console.log(answerWeight.index, weight.index)
                if (answerWeight.index != weight.index) {
                    console.log('not equal!')
                    newAnswerAreaWeights.push(answerWeight)
                }
            }
            console.log('new answer area weights: ', newAnswerAreaWeights)
            this.answerAreaWeights = newAnswerAreaWeights
            this.startDrag(weight.index, window.event)
        }
    },
    created() {
        let coordinates = []
        let startWeights = {}
        for (let row = 1; row <= this.rows; row++) {
            for (let column = 1; column <= this.inRow; column++) {
                coordinates.push({x: (column - 1) * (this.weightGap + this.weightWidth), y: 0})
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
        document.addEventListener('DOMContentLoaded', function(){
            const svgRect = this.$refs['svg'].getBoundingClientRect()
            const svgX = svgRect.left
            const svgY = svgRect.top

            const cupCoordinates = {
                left: {x: 0, y: 0},
                right: {x: 0, y: 0},
            }
            const leftCupRect = document.querySelector('.left_cup').getBoundingClientRect()
            const rightCupRect = document.querySelector('.right_cup').getBoundingClientRect()
            cupCoordinates.left.x = leftCupRect.left + leftCupRect.width / 2 - svgX
            cupCoordinates.left.y = leftCupRect.top + leftCupRect.height / 2 - svgY
            cupCoordinates.right.x = rightCupRect.left + rightCupRect.width / 2 - svgX
            cupCoordinates.right.y = rightCupRect.top + rightCupRect.height / 2 - svgY
            console.log(cupCoordinates.left, cupCoordinates.right)
            console.log(cupCoordinates)
            this.cupCoordinates = cupCoordinates
            this.svgX = svgX
            this.svgY = svgY
            console.log(this.svgX)
        }.bind(this))
    }
}
</script>
