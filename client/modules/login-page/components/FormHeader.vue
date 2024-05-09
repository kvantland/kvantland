<template>
     <div class="header">
        <span :class="mode=='auth' ? 'dark' : 'light'" @click="changeHeaderMode('auth')"> ВХОД </span>
        <span :class="mode=='reg' ? 'dark' : 'light'" @click="changeHeaderMode('reg')"> РЕГИСТРАЦИЯ </span>
	 </div>
</template>

<script>
export default {
    props: ['mode'],

    methods: {
        changeHeaderMode(modeToChange) {
            this.$emit('changeHeaderMode', modeToChange)
        }
    },
}
</script>


<style>
.header {
    display: inline-flex;
    justify-content: center;
    gap: 20px;
    font-weight: 700;
    font-size: 16px;
    text-transform: uppercase;
}
.header span {
    cursor: pointer;
}
span.dark {
    color: black;
}
span.light {
    color: rgba(0, 0, 0, 0.30);
}
</style>