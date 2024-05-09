<template>
    <header>
        <Logo />
    </header>
</template>

<script>

export default {
    data(){
        return {
            topScrolled: 0,
            blocked: true,
        }
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