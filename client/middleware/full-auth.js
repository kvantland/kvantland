export default async function({$axios, redirect, $auth}) {
    if (!$auth.loggedIn)
        return redirect('/login')
    else{
        let resp = {
            status: false,
        }
        await $axios.$post('/api/is_user_info_full')
        .then((res) => {resp = res})
        if (!resp.status)
            return redirect('/acc/editInfo?globalError=fillFields')
    }
}