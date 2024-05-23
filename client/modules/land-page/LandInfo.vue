<template>
	<svg class="map" version="1.1" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
		<defs>
			<clipPath id="map_border">
				<path d="
						M 0 20
						v 680
						a 20 20 0 0 0 20 20
						h 1240
						a 20 20 0 0 0 20 -20
						v -680
						a 20 20 0 0 0 -20 -20
						h -1240
						a 20 20 0 0 0 -20 20
						z" />
			</clipPath>

			<clipPath id="icon_border">
				<path d="
						M -30 0
						a 30 30 0 0 0 30 30 
						a 30 30 0 0 0 30 -30
						a 30 30 0 0 0 -30 -30
						a 30 30 0 0 0 -30 30
						z" />
			</clipPath>
			<filter id="dropshadow" height="130%">
				<feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
				<feOffset dx="2" dy="2" result="offsetblur"/>
				<feComponentTransfer>
					<feFuncA type="linear" slope="0.5"/>
				</feComponentTransfer>
				<feMerge>
					<feMergeNode/>
					<feMergeNode in="SourceGraphic"/>
				</feMerge>
			</filter>
		</defs>

		<image href="../../../static/map/land.png" width="1280" height="720" preserveAspectRatio="xMinYMin" clip-path="url(#map_border)" meet/>
	
	</svg>
</template>