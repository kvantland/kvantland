export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'client',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/svg', href: '/favicon.svg' }],
  },

  publicRuntimeConfig: {
    recaptcha: {
        siteKey: process.env.RECAPTCHA_SITE_KEY,
        version: 2,
    }
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
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: process.env.API,
  },

  auth: {
    watchLoggedIn: true,
    redirect: {
        login: '/login',
        logout: '/',
        home: '/',
        callback: '/'
    },
    strategies: {
      local: {
        token: {
          property: 'token',
          global: true,
          type: 'Bearer'
        },
        user: {
          property: 'user',
        },
        endpoints: {
          login: { url: '/api/check_login', method: 'post' },
          logout: false,
          user: { url: '/api/user', method: 'get'},
        },
      },
      vk: {
        scheme: '~auth-schemes/localAuthO',
        endpoints: {
            authorization: 'http://oauth.vk.com/authorize',
            apiLogin: `${process.env.API}/api/vk_auth`,
            userInfo: `${process.env.API}/api/user`,
        },
        userId: {
            property: 'user_id',
        },
        token: {
            property: 'access_token',
        },
        accessToken: {
            property: 'access_token',
        },
        refreshToken: {
            property: 'refresh_token',
        },
        user: {
            property: 'user',
        },
        responseType: 'token',
        scope: [],
        clientId: process.env.VK_CLIENT,
        codeChallengeMethod: '',
        redirectUri: `${process.env.BASE_URL}/`,
        state: 'VK',
      }
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  layout: 'default',
}
