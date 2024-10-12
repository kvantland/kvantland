<template>
    <footer>
        <div class="basement">
            <hr size="1" color="#1E8B93" noshade />
            <div class="content">
                   <Logo />

            <div class="confidentiality">
                <NuxtLink to="/policy"> Политика конфиденциальности </NuxtLink>
            </div>
            <div class="organization"> © ООО "Квантик", 2024 </div>
            </div>
        </div>
    </footer>
</template>

<style scoped>
.basement {
	width: 100%;
	box-sizing: border-box;
	padding: 10px min(5vw, 80px) 0 min(5vw, 80px);
	justify-content: space-between; 
	align-items: center; 
	display: inline-flex;
	flex-direction: column;
	gap: 60px;
	margin-bottom: 60px;
}

.basement hr {
	width: 100%;
	color: #1E8B93;
}

.basement .content {
	align-items: center;
	align-self: stretch;
	display: flex;
	justify-content: space-between;
}

.basement .logo_area {
	justify-content: center;
	align-items: center; 
	gap: 10px; 
	display: flex;
}

.basement .logo {
	width: 52px; 
	height: 52px;
	border-radius: 10px;
}

.basement .logo_name {
	color: #1E8B93; 
	font-size: 20px; 
	font-family: Montserrat Alternates; 
	font-weight: 600;
}

.basement .confidentiality {
	display: inline-block;
	width: min-content;
	font-size: 16px;
	font-family: Montserrat Alternates;
	font-weight: 500;
	text-decoration: underline;
}

.basement .organization {
	font-size: 16px;
	font-family: Montserrat Alternates;
	font-weight: 500;
}

@media(max-width: 800px) {
	.basement .organization {
		font-size: 2vw;
	}
	.basement .confidentiality {
		font-size: 2vw;
	}
	.basement {
		gap: 22px;
		margin-bottom: 22px;
	}
}
</style>