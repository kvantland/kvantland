<template>
    <nav class="menu">
        <div
		v-for="item in menuItems" :key="item.id" 
        :class="`menu_item ${item.id}`" @click="scrollToSection(item.id)"> {{ item.title }} </div>
    </nav>
</template>

<script>
export default {
    data() {
        return {
            menuItems: [
                {'id': "commonInfo", 'title': "О турнире"},
                {'id': "problemExamples", 'title': "Примеры задач"},
                {'id': "teamInfo", 'title': "О нас"},
                {'id': "contacts", 'title': "Наши контакты"}
            ]
        }
    },

    methods: {
        scrollToSection(id) {
            this.$emit('scrollToSection')
            const add = document.querySelector('header').getBoundingClientRect().height
            const sectionTop = document.getElementById(id).getBoundingClientRect().top
            window.scrollTo(0,  sectionTop - add + window.pageYOffset)
        }
    },
}
</script>

<style scoped>
.menu {
	justify-content: flex-start; 
	align-items: center; 
	gap: max(10px, min(40px, 2.6vw)); 
	display: inline-flex;
}
.menu .menu_item {
	color: black; 
	font-size: max(10px, min(16px, 1.25vw)); 
	font-family: Montserrat Alternates; 
	font-weight: 500;
	border-radius: 20px;
	padding: 5px 10px;
	transition: 0.3s background;
}
.menu .menu_item:active {
	background: rgba(26.35, 88.38, 102, 0.20);
}
@media(hover:hover) {
	.menu .menu_item:hover {
		cursor: pointer;
		background: rgba(26.35, 88.38, 102, 0.10);
	}
}
</style>