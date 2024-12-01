<template>
    <div class="svg_with_clear_button">
            <svg version="1.1"
            :viewBox="`0 0 ${svgWidth} ${svgHeight}`" 
            preserveAspectRatio="xMidYMid meet" 
            overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <g :transform="`translate(0 ${svgMarginTop})`">
                <image class="tap" :class="(transfusionSubject[0] == 'tap') ? 'choiced': 'not-choiced'" 
                    href="/problem_assets/tap.svg" :x="tapSize.x" :y="tapSize.y" :width="tapSize.width" :height="tapSize.height" @click="choose(['tap', 0])"/>
                <g :transform="`translate(${tapSize.width + tapPadding} 0)`">
                    <svg v-for="(pot, potNum) in potSizes" class="pot" overflow="visible"
                        :x="potSizes[potNum].x" :y="potSizes[potNum].y"
                        :width="potSizes[potNum].width" :height="potSizes[potNum].height">
                        <g :transform="`rotate(${potSizes[potNum].angle} ${potSizes[potNum].width / 2} 0)`" @click="choose(['pot', potNum])">
                            <rect class="liquid" x="4" :y="potSizes[potNum].height - liquidAmount[potNum] * potSizes[potNum].height + 2"
                                :fill="nectarConcentration[potNum] != 0 ? `rgba(255, 139, 31, ${nectarConcentration[potNum]})` : `rgba(204, 247, 247, 1)`" 
                                :width="potSizes[potNum].width - 8" :height="liquidAmount[potNum] * potSizes[potNum].height - 2" />
                            <image class="pot_form" href="/problem_assets/pot_form.svg" x="0" y="0" :width="potSizes[potNum].width" :height="potSizes[potNum].height" />
                            <image :class="(transfusionObject[0] == 'pot' && transfusionObject[1] == potNum 
                                || transfusionSubject[0] == 'pot' && transfusionSubject[1] == potNum) ? 'pot choiced' : 'pot not-choiced'"
                            href="/problem_assets/pot.svg"  
                                :width="potSizes[potNum].width" :height="potSizes[potNum].height" x="0" y="0"/>
                            <text class="volumeText" :x="potSizes[potNum].width / 2" dy="0.35em"
                                :y="potSizes[potNum].height - volumeTitleMarinBottom"> {{ volumes[potNum] }} </text>
                        </g>
                    </svg>
                    <image href="/icons/reload.png" :x="potsWidth + reloadPad" 
                        :y="svgHeight - reloadHeight - svgMarginTop" :width="reloadWidth" :height="reloadHeight" class="reload" @click="reload" />
                </g>
            </g>
        </svg>
        <button class="clear_button" @click="clearPot"> Вылить </button>
    </div>
</template>

<script>
export default {
    props: ['problemParams'],
    model: {
        prop: 'answer',
        event: 'updateAnswer',
    },
    data() {
        return {
            tapSize: {
                width: 80,
                height: 80,
                x: 0,
                y: 0,
                defaultX: 0,
                defaultY: 0,
            },
            volumeTitleMarinBottom: 65,
            firstPotWidth: 120,
            firstPotHeight: 140,
            tapPadding: 20,
            streamHeight: 15,
            reloadWidth: 90,
            reloadHeight: 90,
            reloadPad: 20,
            gap: 10,
            transfusionMode: false,
            transfusionObject: [undefined, -1],
            transfusionSubject: [undefined, -1],
            svgMarginTop: 100,
        }
    },
    computed: {
        volumes() {
            return this.problemParams.volumes
        },
        configuration() {
            return this.problemParams.configuration
        },
        potSizes() {
            let potSizes = []
            let maxHeight = 0
            let x = 0
            const firstVolume = this.volumes[0]
            for (const volume of this.volumes) {
                const scale = Math.sqrt(volume / firstVolume)
                potSizes.push({width: this.firstPotWidth * scale, 
                        height: this.firstPotHeight * scale, 
                        x: x, y: 0, 
                        defaultX: x, defaultY:0, angle:0})
                maxHeight = Math.max(maxHeight, this.firstPotHeight * scale)
                x += this.firstPotWidth * scale + this.gap
            }
            for (let potNum=0; potNum < potSizes.length; potNum++) {
                potSizes[potNum].y = maxHeight - potSizes[potNum].height
                potSizes[potNum].defaultY = maxHeight - potSizes[potNum].height
            }
            return potSizes
        },
        liquidAmount() { //percents
            const liquidAmount = Array(this.configuration.length)
            let potNum = 0
            for (const potConfig of this.configuration) {
                liquidAmount[potNum] = (potConfig['water'] + potConfig['nectar']) / this.volumes[potNum]
                potNum += 1
            }
            console.log('liquid amount: ', liquidAmount)
            return liquidAmount
        },
        nectarConcentration() {
            const nectarConcentration = Array(this.configuration.length)
            let potNum = 0
            for (const potConfig of this.configuration) {
                if (this.liquidAmount[potNum] != 0)
                    nectarConcentration[potNum] = potConfig['nectar'] / (this.liquidAmount[potNum] * this.volumes[potNum])
                else
                    nectarConcentration[potNum] = 0
                potNum += 1
            }
            console.log('nectar concentration: ', nectarConcentration)
            return nectarConcentration
        },
        potsWidth() {
            let potsWidth = 0
            for(const pot of this.potSizes) {
                potsWidth += this.gap + pot.width
            }
            return potsWidth
        },
        svgWidth() {
            return this.tapSize.width + this.potsWidth + this.reloadWidth + this.reloadPad
        },
        svgHeight() {
            let maxHeight = 0
            for (const pot of this.potSizes) {
                if (pot.height > maxHeight)
                    maxHeight = pot.height
            }
            return maxHeight + this.svgMarginTop
        }
    },
    methods: {
        choose(Obj) {
            if (this.transfusionSubject[0] && Obj[0] != 'tap') {
                console.log(Obj, this.transfusionSubject)
                if (Obj[0] == this.transfusionSubject[0] && Obj[1] == this.transfusionSubject[1]) {
                    this.transfusionSubject = [undefined, -1]
                }
                else {
                    this.transfusionObject = Obj
                    this.transfusionMode = true
                }
            }
            else {
                this.transfusionSubject = Obj
            }
        },
        reload() {
            this.$emit('xhrRequest', {type: 'reload'})
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
        },
        clearPot() {
            if (this.transfusionObject[0] == 'tap') {
                return;
            }
            else {
                this.transfusionMode = false
                this.$emit('xhrRequest', {transfusionSubject: this.transfusionSubject, type: 'clear'})
                this.toDefault()
            }
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
                        - (this.tapSize.width - this.potSizes[potNum].width / 2) + this.potSizes[potNum].width * 0.06
                    this.tapSize.y = this.potSizes[potNum].y - this.tapSize.height - this.streamHeight
                    this.$set(this.liquidAmount, potNum, 1)
                    console.log('concentration: ', nectarAmount/this.volumes[potNum])
                    this.$set(this.nectarConcentration, potNum, nectarAmount/this.volumes[potNum])
                }
                setTimeout(() => {resolve('success')}, 300)
            })
            transfusionPromise.then(result => {
                this.transfusionMode = false
                this.$emit('xhrRequest', {transfusionObject: this.transfusionObject, transfusionSubject: this.transfusionSubject, type: 'transfusion'})
            })
        }
    }
}
</script>