<template>
    <DialogShadowScreen>
        <div class="dialog">
            <div class="dialog_header">
                <p> {{ title }} </p>
                <div><img class="cross" loading="lazy" @click="closeDialog" src="/icons/cross.svg" /></div>
            </div>
            <div class="content">
                <p v-for="(par, parNum) in pars" :key="`par_${parNum}`" v-html="par"></p>
            </div>
        </div>
    </DialogShadowScreen>
</template>

<script>

export default {
    data() {
        return {
            title: 'Согласие на обработку персональных данных',
            pars: [],
        }
    },

    async fetch() {
        const pars = await this.$axios.$get('/api/agreement_pars')
        this.pars = pars
    },

    methods: {
        closeDialog() {
            this.$emit('closeDialog')
        },
    },
}
</script>

<style scoped>
.dialog {
    opacity: 1;
    animation: show 0.4s;
    min-width: 500px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    display: inline-flex;
    flex-direction: column;
    gap: 40px;
    padding: 40px 60px;
    background: rgb(30, 139, 147);
    border-radius: 20px;
    font-family: Montserrat;
    font-weight: 600;
    font-size: 24px;
}

@keyframes show {
    0% {opacity: 0;}
    100% {opacity: 1;}
}

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
::v-deep a.policy {
    font-weight: 600;
    text-decoration: underline;
}
img.cross {
    cursor: pointer;
    align-self: center;
}
</style>