<template>
    <div class="plot_area">
    <svg version="1.1" :width="svgWidth" 
        :height="svgHeight" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <circle
          v-for="(point, index) in points"
          :key="index"
          :cx="point.x"
          :cy="point.y"
          :r="point.radius"
          :fill="point.color"
        />
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
        return {
            amount: amount,
            side: 80,
            svgWidth: 400,
            svgHeight: 400,
            center: { x: 200, y: 200 }, // Center of the main circle
            mainCircleRadius: 100,
            numberOfCircles: 10,
        }
    },
    methods: {
    },

    computed: {
        points() {
            const points = [];
            const angleIncrement = (2 * Math.PI) / this.amount;
            for (let i = 0; i < this.amount; i++) {
                const angle = i * angleIncrement;
                const x = this.center.x + this.mainCircleRadius * Math.cos(angle);
                const y = this.center.y + this.mainCircleRadius * Math.sin(angle);
                const radius = 5;
                points.push({ x, y, radius});
            }
            return points;
        },
    },
}
</script>