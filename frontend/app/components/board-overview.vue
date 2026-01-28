<template>
  <div class="board-overview group relative cursor-pointer">
    <button v-if="favorite" class="absolute top-2 right-2 z-10"
      @click.stop="toggleFavorite">
      <UIcon name="i-lucide-star" class="w-5 h-5 cursor-pointer" :class="favorite ? 'text-yellow-400 fill-yellow-400' : 'text-white/80 hover:text-yellow-400'"/>
    </button>
    <button v-else class="absolute top-2 right-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
      @click.stop="toggleFavorite">
      <UIcon name="i-lucide-star" class="w-5 h-5" :class="favorite ? 'text-yellow-400 fill-yellow-400' : 'text-white/80 hover:text-yellow-400'"/>
    </button>
    <div class="board-overview-header" :style="{ backgroundColor: color }"/>
      <div class="board-overview-body">
        {{ title }}
      </div>
    </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth'

const props = defineProps<{
  id: string
  color: string
  title?: string
  favorite?: boolean
}>()

const emit = defineEmits<{
  (e: 'favorite-changed', value: boolean): void
}>()

const auth = useAuthStore()
const { $bridge } = useNuxtApp()
const api = $bridge
const toast = useToast()

async function toggleFavorite() {
  if (!auth.jwt) return

  try {
    api.setjwt(auth.jwt)
    await api.favoriteBoard(props.id, !props.favorite)
    emit('favorite-changed', !props.favorite)
  } catch (err) {
    console.error(err)
    toast.add({
      title: 'Error',
      description: 'Failed to add board to favorites.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
  }
}
</script>


<style>
.board-overview {
    display: flex;
    flex-direction: column;
    width: 220px;
    height: 128px;
    transition: box-shadow 0.2s ease;
    box-shadow: 0px 0px 5px 0px rgba(0,0,0,0.65);
    border-radius: 8px;
}

.board-overview:hover {
  box-shadow: 0px 0px 12px 0px rgba(0,0,0,1);
}

.board-overview-header {
    width: 220px;
    height: 82px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

.board-overview-body{
    height: 56px;
    padding: 8px;
    color: var(--text-color);
    font-size: 14px;
    overflow: scroll;
}
</style>