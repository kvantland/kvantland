<template>
	<div class="logout_component">
		<LogoutDialog v-if="logoutDialogMode" @hideDialog="hideLogoutDialog"/>
		<div class="logout_button" role="button" tabindex="0" @click="showLogoutDialog"> Выйти </div>
	</div>
</template>

<script>
import LogoutDialog from './LogoutDialog.vue'

export default {
	components: {
		LogoutDialog
	},

	data() {
		return {
			logoutDialogMode: false
		}
	},

	methods: {
		showLogoutDialog() {
			this.logoutDialogMode = true
		},
		hideLogoutDialog(){
			this.logoutDialogMode = false
		},
	}
}
</script>

<style scoped>
.logout_component {
	height: 100%;
}

.logout_button {
	height: 100%;
	display: flex;
	align-items: center;
	padding: 0 20px;
	background: #1E8B93; 
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25); 
	border-radius: 10px;
	color: white; 
	font-size: min(2vw, 20px); 
	font-family: Montserrat Alternates; 
	font-weight: 600;
	cursor: pointer;
}
</style>