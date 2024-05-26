<template>
    <button class="hint_button" :title="hintTitle"> 
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
}
</script>

<style scoped>
.hint_button {
    align-self: stretch;
    padding: 10px 20px;
    background: #FFC400;
    box-shadow: 7px 7px 7px #1A5866;
    border-style: none;
    border-radius: 10px;
    justify-content: center;
    align-items: center;
    gap: 10px;
    display: flex;
    font-size: 24px;
    font-family: Montserrat;
    font-weight: 600;
    text-align: center;
}

.hint_icon {
    height: 25px;
    color: black;
}

</style>