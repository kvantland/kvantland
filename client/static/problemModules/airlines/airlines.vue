<template>
    <svg version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`" preserveAspectRatio="xMidYMid meet"  overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <defs>
            <clipPath id="city_border">
                <path d="
                    M -30 0
                    a 30 30 0 0 0 30 30 
                    a 30 30 0 0 0 30 -30
                    a 30 30 0 0 0 -30 -30
                    a 30 30 0 0 0 -30 30
                    z" />
            </clipPath>
        </defs>
        <line v-for="(line, index) in lines" :key="`line_${index}`"
                :x1="points[line.point1].x" :y1="points[line.point1].y"
                :x2="points[line.point2].x" :y2="points[line.point2].y"
                stroke="black" stroke-width="20px" class="lines"/>
        <g v-for="(point, index) in points" :key="`city_${index}`" :class="`city city_${index}`" :transform="`translate(${point.x} ${point.y})`" @click="handleCircleClick(index)">
            <image :href="`/new-problem_assets/airlines/city${index % 3}.png`" :x="cityImgX" :y ="cityImgY" :width="cityImgWidth" clip-path="url(#city_border)"/>
            <circle :r="point.r" :color="selectedPoints.includes(index) ? 'green': 'black'" class="circles"/>
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
            svgWidth: 400,
            svgHeight: 400,
            cityImgX: -40,
            cityImgY: -40,
            cityImgWidth: 80,
            minCircleCenter: { x: 200, y: 200 }, 
            mainCircleRadius: 150,
            radius: 30,
            selectedPoints: [],
            lines: [],
            ans: [],
        }
    },
    computed: {
        points() {
            const angleIncrement = (2 * Math.PI) / this.amount;
            let points = []
            for (let i = 0; i < this.amount; i++) {
                const angle = i * angleIncrement;
                const x = this.minCircleCenter.x + this.mainCircleRadius * Math.cos(angle);
                const y = this.minCircleCenter.y + this.mainCircleRadius * Math.sin(angle);
                const r = this.radius;
                points.push({ x, y, r});
            }
            return points;
        },
        amount() {
            return this.problemParams['amount'];
        }
    },
    methods: {
        handleCircleClick(index) {
            this.selectedPoints.push(index);
            this.$set(this.points[index], 'color', 'green');
            if (this.selectedPoints.length === 2) {
                const [index1, index2] = this.selectedPoints;
                const point1 = index1;
                const point2 = index2;
                console.log(this.countLinesFromPoint(point1), this.countLinesFromPoint(point2))
                const curIndex = this.lineIndex(point1, point2)
                if (curIndex !== -1) {
                    this.lines.splice(curIndex, 1);
                } else if (point1 !== point2 && this.countLinesFromPoint(point1) < 4 && this.countLinesFromPoint(point2) < 4) {
                    this.lines.push({ point1, point2 });
                    this.ans.push([index1, index2]);
                    this.$emit('updateAnswer', this.ans)
                    //console.log(this.ans)
                }
                this.selectedPoints = [];
            }
        },
        lineIndex(point1, point2) {
            return this.lines.findIndex(line => 
                (line.point1 === point1 && line.point2 === point2) ||
                (line.point1 === point2 && line.point2 === point1)
            );

        },
        countLinesFromPoint(pointIndex) {
            return this.lines.filter(line => line.point1 === pointIndex || line.point2 === pointIndex).length;
        },
    },
}
</script>