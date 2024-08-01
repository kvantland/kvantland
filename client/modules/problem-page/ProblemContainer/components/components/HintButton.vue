<template>
    <div>
        <ConfirmHintDialog v-if="dialogMode" @hideHintConfirmDialog="hideHintConfirmDialog" @getHint="getHint" :hintCost="hintCost" />
        <button class="hint_button" :title="hintTitle" @click="showConfirmHintDialog"> 
            <img class="hint_icon" src="/icons/hint_icon.svg" />
            <p> Подсказка </p>
        </button>
    </div>
</template>

<script>
import ConfirmHintDialog from './ConfirmHintDialog'

export default {
    props: {
        hintCost: {default: "1 квантик"},
    },

    components: {
        ConfirmHintDialog,
    },

    data() {
        return {
            hintTitle: 'Получить подсказку (стоимость: 1)',
            dialogMode: false,
        }
    },
    
    methods: {
        showConfirmHintDialog() {
            this.dialogMode = true
        },
        hideHintConfirmDialog() {
            this.dialogMode = false
        },
        getHint() {
            this.$emit('getHint')
        }
    }
}
</script>

<style scoped>
.hint_button {
    user-select: none;
    -webkit-user-select: none;
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
    cursor: pointer;
}

.hint_icon {
    height: 25px;
    color: black;
}

</style>