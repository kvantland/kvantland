import { Oauth2Scheme } from "~auth/runtime";

function parseQuery(query) {
	const query_arr = query.split('&')
	const resp = {}
	for (const item of query_arr) {
		const [param, value] = item.split('=')
		resp[param] = value
	}
	return resp
}

function encodeQuery(opts) {
	let query = ""
	for (const opt in opts) {
		query += '&' + encodeURIComponent(opt) + '=' + encodeURIComponent(opts[opt])
	}
	return query.substring(1)
}

export default class LocalOauth2Scheme extends Oauth2Scheme {
	async login({state, params, nonce} = {}){ 
		console.log('login!')

        const PKCE = await this.$auth.request({
			method: 'post',
			url: this.options.endpoints.PKCEurl,
		})

		console.log(PKCE.data)

		const opts = {
			response_type: this.options.responseType,
			client_id: this.options.clientId,
			redirect_uri: this.options.redirectUri,
			scope: this.options.scope,
			state: this.options.state,
            code_challenge: PKCE.data.code_challenge,
            code_challenge_method: this.options.codeChallengeMethod,    
		}
            
		this.$auth.$storage.setUniversal(this.name + '.state', opts.state)
        this.$auth.$storage.setUniversal(this.name + '.code_verifier', PKCE.data.code_verifier)

		const url = this.options.endpoints.authorization + '?' + encodeQuery(opts)
        console.log(url)
		window.location.replace(url)
	}

	async fetchUser(classes = "all") {
		console.log('fetch!!', classes)
		if (!this.check().valid) {
			return
		}
	  
		if (!this.options.endpoints.userInfo) {
			this.$auth.setUser({})
			return
		}

		const response = await this.$auth.request({
			method: 'get',
			url: this.options.endpoints.userInfo + '?' + `classes=${classes}`
		})

		this.$auth.setUser(response.data[this.options.user.property])
	}

	async _handleCallback() {
		if (this.check().valid) {
			console.log('Authorized!')
			return
		}
		console.log('first!')
		// Handle callback only for specified route
	   /* if (
			this.$auth.options.redirect &&
			this.$auth.ctx.route.path != this.$auth.options.redirect.callback
		) {
			return
		} */

		// Callback flow is not supported in server side
		if (process.server) {
		  return
		}

        console.log(this.$auth.ctx.route)
		const parsedQuery = this.$auth.ctx.route.query
		const vk_code = parsedQuery[this.options.code.property]
		const device_id = parsedQuery[this.options.deviceId.property]
        const code_verifier = this.$auth.$storage.getUniversal(this.name + '.code_verifier')
		console.log(vk_code, device_id, code_verifier)

		if (!(vk_code || device_id))
			return
	
		// Validate state
		const state = this.$auth.$storage.getUniversal(this.name + '.state')
		this.$auth.$storage.setUniversal(this.name + '.state', null)
		if (state && parsedQuery.state !== state) {
		  return
		}

        console.log('state approved!')

        const resp = await this.$auth.request({
            method: 'post',
            url: this.options.endpoints.apiLogin,
            data: {
                device_id,
                code: vk_code,
                code_verifier,
                state: this.options.state,
            }
        })

		if (!resp.data.user_exists) {
			console.log('user not exists!')
			const redirect_to_acc = `/acc/editInfo?${encodeQuery({'user_info': JSON.stringify(resp.data.user_info), 
				'request': "oauthReg", 'globalError':"fillFields"})}`
			console.log(redirect_to_acc)
			window.location.replace(redirect_to_acc)
			return true
		}
		else if (resp.data.tokens) {
                console.log(resp.data.tokens)
                this.token.set(resp.data.tokens[this.options.accessToken.property])
		        this.refreshToken.set(resp.data.tokens[this.options.refreshToken.property])
				// this.$auth.setUserToken(resp.data.tokens.access_token, resp.data.tokens.refresh_token)
			}
		/* this.token.set(resp.data.tokens[this.options.accessToken.property])
		this.refreshToken.set(resp.data.tokens[this.options.refreshToken.property]) */
		if (this.$auth.options.watchLoggedIn) {
			await this.fetchUser()
			this.$auth.redirect('home', true)
			return true // True means a redirect happened
		}
	}

    async refreshTokens() {
        console.log('refresh attempt!')
        // Get refresh token
        let refreshToken
        try {
            refreshToken = this.refreshToken.get()
        }
        catch(e) {
            return
        }
        // Refresh token is required but not available
        if (!refreshToken) {
            return
        }

        // Get refresh token status
        const refreshTokenStatus = this.refreshToken.status()
        const accessTokenStatus = this.accessToken.status()

        // Refresh token is expired. There is no way to refresh. Force reset.
        if (refreshTokenStatus.expired()) {
            this.$auth.reset()
            throw new ExpiredAuthSessionError()
        }

        if (!accessTokenStatus.expired()) {
            return
        }
        
        // Delete current token from the request header before refreshing
        this.requestHandler.clearHeader()

        const resp = await this.$auth.request({
            method: 'post',
            url: this.options.endpoints.refresh,
            baseURL: '',
            data: {
                refresh_token: refreshToken
            },
        })
        .catch((error) => {
            this.$auth.callOnError(error, { method: 'refreshToken' })
            return Promise.reject(error)
          })
    
        this.updateTokens(resp)
    }

	updateTokens(response) {
		console.log('update tokens!')
		const accessToken = response.data[this.options.accessToken.property]
		const refreshToken = response.data[this.options.refreshToken.property]
		this.token.set(accessToken)
		this.refreshToken.set(refreshToken)
	}
}
