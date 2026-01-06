<template>
    <TopBar></TopBar>
    <UPage>
    <UPageHeader title="Your boards" class="flex justify-center items-center text-center"/>
    <UPageBody>
      <UContainer class="max-w-[914px] w-[914]">
        <div class="board-overview-container">
          <BoardOverview v-for="(board, index) in boards" :key="board.id || index" v-bind="board" @click="router.push(`/boards/${board.id}`)"/>
        </div>
      </UContainer>
    </UPageBody>
  </UPage>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/store/auth'

const { $bridge } = useNuxtApp()
const api = $bridge

const auth = useAuthStore()
const boards = ref<any[]>([])
const loading = ref(false)

const router = useRouter()

onMounted(async () => {
  if (!auth.authenticated || !auth.user.id) return

  api.setjwt(auth.jwt);

  loading.value = true;
  try {
    const response = await api.getBoards();
    boards.value = response.boards;
  } finally {
    loading.value = false;
  }
})
</script>

<style>
.board-post {
    width: 220px;
}

.board-overview-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    row-gap: 12px;
    column-gap: 12px;
}
</style>