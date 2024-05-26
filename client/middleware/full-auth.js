export default function({$axios, redirect, store}) {
    if (!store.state.authenticated)
        return redirect('/login')
    else{
        const resp = $axios.$post('/api/is_user_info_full')
        if (!resp['status'])
            return redirect('/acc/editInfo')
    }
    console.log(resp)
}