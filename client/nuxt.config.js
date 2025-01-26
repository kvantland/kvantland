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
			path: '~UI/Form',
			prefix: false,
		},
		{
			path: '~UI/Headers',
			prefix: false,
		},
		{
			path: '~static/problemModules/components',
			prefix: false,
		}
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
  
  layout: 'default',
}

