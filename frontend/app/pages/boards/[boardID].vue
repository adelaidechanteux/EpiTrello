<template>
    <TopBar></TopBar>
    <ClientOnly>
      <Board v-if="board" v-model:board="board" />
    </ClientOnly>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth'
import type { Column } from '~/composables/types/board'

const route = useRoute()
const boardID = computed(() => {
  const id = route.params.boardID
  return Array.isArray(id) ? id[0] : id
})


const { $bridge } = useNuxtApp()
const api = $bridge

const auth = useAuthStore()
const board = ref<Column[]>([])

const getBoardData = async () => {
  if (!auth.authenticated || !auth.jwt || !boardID.value) return
  api.setjwt(auth.jwt)
  const data = await api.getBoardData(boardID.value).catch((error) => {
    console.error(error);
  });
  board.value = data.categories.map((category: string) => ({
    id: category,
    title: category,
    cards: data.tasks
      .filter((t: any) => t.category === category)
      .map((t: any) => ({
        id: t.id,
        title: t.title,
      })),
  }))
}

onMounted(async () => {
  await getBoardData();
})


</script>
