<template>
    <div>
        <div class="shadow"></div>
        <div class="dialog">
            <div class="dialog_header">
                <p> {{ title }} </p>
                <div><img class="cross" loading="lazy" @click="closeDialog" src="/icons/cross.svg" /></div>
            </div>
            <div class="content">
                <p v-for="par in pars" v-html="par"></p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            title: 'Согласие на обработку персональных данных',
            pars: [],
        }
    },

    methods: {
        closeDialog() {
            this.$emit('closeDialog')
        },
    },

    async fetch() {
        const pars = await this.$axios.$get('/api/agreement_pars')
        this.pars = pars
    },
}
</script>

<style>
.dialog_header {
    display: inline-flex;
    justify-content: space-between;
    color: white;
    font-size: 24px;
    font-weight: 600;
}
.dialog .content {
    width: 700px;
    display: inline-flex;
    flex-direction: column;
    padding: 40px;
    gap: 40px;
    border-radius: 16px;
    box-shadow: 12px 12px 14px 0px rgba(0, 0, 0, 0.25);
    background: rgb(255, 255, 255);
    font-family: Montserrat;
    font-size: 20px;
    font-weight: 400;
}
a.policy {
    font-weight: 600;
    text-decoration: underline;
}
img.cross {
    cursor: pointer;
    align-self: center;
}
</style>