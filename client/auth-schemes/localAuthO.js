import { Oauth2Scheme } from "~auth/runtime";

function parseQuery(query) {
    let query_arr = query.split('&')
    let resp = {}
    for (let item of query_arr) {
        let [param, value] = item.split('=')
        resp[param] = value
    }
    return resp
}

function encodeQuery(opts) {
    let query = ""
    for (let opt in opts) {
        query += '&' + encodeURIComponent(opt) + '=' + encodeURIComponent(opts[opt])
    }
    return query.substring(1)
}

export default class LocalOauth2Scheme extends Oauth2Scheme {
    async login({state, params, nonce} = {}){ 
        const opts = {
            protocol: 'oauth2',
            response_type: this.options.responseType,
            access_type: this.options.accessType,
            client_id: this.options.clientId,
            redirect_uri: this.options.redirectUri,
            scope: this.options.scope,
            state: this.options.state,
            code_challenge_method: '',
        }
        this.$auth.$storage.setUniversal(this.name + '.state', opts.state)
        const url = this.options.endpoints.authorization + '?' + encodeQuery(opts)
        window.location.replace(url)
    }

    async fetchUser() {
        if (!this.check().valid) {
            return
        }
      
        if (!this.options.endpoints.userInfo) {
            this.$auth.setUser({})
            return
        }

        const response = await this.$auth.request({
            method: 'get',
            url: this.options.endpoints.userInfo
        })

        this.$auth.setUser(response.data[this.options.user.property])
    }

    async _handleCallback() {       
        // Callback flow is not supported in server side
        if (process.server) {
          return
        }
    
        const parsedQuery = parseQuery(this.$auth.ctx.route.hash.substr(1))
        const vk_token = parsedQuery[this.options.token.property]
        const user_id = parsedQuery[this.options.userId.property]
    
        // Validate state
        const state = this.$auth.$storage.getUniversal(this.name + '.state')
        this.$auth.$storage.setUniversal(this.name + '.state', null)
        if (state && parsedQuery.state !== state) {
          return
        }

        const resp = await this.$auth.request({
            method: 'post',
            url: this.options.endpoints.apiLogin,
            baseURL: '',
            data: {
                token: vk_token,
                user_id: user_id,
            }
        })

        if (!resp.data.tokens)
            return

        this.token.set(resp.data.tokens[this.options.accessToken.property])
        this.refreshToken.set(resp.data.tokens[this.options.refreshToken.property])
    }

    updateTokens(response) {
        console.log('update tokens!')
        const accessToken = response.data[this.options.accessToken.property]
        const refreshToken = response.data[this.options.refreshToken.property]
        this.token.set(accessToken)
        this.refreshToken.set(refreshToken)
    }
}
