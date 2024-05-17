<template>
    <div class="conf_content" id="confidentialityInfo">
        <div class="page_header">Политика конфиденциальности</div>
            <PolicyPar :parHeader="policyPar.header" :parDescription="policyPar.desc" :num="key"
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
        const policyParsData = await this.$axios.$get('/api/policy_pars')
        this.policyPars = policyParsData
    },
}
</script>

<style>
.conf_content {
    align-self: stretch;
    display: flex;
    flex-direction: column;
    gap: 40px;
    padding: 40px;
    border-radius: 40px;
    border: 3px #1E8B93 solid;
}

.conf_content .page_header {
    color: #1E8B93;
    font-size: 40px;
    font-family: Montserrat Alternates;
    font-weight: 600;
    text-transform: capitalize;
}

.conf_content a {
    color: #0000EE !important;
    text-decoration: underline !important;
}

.conf_content a.visited {
    color: #551A8B !important;
}
</style>