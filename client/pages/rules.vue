<template>
    <div>
        <StartHeader />
        <div class="content_wrapper_rules">
            <Breadcrumbs :crumbs="rulesCrumbs" />
            <RulesInfo />
        </div>
    </div>
</template>


<script>
import StartHeader from '../modules/all-pages/Headers/StartHeader.vue'
import Breadcrumbs from '../modules/all-pages/Breadcrumbs.vue'
import RulesInfo from '../modules/rules-page/RulesInfo.vue'
    export default {
        head() {
            return {
                title: 'Правила — Квантландия'
            };
        },
        middleware: 'auth',
        components: {
            StartHeader,
            Breadcrumbs,
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
