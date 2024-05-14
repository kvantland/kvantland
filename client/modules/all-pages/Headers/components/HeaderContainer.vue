<template>
    <header>
        <slot />
    </header>
</template>

<script>
export default {

    data(){
        return {
            topScrolled: 0,
            blocked: false,
        }
    },

    methods: {
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
header {
	-webkit-user-select: none;
	user-select: none;
	background-color: white;
	width: 100%;
	box-sizing: border-box;
	position: fixed;
	padding: 30px max(40px, min(5vw, 80px));
	justify-content: space-between; 
	align-items: center; 
	display: inline-flex;
	z-index: 2;
	box-shadow: 0 1px 5px #C2C2C2;
    transition: transform 0.3s;
}
header.up {
	transform: none;
}

header.down {
	transform: translate(0, -100%);
}
</style>