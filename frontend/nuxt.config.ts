import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  modules: [
    'nuxt-vue3-google-signin'
  ],
  googleSignIn: {
    clientId: '80772791160-5uj31qlmeraos15g0ukpp9o791r00jv0.apps.googleusercontent.com',
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true }
})