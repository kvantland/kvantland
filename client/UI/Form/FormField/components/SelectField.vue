<template>
    <div>
        <div class="select_line" @click="showSelect">
            <input name="fieldInfo.name" :value="selectedOption"
            readonly required/> 
            <img class="arrow" src="/icons/down_arrow.svg" />
        </div>
        <SelectList ref="SelectList" v-if="showSelectList" :options="fieldInfo.options" 
        :name="fieldInfo.name" :selectedOption="selectedOption" @hideSelectedList="hideSelect"
        />
    </div>
</template>

<script>

export default {

    data() {
        return {
            showSelectList: false,
            canHideSelectList: 0, //на 2-й клик можно скрывать!
        }
    },

    props: {
        fieldInfo:{},
        selectedOption: {
            default: '',
        }
    },

    methods: {
        showSelect() {
            this.showSelectList = true
        },
        hideSelect(selectedOption) {
            this.showSelectList = false
            this.$emit('selectOption', selectedOption)
            this.canHideSelectList = 0
        },
        changeHideAbility() {
            if (this.canHideSelectList < 2)
                this.canHideSelectList += 1
        },
    },

    watch: {
        showSelectList(newValue) {
            if (newValue == true)
                window.addEventListener('click', this.changeHideAbility)
            else 
                window.removeEventListener('click', this.changeHideAbility)
        },
        canHideSelectList(newValue) {
            if (newValue == 2) 
                window.addEventListener('click', this.hideSelect(this.selectedOption))
        },
    }
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