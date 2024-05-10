<template>
    <button class="submit_button" type="submit" :form="id" @click="onClick">
        <slot />
    </button>
</template>


<script>
export default {
    props: ['id'],

    methods: {
        onClick(){
            this.$emit('onClick')
        }
    }
}
</script>

<style>
.submit_button {
    cursor: pointer;
    align-self: stretch;
    padding: 0 20px;
    height: 50px;
    font-size: 14px;
    font-weight: 600;
    background: #1E8B93;
    box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25);
    border-radius: 6px;
    color: white;
    border: none;
    font-family: Montserrat;
}
</style>