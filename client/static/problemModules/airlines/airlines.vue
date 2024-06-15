<template>
    <div class="plot_area">
    <svg version="1.1" :width="svgWidth" 
        :height="svgHeight" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <line v-for="(line, index) in lines" :key="`line_${index}`" :x1="line.x1" :y1="line.y1" :x2="line.x2" :y2="line.y2" stroke="black" :class="`line_${index}`" />
        <circle v-for="(point, index) in points" :key="`city_${index}`" :cx="point.x" :cy="point.y" :r="point.r" :class="`city_${index}`" @click="handleCircleClick(index)"/>
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
            center: { x: 200, y: 200 }, // Center of the main circle
            mainCircleRadius: 150,
            numberOfCircles: 10,
            radius: 10,
            selectedPoints: [],
            lines: [],
            ans: ans,
        }
    },
    methods: {
        handleCircleClick(index) {
            if (this.selectedPoints.length < 2) {
                this.selectedPoints.push(index);
                if (this.selectedPoints.length === 2) {
                    const [index1, index2] = this.selectedPoints;
                    const point1 = this.points[index1];
                    const point2 = this.points[index2];
                    if (!this.lineExists(point1, point2) && this.countLinesFromPoint(point1) < 4 && this.countLinesFromPoint(point2) < 4) {
                        this.lines.push({
                            x1: point1.x,
                            y1: point1.y,
                            x2: point2.x,
                            y2: point2.y
                        });
                        this.ans.push([index1, index2]);
                        this.$emit('updateAnswer', this.ans)
                        console.log(this.ans)
                    }
                    this.selectedPoints = [];
                }
            } else {
                this.selectedPoints = [index];
            }
        },
        lineExists(point1, point2) {
            return this.lines.some(line => 
                ((line.x1 === point1.x && line.y1 === point1.y && line.x2 === point2.x && line.y2 === point2.y) ||
                (line.x1 === point2.x && line.y1 === point2.y && line.x2 === point1.x && line.y2 === point1.y))
            );

        },
        countLinesFromPoint(point) {
            return this.lines.filter(line => line.x1 === point.x && line.y1 === point.y).length;
        },
    },

    computed: {
        points() {
            const points = [];
            const angleIncrement = (2 * Math.PI) / this.amount;
            for (let i = 0; i < this.amount; i++) {
                const angle = i * angleIncrement;
                const x = this.center.x + this.mainCircleRadius * Math.cos(angle);
                const y = this.center.y + this.mainCircleRadius * Math.sin(angle);
                const r = this.radius;
                points.push({ x, y, r});
            }
            return points;
        },
    },
}
</script>