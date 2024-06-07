<template>
     <svg version="1.1" :width="svgWidth" :height="svgHeight" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <image class="tap" :class="(transfusionSubject[0] == 'tap') ? 'choiced': 'not-choiced'" 
            href="/new-problem_assets/tap.svg" :x="tapSize.x" :y="tapSize.y" :width="tapSize.width" :height="tapSize.height" @click="choose(['tap', 0])"/>
        <g :transform="`translate(${tapSize.width + tapPadding} 0)`">
            <svg v-for="(pot, potNum) in potSizes" class="pot" overflow="visible"
                :transform="`rotate(${potSizes[potNum].angle} ${potSizes[potNum].width / 2 + potSizes[potNum].x} ${potSizes[potNum].y})`"
                :x="potSizes[potNum].x" :y="potSizes[potNum].y"
                :width="potSizes[potNum].width" :height="potSizes[potNum].height">
                <rect class="liquid" x="4" :y="potSizes[potNum].height - liquidAmount[potNum] * potSizes[potNum].height + 2"
                    :fill="nectarConcentration[potNum] != 0 ? `rgba(255, 139, 31, ${nectarConcentration[potNum]})` : `rgba(204, 247, 247, 1)`" 
                    :width="potSizes[potNum].width - 8" :height="liquidAmount[potNum] * potSizes[potNum].height - 2" />
                <image class="pot_form" href="/new-problem_assets/pot_form.svg" x="0" y="0" :width="potSizes[potNum].width" :height="potSizes[potNum].height" />
                <image :class="(transfusionObject[0] == 'pot' && transfusionObject[1] == potNum 
                    || transfusionSubject[0] == 'pot' && transfusionSubject[1] == potNum) ? 'pot choiced' : 'pot not-choiced'"
                href="/new-problem_assets/pot.svg" @click="choose(['pot', potNum])"
                    :width="potSizes[potNum].width" :height="potSizes[potNum].height" x="0" y="0"/>
            </svg>
            <image href="/icons/reload.png" :x="potSizes[potSizes.length - 1].x + potSizes[potSizes.length - 1].width + reloadPad" 
                :y="svgHeight - reloadHeight" :width="reloadWidth" :height="reloadHeight" class="reload" @click="reload" />
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
        const firstHeight = 100
        const firstWidth = 90
        const gap = 10
        const configuration  = this.problemParams.configuration
        let x = 0
        let potSizes = []
        let maxHeight = 0
        for (const volume of this.problemParams.volumes) {
            const scale = Math.sqrt(volume / firstVolume)
            potSizes.push({width: firstWidth * scale, 
                    height: firstHeight * scale, 
                    x: x, y: 0, 
                    defaultX: x, defaultY:0, angle:0})
            maxHeight = Math.max(maxHeight, firstHeight * scale)
            x += firstWidth * scale + gap
        }
        for (let potNum=0; potNum < potSizes.length; potNum++) {
            potSizes[potNum].y = maxHeight - potSizes[potNum].height
            potSizes[potNum].defaultY = maxHeight - potSizes[potNum].height
        }
        let potNum = 0
        const liquidAmount = Array(configuration.length)
        const nectarConcentration = Array(configuration.length)
        for (const potConfig of configuration) {
            liquidAmount[potNum] = (potConfig['water'] + potConfig['nectar']) / this.problemParams.volumes[potNum]
            if (liquidAmount[potNum] != 0)
                nectarConcentration[potNum] = potConfig['nectar'] / (liquidAmount[potNum] * this.problemParams.volumes[potNum])
            else
                nectarConcentration[potNum] = 0
            potNum += 1
        }
        return {
            tapSize: {
                width: 60,
                height: 60,
                x: 0,
                y: 0,
                defaultX: 0,
                defaultY: 0,
            },
            tapPadding: 20,
            streamHeight: 15,
            reloadWidth: 70,
            reloadHeight: 70,
            reloadPad: 20,
            gap: gap,
            volumes: this.problemParams.volumes,
            potSizes: potSizes,
            transfusionMode: false,
            transfusionObject: [undefined, -1],
            transfusionSubject: [undefined, -1],
            liquidAmount: liquidAmount,
            nectarConcentration: nectarConcentration,
        }
    },
    computed: {
        svgWidth() {
            let potsWidth = 0
            for(const pot of this.potSizes) {
                potsWidth += this.gap + pot.width
            }
            console.log(potsWidth)
            return this.tapSize.width + potsWidth + this.reloadWidth + this.reloadPad
        },
        svgHeight() {
            let maxHeight = 0
            for (const pot of this.potSizes) {
                if (pot.height > maxHeight)
                    maxHeight = pot.height
            }
            return maxHeight
        }
    },
    methods: {
        choose(Obj) {
            if (this.transfusionSubject[0] && Obj[0] != 'tap') {
                console.log('start transfusion!')
                this.transfusionObject = Obj
                this.transfusionMode = true
            }
            else {
                this.transfusionSubject = Obj
            }
        },
        async reload() {
            this.$emit('xhrRequest', {type: 'reload'})
            console.log('here!')
            //this.$emit('updateProblemStatus')
        },
        toDefault() {
            this.transfusionObject = [undefined, -1]
            this.transfusionSubject = [undefined, -1]
            for(let potNum=0; potNum < this.potSizes.length; potNum++) {
                const newParams = this.potSizes[potNum]
                newParams.y = newParams.defaultY
                newParams.x = newParams.defaultX
                newParams.angle = 0
                this.$set(this.potSizes, potNum, newParams)
            }
            this.tapSize.y = this.tapSize.defaultY
            this.tapSize.x = this.tapSize.defaultX
        }
    },
    watch: {
        async transfusionMode(newValue) {
            if (newValue == false) {
                this.toDefault()
                return;
            }
            console.log(this.transfusionObject, this.transfusionSubject)
            let transfusionPromise = new Promise((resolve, reject) => {
                if (this.transfusionSubject[0] == 'pot') {
                    const objectNum = this.transfusionObject[1]
                    const subjectNum = this.transfusionSubject[1]
                    let params = this.potSizes[subjectNum]
                    const transfusionLiquidAmount = Math.min(this.volumes[objectNum] * (1 - this.liquidAmount[objectNum]), 
                            this.volumes[subjectNum] * this.liquidAmount[subjectNum])
                    console.log('liquid: ', transfusionLiquidAmount)
                    const nectarAmount = transfusionLiquidAmount * this.nectarConcentration[subjectNum]
                                    + this.liquidAmount[objectNum] * this.nectarConcentration[objectNum] * this.volumes[objectNum]
                    console.log(this.nectarConcentration[subjectNum])
                    console.log('objectLiquid: ', this.liquidAmount[objectNum])
                    console.log('nectarAmount: ', nectarAmount)
                    params.x = this.potSizes[objectNum].x
                    params.y = this.potSizes[objectNum].y - params.width * 2/3
                    if (subjectNum < objectNum)
                        params.angle = 90
                    else 
                        params.angle = -90
                    this.$set(this.potSizes, subjectNum, params)
                    this.$set(this.liquidAmount, subjectNum, (this.liquidAmount[subjectNum] * this.volumes[subjectNum] - transfusionLiquidAmount) / this.volumes[subjectNum])
                    this.$set(this.liquidAmount, objectNum, (this.liquidAmount[objectNum] * this.volumes[objectNum] + transfusionLiquidAmount) / this.volumes[objectNum])
                    this.$set(this.nectarConcentration, objectNum, nectarAmount/(this.volumes[objectNum] * this.liquidAmount[objectNum]))
                }
                else if (this.transfusionSubject[0] == 'tap') {
                    const potNum = this.transfusionObject[1]
                    const nectarAmount = this.liquidAmount[potNum] * this.nectarConcentration[potNum] * this.volumes[potNum]
                    this.tapSize.x = this.potSizes[potNum].x + this.tapSize.width + this.tapPadding 
                        - (this.tapSize.width - this.potSizes[potNum].width / 2) + this.potSizes[potNum].width * 0.1
                    this.tapSize.y = this.potSizes[potNum].y - this.tapSize.height - this.streamHeight
                    this.$set(this.liquidAmount, potNum, 1)
                    console.log('concentration: ', nectarAmount/this.volumes[potNum])
                    this.$set(this.nectarConcentration, potNum, nectarAmount/this.volumes[potNum])
                }
                setTimeout(() => {resolve('success')}, 1000)
            })
            transfusionPromise.then(result => {
                this.transfusionMode = false
                this.$emit('xhrRequest', {transfusionObject: this.transfusionObject, transfusionSubject: this.transfusionSubject, type: 'transfusion'})
            })
        }
    }
}
</script>