<template>
    <div class="data_preview">
        <img class="avatar_img" src="/icons/userAvatar.png" />
        <div class="text_data">
            <div class="name_with_edit">
                <p class="name"> {{ userInfo.name }} {{ userInfo.surname }} </p>
                <NuxtLink to="/acc/editInfo">
                    <img class="edit" src="/icons/edit.svg" />
                </NuxtLink>
            </div>

            <p class="city"> {{ userInfo.town }} </p>
            <p class="school"> {{ userInfo.school }} </p>
        </div>
    </div>
</template>

<script>
export default {
    props: ['userInfo'],
}
</script>

<style scoped>
.data_preview {
	display: inline-flex;
	flex-direction: row;
	padding: 10px 20px;
	width: 320px;
	box-sizing: border-box;
	background: rgba(26, 88, 102, 0.1);
	border-radius: 6px;
	justify-content: space-between;
	gap: 10px;
}

.data_preview .avatar_img {
	width: 70px;
	height: 70px;
}

.data_preview .text_data {
	width: 100%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	padding: 10px 0px;
	font-size: 12px;
}

.data_preview .name_with_edit {
	display: inline-flex;
	flex-direction: row;
	justify-content: space-between;
}

.data_preview .name {
	font-size: 12px;
	font-weight: 600;
}

.data_preview .edit {
    cursor: pointer;
}
@media (max-width: 800px) {
	.data_preview {
		width: 100%;
		box-sizing: border-box;
	}
}
</style>