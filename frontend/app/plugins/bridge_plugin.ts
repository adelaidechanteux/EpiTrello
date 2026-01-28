import { defineNuxtPlugin } from '#app'
import { bridge } from '~/composables/service/bridge'

const bridgeInstance = new bridge()

export default defineNuxtPlugin(() => {
  const requestUrl = useRequestURL();
  (bridgeInstance as bridge).seturl(`${requestUrl.protocol}//${requestUrl.hostname}:${requestUrl.port}`);
  return {
    provide: {
      bridge: bridgeInstance as bridge
    }
  }
})
