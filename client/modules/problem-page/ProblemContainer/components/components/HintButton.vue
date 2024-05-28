<template>
    <button class="hint_button" :title="hintTitle" @click="getHint"> 
        <img class="hint_icon" src="/icons/hint_icon.svg" />
        <p> Подсказка </p>
    </button>
</template>

<script>
export default {
    data() {
        return {
            hintTitle: 'Получить подсказку (стоимость: 1)',
        }
    },
    
    methods: {
        getHint() {
            this.$emit('getHint')
        }
    }
}
</script>

<style scoped>
.hint_button {
    padding: 10px 20px;
    background: #FFC400;
    box-shadow: 7px 7px 7px #1A5866;
    border-style: none;
    border-radius: 10px;
    align-items: center;
    gap: 10px;
    display: inline-flex;
    font-size: 24px;
    font-family: Montserrat;
    font-weight: 600;
    text-align: center;
    justify-self: flex-end;
}

.hint_icon {
    height: 25px;
    color: black;
}

</style>