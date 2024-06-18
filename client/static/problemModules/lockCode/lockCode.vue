<template>
    <div class="inRow">
        <img class="diplomat" src="/new-problem_assets/diplomat.png" />
        <div class="lockBorder">
            <Safe :slotsAmount="3" :startValues="startValues" @changeConfig="changeConfig" style="width: 95%; height: 95%;"/>
        </div>
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