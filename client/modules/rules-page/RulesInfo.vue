<template>
    <div class="conf_content" id="rulesInfo">
        <div class="page_header">Правила — Квантландия</div>
            <RulesInfoCard :rulesDescription="rulesInfo.desc" 
                        v-for="(rulesInfoCard, key) in rulesInfoCards" :key="key" />
    </div>
</template>

<script>
import RulesInfoCard from "./components/RulesInfoCard.vue"

export default {
    components: {
        PolicyPar,
    },

    data() {
        return {
            rulesInfoCards: {},
        }
    },

    async fetch() {
        const rulesInfoCardData = await this.$axios.$get('/api/rules_card')
        this.rulesInfoCards = rulesInfoCardData
    },
}
</script>