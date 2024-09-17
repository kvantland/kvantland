<template>
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
			M -40 0
			a 40 40 0 0 0 40 40 
			a 40 40 0 0 0 40 -40
			a 40 40 0 0 0 -40 -40
			a 40 40 0 0 0 -40 40
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
</template>