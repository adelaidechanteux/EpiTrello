import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  modules: [
    'nuxt-vue3-google-signin',
    '@nuxt/ui',
    '@pinia/nuxt',
    'pinia-plugin-persistedstate/nuxt'
  ],
  css: ['~/assets/css/main.css'],
  googleSignIn: {
    clientId: '119555573006-0pmpdnm96mbodsg37td3v7tu4sbfunuq.apps.googleusercontent.com',
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true }
})