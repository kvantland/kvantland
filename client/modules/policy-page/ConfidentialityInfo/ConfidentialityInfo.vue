<template>
    <div class="conf_content" id="confidentialityInfo">
        <div class="page_header">Политика конфиденциальности</div>
            <PolicyPar :parHeader="policyPar.header" :parDescription="policyPar.desc" 
                        v-for="(policyPar, key) in policyPars" :key="key" />
    </div>
</template>

<script>
import PolicyPar from "./components/PolicyPar.vue"

export default {
    components: {
        PolicyPar,
    },

    data() {
        return {
            policyPars: {},
        }
    },

    async fetch() {
        const policyParsData = await this.$axios.$get('/policy_pars')
        this.policyPars = policyParsData
    },
}
</script>