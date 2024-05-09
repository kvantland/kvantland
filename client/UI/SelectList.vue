<template>
    <div class="select_box" :name="name">
        <div v-for="optionName in options" :class="optionName == selectedOption ? 'option selected' : 'option'" 
        @click="select(optionName)">{{ optionName }}</div>
    </div>
</template>

<script>
export default {
    props: ['name', 'options', 'selectedOption'],

    methods: {
        select(optionName) {
            this.$emit('hideSelectedList', optionName)
        },
    },
}
</script>

<style>
.select_box {
    z-index: 1;
    position: absolute;
    transform: translate(45%, -70%);
    box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.20);
    padding: 10px 0;
    border-radius: 10px;
    background-color: white;
    display: inline-flex;
    flex-direction: column;
    overflow: hidden;
}
.select_box .option {
    padding: 4px 20px;
    font-family: Montserrat Alternates;
    font-size: 14px;
    font-weight: 500;
    width: 160px;
    cursor: pointer;
}
.select_box .option.selected {
    background-color: #E8EEF0;
}
@media(hover:hover) {
    .select_box .option:hover {
        background-color: rgba(26.35, 88.38, 102, 0.10);
    }
}
</style>