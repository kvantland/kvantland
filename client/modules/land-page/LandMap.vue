<template>
	<svg class="map" version="1.1" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
		<LandDefs/>
		<image href="map_img/land.png" width="1280" height="720" preserveAspectRatio="xMinYMin" clip-path="url(#map_border)" meet/>
		<Towns/>
	</svg>
</template>
<script>
import LandDefs from "./components/LandDefs.vue"
import Towns from "./components/Towns.vue"
export default {
	middleware: 'full-auth',
	components: {
        LandDefs,
        Towns,
    },
}
</script>