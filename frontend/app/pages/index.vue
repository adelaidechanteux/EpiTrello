<template>
    <TopBar></TopBar>
    <UPage>
    <UPageBody>
      <UContainer class="max-w-[914px] w-[914]">
        <div v-if="favoriteBoards.length">
          <h3 class="section-title">Favorites</h3>
          <div class="board-overview-container">
            <BoardOverview v-for="board in favoriteBoards" :key="board.id" :id="board.id" :title="board.title" :color="board.color" :favorite="true" @favorite-changed="getBoards" @click="router.push(`/boards/${board.id}`)"/>
          </div>
        </div>
        <div v-if="ownedBoards.length" class="mt-8">
          <h3 class="section-title">Owned boards</h3>
          <div class="board-overview-container">
            <BoardOverview v-for="board in ownedBoards" :key="board.id" :id="board.id" :title="board.title" :color="board.color" :favorite="false" @favorite-changed="getBoards" @click="router.push(`/boards/${board.id}`)"/>
          </div>
        </div>
        <div v-if="otherBoards.length" class="mt-8">
          <h3 class="section-title">Shared with you</h3>
          <div class="board-overview-container">
            <BoardOverview v-for="board in otherBoards" :key="board.id" :id="board.id" :title="board.title" :color="board.color" :favorite="false" @favorite-changed="getBoards" @click="router.push(`/boards/${board.id}`)"/>
          </div>
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
const loading = ref(false)

const router = useRouter()

const favoriteBoards = ref<any[]>([])
const ownedBoards = ref<any[]>([])
const otherBoards = ref<any[]>([])

async function getBoards() {
  if (!auth.authenticated || !auth.user.id) return

  api.setjwt(auth.jwt)
  loading.value = true

  try {
    const response = await api.getBoards()

    favoriteBoards.value = response.favorite ?? []
    const favoriteIds = new Set(favoriteBoards.value.map(b => b.id))

    ownedBoards.value = (response.owned ?? []).filter(
      (b: any) => !favoriteIds.has(b.id)
    )
    const ownedIds = new Set(ownedBoards.value.map(b => b.id))

    otherBoards.value = (response.boards ?? []).filter(
      (b: any) =>
        !favoriteIds.has(b.id) &&
        !ownedIds.has(b.id)
    )
  } finally {
    loading.value = false
  }
}

onMounted(getBoards)
</script>

<style>
.board-post {
    width: 220px;
}

.board-overview-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    padding: 0px 70px;
    row-gap: 12px;
    column-gap: 18px;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 12px;
  opacity: 0.85;
  padding: 12px 40px;
}

</style>