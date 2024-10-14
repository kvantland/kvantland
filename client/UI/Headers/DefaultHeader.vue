<template>
    <HeaderContainer>
        <Logo />
        <ScoreBar v-if="$auth.loggedIn" class="score_bar"/>
        <ButtonArea v-show="$auth.loggedIn" style="display: none;">
            <AccButton />
            <LogoutButton />
        </ButtonArea>
    </HeaderContainer>
</template>

<script>
import ButtonArea from './components/ButtonArea.vue';
import AccButton from './components/AccButton.vue';
import LogoutButton from './components/LogoutButton.vue';
import HeaderContainer from './components/HeaderContainer.vue'
import ScoreBar from './components/ScoreBar.vue'

export default {
    components: {
        HeaderContainer,
        ScoreBar,
        ButtonArea,
        AccButton,
        LogoutButton,
    }
}
</script>

<style scoped>
@media(max-width: 800px) {
	.score_bar {
		display: none;
	}
}
</style>