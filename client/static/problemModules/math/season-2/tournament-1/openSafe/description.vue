<template>
	<div class='description'>
		<p class="description__content">
			Для того чтобы кодовый замок открылся, нужно набрать три цифры - код. 
			Сделали несколько неверных попыток. Справа от попытки написана подсказка. 
			Разгадайте код и откройте кодовый замок. Выберите нужную комбинацию цифр с 
			помощью красных стрелок.
			У вас всего одна попытка. 
		</p>
		<div class="description__map">
			<div class="map__item">
				<p class="item__var"> n </p>
				<div class="circle_yellow circle"></div>
				<p class="item__description">
					Говорит о том, что n цифр угаданы верно, но находятся не на своём месте
				</p>
			</div>
			<div class="map__item">
				<p class="item__var"> m </p>
				<div class="circle_green circle"></div>
				<p class="item__description">
					Говорит о том, что m цифр угаданы верно и находятся на своём месте
				</p>
			</div>
			<div class="map__item">
				<p class="item__var">   </p>
				<div class="circle_red circle"></div>
				<p class="item__description">
					Говорит о том, что верных цифр нет
				</p>
			</div>
		</div>
	</div>
</template>

<style scoped>
.circle {
	width: 30px;
	min-width: 30px;
	height: 30px;
	border-radius: 100%;
}

.circle_green {
	background-color: rgba(124, 224, 1, 1);
}

.circle_red {
	background-color: rgba(219, 60, 32, 1);
}

.circle_yellow {
	background-color: rgba(240, 204, 0, 1);
}

.description__map {
	display: inline-flex;
	flex-direction: column;
	gap: 20px;
	margin-top: 40px;
}

.map__item {
	display: inline-flex;
}

.item__var {
	width: 40px;
}

.item__description {
	padding-left: 40px;
}
</style>
