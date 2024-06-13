<template>
    <DialogShadowScreen>
        <div class="xhr_dialog">
            <div class="header">
                <div class="title">
                    <img class="info" src="/icons/warning.svg" />
                    <p> Обрати внимание! </p>
                </div>
                <img class="cross" @click="close" src="/icons/cross.svg" />
            </div>
            <p class="body"> <slot /> </p>
        </div>
    </DialogShadowScreen>
</template>

<script>
export default {
    methods: {
        close() {
            this.$emit('close')
        }
    },
}
</script>

<style scoped>
.xhr_dialog {
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
    color: white;
    font-weight: 600;
    font-size: 24px;
}

@keyframes show {
    0% {opacity: 0;}
    100% {opacity: 1;}
}

.header {
    display: inline-flex;
    align-items: center;
    justify-content: space-between;

}

.title {
    display: inline-flex;
    gap: 17px;
    align-items: center;
}

.info {
    width: 30px;
    height: 30px;
}

.cross {
    cursor: pointer;
    width: 24px;
    height: 24px;
}
</style>