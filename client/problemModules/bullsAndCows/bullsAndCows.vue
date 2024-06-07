<template>
    <div class="plot_area">
    <svg version="1.1" :width="`${boardWidth + (animalInRow - 2)* side + animalColumnInd}`" 
        :height="`${boardHeight}`" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <g class="board">
            <line class="horizontal" v-for="(line, num) in rectInColumn  + 1" 
                x1="0" :y1="`${side * num}`" :x2="`${rectInRow * side}`" :y2="`${side * num}`" :stroke-width="lineWidth" />
            <line class="vertical" v-for="(line, num) in rectInRow + 1"
                :x1="`${side * num}`" y1="0" :x2="`${side * num}`" :y2="`${rectInColumn * side}`" :stroke-width="lineWidth" />
            <g v-for="(rect_row, yInd) in rectInColumn" :key="`row_${yInd}`">
                <rect :class="{ 'field': true, 'questionField': problemParams.start_board[yInd][xInd] === '?' }" v-for="(rect, xInd) in rectInRow"
                    :x="`${xInd * side + rectInd}`" :y="`${yInd * side + rectInd}`" :width="innerSide" :height="innerSide" :key="`rect_${xInd}_${yInd}`"/>
                <text v-for="(perimeterValue, xInd) in problemParams.start_board[yInd]" :x="`${xInd * side + rectInd + side / 2}`" 
                    :y="`${yInd * side + rectInd + side / 2}`"> {{ perimeterValue }} </text>
            </g>
        </g>
        <g class="animals" :transform="`translate(${boardWidth + animalInd} ${side / 2})`">
            <g class="animalColumns" v-for="(column, yind) in animalInColumn" 
                :transform="`translate(0 ${yind * side + side / 2})`">
                <image v-for="(animal, xind) in animalInRow" :href="problemParams.cows_and_bulls[yind][xind] !== '' ? getImageHref(problemParams.cows_and_bulls[yind][xind]) : null" :class="`animal_${problemParams.cows_and_bulls[yind][xind]}`" :x="`${xind * side + animalColumnInd - side / 2}`" :width="side"/>
            </g>
        </g>
    </svg>
    </div>
</template>

<script>
export default {
    props: ["problemParams"],
    data() {
        const rectInRow = this.problemParams['start_board'][0].length
        const rectInColumn = this.problemParams['start_board'].length
        const animalInRow = this.problemParams['cows_and_bulls'][0].length
        const animalInColumn = this.problemParams['cows_and_bulls'].length
        return {
            rectInColumn: rectInColumn,
            rectInRow: rectInRow,
            animalInRow: animalInRow,
            animalInColumn: animalInColumn,
            side: 80,
            lineWidth: 2,
            animalInd: 40,
            animalColumnInd: 10,
        }
    },

    methods: {
        getImageHref(animal) {
            const imagePathMap = {
                b: '/problem_assets/bulls_and_cows/bull.png',
                c: '/problem_assets/bulls_and_cows/cow.png',
            };

            return imagePathMap[animal];
        }
    },

    computed: {
        boardWidth() {
            return this.rectInRow * this.side
        },
        boardHeight() {
            return this.rectInColumn * this.side + this.lineWidth
        },
        innerSide(){
            return this.side - this.lineWidth
        },
        rectInd() {
            return this.lineWidth / 2
        },
    },
    mounted() {
        console.log(this.colors)
    }
}
</script>

<style scoped>

.plot_area {
    margin-top: 50px;
    width: 100%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
} 

line {
    stroke: black;
	stroke-linecap: round;
}

.field {
    fill: white;
}

.questionField {
    fill: grey;
}

text {
    font-size: 40px;
    dominant-baseline: central;
    text-anchor: middle;
    pointer-events: none;
}
</style>