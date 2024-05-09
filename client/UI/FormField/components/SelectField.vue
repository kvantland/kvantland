<template>
    <div>
        <div class="select_line" @click="showSelect">
            <input name="fieldInfo.name" readonly required :value="selectedOption" /> 
            <img class="arrow" src="/icons/down_arrow.svg" />
        </div>
        <SelectList v-if="showSelectList" :options="fieldInfo.options" 
        :name="fieldInfo.name" :selectedOption="selectedOption" @hideSelectedList="hideSelect"/>
    </div>
</template>

<script>

export default {

    data() {
        return {
            showSelectList: false,
            selectedOption: '',
        }
    },

    props: ['fieldInfo'],

    methods: {
        showSelect() {
            this.showSelectList = true
        },
        hideSelect(selectedOption) {
            console.log(selectedOption)
            this.showSelectList = false
            this.selectedOption = selectedOption
        }
    },
}
</script>

<style>
.select_line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: Montserrat Alternates;
    cursor: pointer;
}
.select_line input {
    appearance: none;
    cursor: inherit;
}
.arrow {
    width: 10px;
    height: 5.84px;
}
</style>