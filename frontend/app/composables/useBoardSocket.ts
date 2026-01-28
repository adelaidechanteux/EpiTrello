import { ref, onBeforeUnmount } from 'vue'
import { useAuthStore } from '~/store/auth'

export function useBoardSocket(boardID: string, uri: string) {
    const socket = ref<WebSocket | null>(null)
    const connected = ref(false)
    const auth = useAuthStore()

    const connect = () => {
        if (!boardID || !auth.jwt) return

        socket.value = new WebSocket(
            `ws://${uri}/ws/board/${boardID}/`
        )

        socket.value.onopen = () => {
            console.log('[WS] connected')

            socket.value?.send(JSON.stringify({
                type: 'login',
                Authorization: `Bearer ${auth.jwt}`
            }))

            connected.value = true
        }

        socket.value.onclose = () => {
            console.log('[WS] disconnected')
            connected.value = false
        }

        socket.value.onerror = (err) => {
            console.error('[WS] error', err)
        }

        socket.value.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data)
                handleMessage(data)
            } catch {
                console.warn('[WS] invalid JSON', event.data)
            }
        }
    }

    const disconnect = () => {
        socket.value?.close()
        socket.value = null
    }

    onBeforeUnmount(disconnect)

    let handleMessage = (_: any) => { }

    const onMessage = (fn: (data: any) => void) => {
        handleMessage = fn
    }

    return {
        connect,
        disconnect,
        connected,
        onMessage
    }
}
