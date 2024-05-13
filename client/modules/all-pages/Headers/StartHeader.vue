<template>
    <HeaderContainer ref="Header">
        <Logo />
        <StartPageNav @scrollToSection="blockHeader" />
        <ButtonArea>
            <template v-if="$auth.loggedIn">
                <AccButton />
                <LogoutButton />
            </template>
            <LogButton v-else />
        </ButtonArea>
    </HeaderContainer>
</template>

<script>
import HeaderContainer from './components/HeaderContainer.vue'
import StartPageNav from "./components/StartPageNav.vue"
import ButtonArea from "./components/ButtonArea.vue"
import LogButton from "./components/LoginButton.vue"
import LogoutButton  from './components/LogoutButton.vue'
import AccButton from './components/AccButton.vue'

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
        LogoutButton,
        AccButton,
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