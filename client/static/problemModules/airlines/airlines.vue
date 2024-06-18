<template>
    <div class="plot_area">
    <svg version="1.1" :width="svgWidth" 
        :height="svgHeight" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <line v-for="(line, index) in lines" :key="`line_${index}`"
                :x1="points[line.point1].x" :y1="points[line.point1].y"
                :x2="points[line.point2].x" :y2="points[line.point2].y"
                stroke="black" stroke-width="20px" class="lines"/>
        <g v-for="(point, index) in points" :key="`city_${index}`" :class="`city_${index}`" :transform="`translate(${point.x} ${point.y})`" @click="handleCircleClick(index)">
            <image :href="`/problem_assets/airlines/city${index % 3}.png`" :x="cityImgX" :y ="cityImgY" :width="cityImgWidth"/>
            <circle :r="point.r" :color="point.color" class="circles"/>
        </g>
    </svg>
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
        const amount = this.problemParams['amount']
        let ans = []
        return {
            amount: amount,
            side: 80,
            svgWidth: 400,
            svgHeight: 400,
            cityImgX: -40,
            cityImgY: -40,
            cityImgWidth: 80,
            center: { x: 200, y: 200 }, // Center of the main circle
            mainCircleRadius: 150,
            radius: 33,
            selectedPoints: [],
            lines: [],
            points: this.initialPoints(),
            ans: ans,
        }
    },
    computed: {
        computedPoints() {
            const angleIncrement = (2 * Math.PI) / this.amount;
            let points = []
            for (let i = 0; i < this.amount; i++) {
                const angle = i * angleIncrement;
                const x = this.center.x + this.mainCircleRadius * Math.cos(angle);
                const y = this.center.y + this.mainCircleRadius * Math.sin(angle);
                const r = this.radius;
                const color = "black"
                points.push({ x, y, r, color});
            }
            return points;
        },
    },
    watch: {
        computedPoints(newPoints) {
            this.points = newPoints;
        }
    },
    methods: {
        initialPoints() {
            return this.computedPoints;
        },
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
                this.$set(this.points[index1], 'color', 'black');
                this.$set(this.points[index2], 'color', 'black');
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
    created() {
        this.points = this.initialPoints();
    },
}
</script>