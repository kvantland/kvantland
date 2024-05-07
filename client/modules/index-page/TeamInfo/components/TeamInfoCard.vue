<template>
    <div class="content_box" v-if="cardInfo.type == 'personal'">
        <img class="photo" loading="lazy" :src="`/team_photos/${cardInfo.image}`" />
        <p class="name"> {{ cardInfo.name }} </p>
        <p v-html="cardInfo.desc"> </p>
    </div>
    <div class="content_box" v-else-if="cardInfo.type == 'list'">
        <div class="list">
            <template v-for="team_desc in cardInfo.desc">
                <div class="par">
                    <p class="header"> {{ team_desc.title }} </p>
                    <p v-for="member_name in team_desc.team_members"> {{ member_name }} </p>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    props: ["cardInfo"]
}
</script>