<template>
  <TopBar></TopBar>
  <div class="min-h-screen transition-colors duration-300" :style="pageStyle">
    <div class="header-bar">
      <h1>{{boardName}}</h1>
      <div class="flex items-center gap-4">
        <UAvatarGroup size="sm" max="5">
          <UAvatar v-for="member in members" :key="member.id" :src="member.profile_picture" :alt="member.username" :title="member.email" />
        </UAvatarGroup>
        <UModal title="Share Board" :ui="{ body: 'bg-[var(--secondary-grey)]', content: 'bg-[var(--secondary-grey)] ring-0', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
          <UButton label="Open" icon="i-lucide-share-2" color="info" variant="solid">Share</UButton>
          <template #body>
            <UCard :ui="{ body: 'bg-[var(--secondary-grey)]', root:' ring-0'}">
              <div class="space-y-4">
                <UInput v-model="inviteEmail" placeholder="Email address" type="email" size="lg" color="info" :ui="{ base: 'bg-[var(--secondary-grey)] border-[var(--text-color)] w-100'}"/>
                <UCheckbox v-model="inviteAdmin" color="info" label="Give admin access" />
              </div>
              <div class="flex justify-end gap-2">
                <UButton color="info" :loading="inviteLoading" :disabled="!inviteEmail" @click="invite"> Invite </UButton>
              </div>
            </UCard>
            <div class="space-y-2">
              <div v-for="member in members" :key="member.id" class="flex items-center justify-between p-2 rounded-md bg-[var(--secondary-grey)]">
                <div class="flex items-center gap-3">
                  <UAvatar :src="member.profile_picture" :alt="member.email" size="sm"/>
                  <div class="flex flex-col">
                    <span class="text-sm font-medium">
                      {{ member.email }}
                    </span>
                    <span class="text-xs opacity-70">
                      {{ admins.some(a => a.email === member.email) ? 'Admin' : 'Member' }}
                    </span>
                  </div>
                </div>
                <UModal v-model="confirmOpen" title="Remove member" description="Are you sure you want to remove this member from the board?" :ui="{ body: 'bg-[var(--secondary-grey)]', content: 'bg-[var(--secondary-grey)] ring-0 w-80', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                  <UButton v-if="member.email !== boardOwnerEmail" icon="i-lucide-x" size="xs" color="error" variant="ghost" @click="askRemoveMember(member.email)"/>
                    <template #body>
                      <div class="flex justify-center gap-2">
                      <UButton color="error" @click="confirmRemoveMember"> Remove </UButton>
                    </div>
                  </template>
                </UModal>
              </div>
            </div>
          </template>
        </UModal>
        <UPopover title="Archived task" :content="{side: 'bottom', sideOffset: 8 }" :ui="{content: 'bg-[var(--main-grey)] w-70 px-6 py-4'}">
          <UButton icon="i-lucide-archive" color="secondary" variant="ghost"/>
          <template #content>
            <div class="flex justify-center gap-4 mb-4">
              <h2 class="text-highlighted font-semibold">
                Archived tasks
              </h2>
            </div>
            <div v-if="archivedTasks.length === 0" class="text-sm opacity-70 text-center py-6">
              No archived tasks
            </div>

            <div v-else class="space-y-4">
              <div v-for="task in archivedTasks" :key="task.id">
              <div class="bg-[var(--secondary-grey)] rounded-lg p-2 text-sm shadow cursor-pointer hover:bg-[var(--ui-hover)]" @click="openArchivedTask(task)">
                {{ task.title }}
              </div>
                <div class="flex gap-0 mt-1">
                  <UButton size="xs" color="info" variant="ghost" @click.stop="restoreTask(task)">Restore</UButton>
                  <UButton size="xs" color="error" variant="ghost" @click.stop="deleteTask(task)">Delete</UButton>
                </div>
              </div>
            </div>
          </template>
        </UPopover>
      </div>
    </div>
    <ClientOnly>
      <Board v-if="board" v-model:board="board" @updated="getBoardData"/>
    </ClientOnly>
  </div>
  <TaskModal v-if="selectedTask" :open="taskModalOpen" :task="selectedTask" :boardID="boardID!" :categories="board.map(c => c.id)" @close="taskModalOpen = false" :archived="true" @updated="getBoardData"/>
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
const boardColor = ref<string | null>(null)
  const textColor = computed(() => {
  if (!boardColor.value) return 'var(--text-color)'

  const luminance = getLuminance(boardColor.value)

  return luminance > 0.55 ? '#111827' : '#F9FAFB'
})
const pageStyle = computed(() => {
  if (!boardColor.value) return {}

  return {
    backgroundColor: boardColor.value,
    '--text-color': textColor.value
  }
})

const shareOpen = ref(false)
const inviteEmail = ref('')
const inviteAdmin = ref(false)
const inviteLoading = ref(false)
const members = ref<any[]>([])
const admins = ref<any[]>([])
const confirmOpen = ref(false)
const memberToRemove = ref<string | null>(null)
const boardOwnerEmail = ref<string | null>(null)

const archivedTasks = ref<Task[]>([])
const selectedTask = ref<Task | null>(null)
const taskModalOpen = ref(false)

const getBoardData = async () => {
  if (!auth.authenticated || !auth.jwt || !boardID.value) return
  api.setjwt(auth.jwt)
  const data = await api.getBoardData(boardID.value).catch((error) => {
    console.error(error);
  });
  boardName.value = data.title
  boardColor.value = data.color ?? null
  members.value = data.members
  admins.value = data.admin ?? []
  boardOwnerEmail.value = data.owner.email

  archivedTasks.value = [...(data.archived ?? [])].sort(
  (a: any, b: any) =>
    new Date(b.date_creation).getTime() -
    new Date(a.date_creation).getTime()
  )

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

    inviteEmail.value = ''
    inviteAdmin.value = false
    shareOpen.value = false
  } catch (err) {
    console.error(err)
  } finally {
    inviteLoading.value = false
    getBoardData()
  }
}

function askRemoveMember(email: string) {
  memberToRemove.value = email
  confirmOpen.value = true
}

async function confirmRemoveMember() {
  if (!memberToRemove.value || !boardID.value) return

  try {
    await api.deleteMember(boardID.value, memberToRemove.value)
    members.value = members.value.filter(
      m => m.email !== memberToRemove.value
    )
  } catch (err) {
    console.error(err)
  } finally {
    confirmOpen.value = false
    memberToRemove.value = null
  }
}

onMounted(async () => {
  await getBoardData();
})

function hexToRgb(hex: string) {
  const normalized = hex.replace('#', '')
  const bigint = parseInt(normalized, 16)

  return {
    r: (bigint >> 16) & 255,
    g: (bigint >> 8) & 255,
    b: bigint & 255,
  }
}

function getLuminance(hex: string) {
  const { r, g, b } = hexToRgb(hex)

  return (0.299 * r + 0.587 * g + 0.114 * b) / 255
}

function openArchivedTask(task: Task) {
  selectedTask.value = { ...task }
  taskModalOpen.value = true
}

async function restoreTask(task: Task) {
  if (!boardID.value) return

  try {
    await api.restoreArchive(boardID.value, task.id)
    await getBoardData()
  } catch (err) {
    console.error(err)
  }
}

async function deleteTask(task: Task) {
  if (!boardID.value) return

  try {
    await api.deleteArchive(boardID.value, task.id)

    archivedTasks.value = archivedTasks.value.filter(t => t.id !== task.id)
  } catch (err) {
    console.error(err)
  }
}
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
