<template>
    <HeaderContainer>
        <Logo />
        <ScoreBar v-if="$auth.loggedIn" />
        <ButtonArea>
            <template v-if="$auth.loggedIn">
                <AccButton />
                <LogoutButton />
            </template>
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
