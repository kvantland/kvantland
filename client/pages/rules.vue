<template>
    <div>
        <StartHeader />
        <div class="content_wrapper">
            <RulesInfo />
        </div>
    </div>
</template>


<script>
import StartHeader from '../modules/all-pages/Headers/StartHeader.vue'
import RulesInfo from '../modules/rules-page/RulesInfo.vue'
    export default {
        head() {
            return {
                title: 'Правила — Квантландия'
            };
        },

        components: {
            StartHeader,
            RulesInfo,
        },
    };
</script>

<style>
@import "../assets/css/rules.css";
</style>
