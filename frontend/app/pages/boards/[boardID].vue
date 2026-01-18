<template>
    <TopBar></TopBar>
    <div class="header-bar">
      <h1>{{boardName}}</h1>
      <UModal title="Share Board" :ui="{ body: 'bg-[var(--secondary-grey)]', content: 'bg-[var(--secondary-grey)] ring-0', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]'}">
        <UButton label="Open" icon="i-lucide-share-2" color="info" variant="solid">Share</UButton>
        <template #body>
          <UCard :ui="{ body: 'bg-[var(--secondary-grey)]', root:' ring-0'}">
            <div class="space-y-4">
              <UInput v-model="inviteEmail" placeholder="Email address" type="email" color="info" :ui="{ base: 'bg-[var(--secondary-grey)] border-[var(--text-color)]'}"/>
              <UCheckbox v-model="inviteAdmin" color="info" label="Give admin access" />
            </div>
              <div class="flex justify-end gap-2">
                <UButton color="info" :loading="inviteLoading" :disabled="!inviteEmail" @click="invite"> Invite </UButton>
            </div>
        </UCard>
      </template>
      </UModal>
    </div>
  <ClientOnly>
    <Board v-if="board" v-model:board="board" @updated="getBoardData"/>
  </ClientOnly>
</template>

<script setup lang="ts">
  import { useAuthStore } from '~/store/auth'
import type { Task, Column } from '~/composables/types/board'

const route = useRoute()
const boardID = computed(() => {
  const id = route.params.boardID
  return Array.isArray(id) ? id[0] : id
})

const { $bridge } = useNuxtApp()
const api = $bridge

const auth = useAuthStore()
const board = ref<Column[]>([])
const boardName = ref('')

const shareOpen = ref(false)
const inviteEmail = ref('')
const inviteAdmin = ref(false)
const inviteLoading = ref(false)

const getBoardData = async () => {
  if (!auth.authenticated || !auth.jwt || !boardID.value) return
  api.setjwt(auth.jwt)
  const data = await api.getBoardData(boardID.value).catch((error) => {
    console.error(error);
  });
  boardName.value = data.title
  board.value = data.categories.map((category: string) => ({
  id: category,
  title: category,
  cards: data.tasks.filter((t: any) => t.category === category),
  }))
}

async function invite() {
  if (!inviteEmail.value || !boardID.value) return

  inviteLoading.value = true
  try {
    await api.InviteBoard(
      boardID.value,
      inviteEmail.value,
      inviteAdmin.value
    )

    // reset + close
    inviteEmail.value = ''
    inviteAdmin.value = false
    shareOpen.value = false
  } catch (err) {
    console.error(err)
  } finally {
    inviteLoading.value = false
  }
}

onMounted(async () => {
  await getBoardData();
})

</script>

<style scoped>
.header-bar {
    display: flex;
    align-items: center;
    height: fit-content;
    padding: 12px 24px;
    justify-content: space-between;
    background-color: rgba(255, 255, 255, 0.164);
}

</style>
