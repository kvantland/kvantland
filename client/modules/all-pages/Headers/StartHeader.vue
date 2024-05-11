<template>
    <HeaderContainer ref="Header">
        <Logo />
        <StartPageNav @scrollToSection="blockHeader" />
        <ButtonArea>
            <LogButton />
        </ButtonArea>
    </HeaderContainer>
</template>

<script>
import HeaderContainer from './components/HeaderContainer.vue'
import StartPageNav from "./components/StartPageNav.vue"
import ButtonArea from "./components/ButtonArea.vue"
import LogButton from "./components/LogButton.vue"

export default {
    data(){
        return {
            blockedHeader: false,
        }
    },

    components: {
        HeaderContainer,
        StartPageNav,
        ButtonArea,
        LogButton,
    },

    methods: {
        blockHeader() {
            this.$refs['Header'].blocked = true
        },
    },
}
</script>

<style>
@import "../../../assets/css/header.css"
</style>