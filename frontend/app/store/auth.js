import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        authenticated: false,
        loading: false,
        user: {
            id: '',
            username: '',
            profile_picture: '',
            email: '',
        },
    }),
    actions: {
        async authenticateUser(credential, user) {

            if (credential) {
                const token = useCookie('token');
                token.value = credential;
                this.authenticated = true;
            }
            if (user) {
                this.user = user;
                console.log("this in auth")
                console.log(this.user)
            }
        },
        logUserOut() {
            const token = useCookie('token');
            this.authenticated = false;
            token.value = null;
        },
    },
    persist: {
        storage: piniaPluginPersistedstate.localStorage(),
    },
});