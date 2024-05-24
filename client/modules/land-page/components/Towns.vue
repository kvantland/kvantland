<template v-for="twn in townsInfo">
	<a :class="twn.clazz" transform="translate({{twn.x}} {{twn.y}})" xlink:href="/town/{{twn.town}}/">
		<image href="/static/town-icon/icon-{{twn.town}}.png" x="-40px" y ="-40px" width="80px" clip-path="url(#icon_border)" />
		<circle class="town-icon" r="33px" />
		<g class="town-name">
			<path class="town-name" :num="twn.cnt" :d="paths[twn.cnt]" transform="translate({{trans[twn.cnt]}})" style="filter:url(#dropshadow)"/>
			<text class="town-name" style="font-family:Montserrat Alternates" :num="twn.cnt" y="-60">{{twn.name}}</text>
		</g>
	</a>
</template>
<script>
export default {
    data() {
        return {
            contacts: {},
            townsInfo:{},
        }
    },

    computed: {
        supportEmail() {
            try {
                let email = this.contacts.filter((contact) => contact.id == 'email')[0].source_link
                return { link: email, title: email.split(':')[1]}
            }
            catch {
                return { link: '', title: '' }
            }
        },
    },

    async fetch() {
        const townsInfoData = await this.$axios.$get('/api/towns_info')
        this.townsInfo = townsInfoData
    }
}
</script>