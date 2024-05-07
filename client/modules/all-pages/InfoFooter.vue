<template>
    <footer>
        <div class="basement">
            <hr size="1" color="#1E8B93" noshade />
            <div class="content">
                <NuxtLink to="/">
                   <Logo />
                </NuxtLink>

            <div class="confidentiality">
                <NuxtLink to="/policy"> Политика конфиденциальности </NuxtLink>
            </div>
            <div class="organization"> © ООО "Квантик", 2024 </div>
            </div>
        </div>
    </footer>
</template>

<script>
import Logo from "../../UI/Logo.vue"
export default {
    components: {
        Logo,
    }
}
</script>

<style>
@import "../../assets/css/footer.css"
</style>