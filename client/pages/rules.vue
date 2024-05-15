<template>
    <div>
        <StartHeader />
        <div class="content_wrapper">
            <ConfidentialityInfo />
        </div>
    </div>
</template>


<script>
import StartHeader from '../../modules/all-pages/Headers/StartHeader.vue'
import ConfidentialityInfo from '../../modules/policy-page/ConfidentialityInfo/ConfidentialityInfo.vue'
    export default {
        head() {
            return {
                title: 'Квантландия'
            };
        },

        components: {
            StartHeader,
            ConfidentialityInfo,
        },
    };
</script>

<style>
@import "../../assets/css/rules.css";
</style>
