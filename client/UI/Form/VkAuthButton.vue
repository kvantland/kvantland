<template>
    <div class="vk_button" @click="vkAuth">
        <span> Войти через </span>
        <img src="/icons/vk_button.svg" />
    </div>
</template>

<script>
export default {
    methods: {
        vkAuth() {
            console.log('vk_reg_attempt')
            this.$auth.loginWith('vk')
        }
    }
}
</script>

<style>
.vk_button {
    padding: 0 20px;
    height: 50px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    font-weight: 600;
    background: white;
    box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25);
    border-radius: 6px;
    color: #1E8B93;
    border: 2px #1E8B93 solid;
    cursor: pointer;
}
</style>