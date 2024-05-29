<template>
    <div class="content_wrapper_rules">
        <Breadcrumbs :crumbs="rulesCrumbs" />
        <RulesInfo />
    </div>
</template>


<script>
import RulesInfo from '../modules/rules-page/RulesInfo.vue'
    export default {
        head() {
            return {
                title: 'Правила — Квантландия'
            };
        },
        middleware: 'auth',
        components: {
            RulesInfo,
        },

        data() {
            return {
                rulesCrumbs: {},
            }
        },

    async fetch() {
        const rulesCrumbsData = await this.$axios.$get('/api/rules_crumbs')
        this.rulesCrumbs = rulesCrumbsData
    },
};
</script>

<style>
.content_wrapper_rules {
    width: 100%;
    padding: 0 min(80px, 5vw);
    margin-top: 130px;
    box-sizing: border-box;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 40px;
    display: inline-flex;
    padding-bottom: 80px;
}
</style>
