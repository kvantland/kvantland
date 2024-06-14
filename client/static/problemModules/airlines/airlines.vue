<template>
    <div class="plot_area">
    <svg version="1.1" :width="svgWidth" 
        :height="svgHeight" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <line v-for="(line, index) in lines" :key="index" :x1="line.x1" :y1="line.y1" :x2="line.x2" :y2="line.y2" stroke="black" />
        <circle v-for="(point, index) in points" :key="index" :cx="point.x" :cy="point.y" :r="point.r" :class="`city_${index}`" @click="handleCircleClick(index)"/>
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
        let cities = []
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
                    this.lines.push({
                        x1: point1.x,
                        y1: point1.y,
                        x2: point2.x,
                        y2: point2.y
                    });
                    this.selectedPoints = [];
                }
            } else {
                this.selectedPoints = [index];
            }
        }
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