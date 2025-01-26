<template>
    <HeaderContainer ref="Header">
        <Logo/>
        <MainStartPageNav @scrollToSection="blockHeader" />
        <ButtonArea />
    </HeaderContainer>
</template>

<script>
import HeaderContainer from './components/HeaderContainer.vue'
import MainStartPageNav from './components/MainStartPageNav.vue'
import ButtonArea from './components/ButtonArea.vue';

export default {

    components: {
        HeaderContainer,
				ButtonArea,
				MainStartPageNav,
    },
    data(){
        return {
            blockedHeader: false,
        }
    },

    methods: {
        blockHeader() {
            this.$refs.Header.blocked = true
        },
    },
}
</script>
