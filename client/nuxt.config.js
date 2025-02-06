export default {
	server: {
		port: 80 // default: 3000
		},
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
	title: 'Квантладия',
	htmlAttrs: {
	  lang: 'en',
	},
	meta: [
	  { charset: 'utf-8' },
	  { name: 'viewport', content: 'width=device-width, initial-scale=1' },
	  { hid: 'description', name: 'description', content: '' },
	  { name: 'format-detection', content: 'telephone=no' },
	],
	link: [
		{ rel: 'icon', type: 'image/svg', href: '/favicon.svg' },
		],
	script: [
		{
			type: "text/javascript",
			id: "MathJax-script",
			src: "https://cdn.jsdelivr.net/npm/mathjax@3.0.1/es5/tex-mml-chtml.js"
		},
		{
			src: 'https://mc.yandex.ru/metrika/tag.js',
			async: true,
		},
		{
			innerHTML: `
				(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
				m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
				(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

				ym(96847675, "init", {
					clickmap:true,
					trackLinks:true,
					accurateTrackBounce:true,
					webvisor:true
				});
			`,
			type: 'text/javascript',
			charset: 'utf-8',
		},
	],
	__dangerouslyDisableSanitizers: ['script']
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ["@assets/css/master.css"],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: {
	dirs: [
		'~components',
		{
			path: '~UI/',
			prefix: false,
		},
		{
			path: '~UI/Headers',
			prefix: false,
		},
	] 
  },

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
	// https://go.nuxtjs.dev/typescript
	'@nuxt/typescript-build',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
	// https://go.nuxtjs.dev/axios
  ],
  // Axios module configuration: https://go.nuxtjs.dev/config-axios

  // Build Configuration: https://go.nuxtjs.dev/config-build
	build: {},

  target: 'static',
}

