<template>
    <div>
        <div class="shadow"></div>
        <div v-if="dialogType=='answer'" class="dialog answer" :num="dialogData.num">
            <div class="head">
                <p>{{ dialogData.problemInfo.title }}</p>
                <img class="cross" loading="lazy" @click="closeDialog" src="/icons/cross.svg"/>
            </div>
            <div class="body">
                <p>
                    <span class="bold_text"> Ответ: </span>
                    {{ dialogData.problemInfo.answer }}
                </p>
            </div>
            <div class="button solution">
                Посмотреть решение
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ["dialogType", "dialogData"],

    methods: {
        closeDialog() {
            this.$emit('closeDialog')
        }
    }
}
</script>