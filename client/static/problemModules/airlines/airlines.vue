<template>
    
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
            startValues: this.problemParams.start_values
        }
    },
    methods: {
        changeConfig(newValue) {
            let ans = []
            for (const slot of newValue) {
                ans.push(slot[1])
            }
            this.$emit('updateAnswer', ans)
        }
    }
}
</script>