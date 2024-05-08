<template>
    <div class="tournament">
        <div class="curr_tournament">
            <img class="map" loading="lazy" src="/map_img/land.png" />
            <div class="text_container">
                <div>
                    <p class="header">Турнир</p>
                    <p class="text">Твоя возможность проявить себя!</p>
                </div>
                <p class="text">Тебя ждут задачи из самых разных областей математики:  
                    Головоломки, Логика, Комбинаторика, Арифметика, Геометрия</p>
                <NuxtLink to="/rules">
                    <div class="start_button"> Открыть турнир </div>
                </NuxtLink>
            </div>
        </div>
        <TournamentHistory />
    </div>
</template>

<script>
import TournamentHistory from "./components/TournamentHistory.vue"

export default {
    components: {
        TournamentHistory,
    }
}
</script>