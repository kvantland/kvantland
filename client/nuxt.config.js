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
			src: '/jsLibraries/jQuery/jquery-3.7.1.js',
		},
		{
			defer: true,
			type: "text/javascript",
			id: "MathJax-script",
			src: "https://cdn.jsdelivr.net/npm/mathjax@3.0.1/es5/tex-mml-chtml.js"
		},
	],
	__dangerouslyDisableSanitizers: ['script']
  },

  publicRuntimeConfig: {
	recaptcha: {
		siteKey: process.env.RECAPTCHA_SITE_KEY,
		version: 2,
	},
	tournamentMode: process.env.MODE || 'private',
	tournamentType: process.env.TOURNAMENT_TYPE || 'math',
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
	'@nuxtjs/axios',
	'@nuxtjs/auth-next',
	'@nuxtjs/recaptcha', 
	'@nuxtjs/proxy',
  ],
  proxy: {
		'/api/': {
			target: process.env.API,
		}
  },
  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
		proxy: true,
		baseUrl: process.env.API
	// Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
  },

  auth: {
	watchLoggedIn: true,
	redirect: {
		login: '/login',
		logout: '/',
		home: '/',
		callback: '/login',
	},
	strategies: {
	  local: {
		scheme: '~auth-schemes/localForClasses',
		token: {
		  property: 'access_token',
		  global: true,
		  type: 'Bearer',
		  maxAge: 1800,
		},
		refreshToken: {
			property: 'refresh_token',
			data: 'refresh_token',
			maxAge: 60 * 60 * 24 * 30,
		},
		user: {
		  property: 'user',
		},
		endpoints: {
		  login: { url: '/api/check_login', method: 'post' },
		  logout: false,
		  user: { url: '/api/user', method: 'get'},
		  refresh: { url: '/api/refresh_tokens', method: 'post'}
		},
	  },
	  vk: {
		scheme: '~auth-schemes/localAuthO',
		endpoints: {
			authorization: 'https://id.vk.com/authorize',
			apiLogin: `${process.env.API}/api/vk_auth`,
			userInfo: `${process.env.API}/api/user`,
			PKCEurl: `${process.env.API}/api/vk_PKCE`,
			refresh: '/api/refresh_tokens', 
		},
		deviceId: {
			property: 'device_id',
		},
		code: {
			property: 'code',
		},
		accessToken: {
			property: 'access_token',
			maxAge: 61,
		},
		refreshToken: {
			property: 'refresh_token',
			data: 'refresh_token',
			maxAge: 60 * 60 * 24 * 30,
		},
		user: {
			property: 'user',
		},
		responseType: 'code',
		scope: [],
		clientId: process.env.VK_CLIENT,
		codeChallengeMethod: 's256',
		redirectUri: process.env.BASE_URL,
		state: 'VK',
	  }
	},
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  generate: {
	routes() {
		const problemRoutes = []
		const townRoutes = []
		const landRoutes = []
		for (const classNum of ['1-3', '4-6', '7-9']) {
			for (let variantNum = 1; variantNum <= 300; variantNum++) {
				problemRoutes.push(`/class/${classNum}/problem/${process.env.TOURNAMENT * 1000 + variantNum}`)
			}
			for (let townNum = 1; townNum <= 5; townNum++) {
				townRoutes.push(`/class/${classNum}/town/${townNum}`)
			}
			landRoutes.push(`/class/${classNum}/land`)
		}
		return [...problemRoutes,
			...townRoutes,
			...landRoutes
		]
		}
  },

  target: 'static',
  
  layout: 'default',
}

