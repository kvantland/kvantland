<template>
    <chessProblemLayout :dragFigures="dragFigures" :boardConfiguration="boardConfiguration" 
        @updateConfig="updateConfig"
        @updateFiguresAmount="updateFiguresAmount" style="width: 57%"/>
</template>

<script>
export default {
    props: ['problemParams'],
    data() {
        return {
            boardConfiguration: 'empty',
            dragFigures: [{type: 'rook_b', amount: this.problemParams.rooks_amount}],
        }
    },
    methods: {
        updateConfig(newConfig) {
            console.log(newConfig)
            this.boardConfiguration = newConfig
        },
        updateFiguresAmount(newValue) {
            console.log(newValue)
            if (this.dragFigures[newValue.index] === 'inf') {
                return
            }
            else {
                this.$set(this.dragFigures[newValue.index], 'amount', newValue.amount)
            }
        }
    }
}
</script>