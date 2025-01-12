import { RefreshScheme } from "~auth/runtime"

export default class LocalForClassesScheme extends RefreshScheme {
	async fetchUser(classes = "all") {
		console.log("fetch!!")
		if (!this.check().valid) {
			return
		}
	  
		if (this.$auth.$storage.getUniversal("classes") && classes === "all") {
			classes = this.$auth.$storage.getUniversal("classes")
		}
		else if (classes !== "all") {
			this.$auth.$storage.setUniversal("classes", classes)
		}

		if (!this.options.endpoints.user) {
			this.$auth.setUser({})
			return
		}

		const response = await this.$auth.request({
			method: 'get',
			url: this.options.endpoints.user.url + '?' + `classes=${classes}`
		})
		console.log(response)
		this.$auth.setUser(response.data[this.options.user.property])
	}
}