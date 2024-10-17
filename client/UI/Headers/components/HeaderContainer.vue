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
			sensivity: 5, 
        }
    },

    mounted() {
        window.addEventListener('scroll', this.scrollHeader)
    },
    destroyed() {
        window.removeEventListener('scroll', this.scrollHeader)
    },

    methods: {
        scrollHeader(){
			const currentScroll =  document.documentElement.scrollTop
            if (!this.blocked) {
                if (this.topScrolled < currentScroll - this.sensivity) 
                    document.querySelector('header').classList = ['down']
                else if (this.topScrolled > currentScroll + this.sensivity && !this.blocked)
                    document.querySelector('header').classList = ['up']
            }
            if (this.blocked)
                this.blocked = false
			if (this.sensivity < Math.abs(this.topScrolled - currentScroll)) {
				this.topScrolled = currentScroll
			}
        },
    }
}
</script>

<style scoped>
header {
	width: 100vw;
	-webkit-user-select: none;
	user-select: none;
	background-color: white;
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
@media(max-width: 800px) {
	header {
		padding: 20px 16px;
	}
}
</style> 