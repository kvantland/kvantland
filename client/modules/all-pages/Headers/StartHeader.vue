<template>
    <header>
        <Logo />
        <StartPageNav @scrollToSection="blockHeader" />
        <ButtonArea>
            <LogButton />
        </ButtonArea>
    </header>
</template>

<script>
import StartPageNav from "./components/StartPageNav.vue"
import ButtonArea from "./components/ButtonArea.vue"
import LogButton from "./components/LogButton.vue"
import Logo from "../../../UI/Logo.vue"

export default {
    data(){
        return {
            topScrolled: 0,
            blocked: true,
        }
    },

    components: {
        Logo,
        StartPageNav,
        ButtonArea,
        LogButton,
    },

    methods: {
        blockHeader() {
            console.log('blocked!')
            this.blocked = true
        },
        scrollHeader(){
            if (!this.blocked) {
                if (this.topScrolled < document.documentElement.scrollTop && !this.blocked)
                    document.querySelector('header').classList = ['down']
                else if (this.topScrolled > document.documentElement.scrollTop && !this.blocked)
                    document.querySelector('header').classList = ['up']
            }
            if (this.blocked)
                this.blocked = false
            this.topScrolled = document.documentElement.scrollTop
        },
    },

    mounted() {
        window.addEventListener('scroll', this.scrollHeader)
    },
    destroyed() {
        window.removeEventListener('scroll', this.scrollHeader)
    }
}
</script>

<style>
@import "../../../assets/css/header.css"
</style>