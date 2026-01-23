import { useAuthStore } from '~/store/auth'

export function useBoardSocket(boardID: string) {
    const auth = useAuthStore()
    const socket = ref<WebSocket | null>(null)

    function connect() {
        if (!auth.jwt) return
        console.log("function connect")

        socket.value = new WebSocket(
            `ws://localhost:5080/ws/board/${boardID}/`
        )

        socket.value.onopen = () => {
            console.log("on open")
            socket.value?.send(JSON.stringify({
                type: 'login',
                Authorization: `Bearer ${auth.jwt}`
            }))
        }

        socket.value.onmessage = (event) => {
            const data = JSON.parse(event.data)
            console.log('[WS]', data)
        }

        socket.value.onerror = (err) => {
            console.error('[WS error]', err)
        }

        socket.value.onclose = () => {
            console.warn('[WS closed]')
        }
    }

    function disconnect() {
        socket.value?.close()
    }

    return { connect, disconnect }
}
