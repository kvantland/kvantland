<template>
     <svg version="1.1" :width="svgWidth" :height="svgHeight" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <image class="tap" href="/new-problem_assets/tap.svg" x="0" y="0" :width="tapWidth" :height="tapHeight"/>
        <g :transform="`translate(${tapWidth + tapPadding} 0)`">
            <image v-for="(pot, potNum) in potSizes" class="pot" href="/new-problem_assets/pot.svg" 
                :width="potSizes[potNum].width" :height="potSizes[potNum].height"
                :x="gap * (potNum + 1) + potSizes[potNum].x" :y="svgHeight - potSizes[potNum].height" />
        </g>
    </svg>
</template>

<script>
export default {
    props: ['problemParams'],
    model: {
        prop: 'answer',
        event: 'updateAnswer',
    },
    data() {
        const firstVolume = this.problemParams.volumes[0]
        const firstHeight = 70
        const firstWidth = 60
        let x = 0
        let potSizes = []
        for (const volume of this.problemParams.volumes) {
            const scale = Math.sqrt(volume / firstVolume)
            potSizes.push({width: firstWidth * scale, height: firstHeight * scale, x: x, y: 0})
            x += firstWidth * scale
        }
        return {
            tapWidth: 60,
            tapHeight: 60,
            tapPadding: 10,
            gap: 10,
            potSizes: potSizes,
        }
    },
    computed: {
        svgWidth() {
            const potsWidth = this.potSizes[this.potSizes.length - 1].x + this.potSizes[this.potSizes.length - 1].width + this.gap * this.potSizes.length
            return this.tapWidth + potsWidth
        },
        svgHeight() {
            let maxHeight = 0
            for (const pot of this.potSizes) {
                if (pot.height > maxHeight)
                    maxHeight = pot.height
            }
            return maxHeight
        }
    }
}
</script>