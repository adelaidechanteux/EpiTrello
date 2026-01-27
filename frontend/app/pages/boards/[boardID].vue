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
        <UPopover :content="{side: 'bottom', sideOffset: 8 }" :ui="{content: 'bg-[var(--main-grey)] w-70 p-4'}">
          <UButton icon="i-lucide-ellipsis" color="secondary" variant="ghost"/>
          <template #content>
            <div class="flex flex-col items-center gap-4">
              <UModal title="Change Board Color" :ui="{ body: 'bg-[var(--secondary-grey)] flex flex-col items-center justify-center gap-2', content: 'bg-[var(--secondary-grey)] ring-0 w-60', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                <UButton label="Open" color="secondary" variant="ghost" size="md" :ui="{ base: 'rounded-sm w-60 text-[var(--text-color)]'}">Board Color</UButton>
                <template #body>
                  <UColorPicker v-model="color"></UColorPicker>
                  <UButton size="md" color="secondary" variant="ghost" :ui="{base: 'text-[var(--text-color)]'}" @click.stop="updateBoardColor()">Change</UButton>
                </template>
              </UModal>

              <UModal title="Change Board Name" :ui="{ body: 'bg-[var(--secondary-grey)] flex flex-col items-center justify-center gap-2', content: 'bg-[var(--secondary-grey)] ring-0 w-60', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                <UButton label="Open" color="secondary" variant="ghost" size="md" :ui="{ base: 'rounded-sm w-60 text-[var(--text-color)]'}">Board Name</UButton>
                <template #body>
                  <UInput v-model="NewBoardName" color="info" :ui="{ base: 'bg-[var(--secondary-grey)] border-[var(--text-color)]'}"/>
                  <UButton size="md" color="secondary" variant="ghost" :ui="{base: 'text-[var(--text-color)]'}" @click.stop="updateBoardName()">Change</UButton>
                </template>
              </UModal>

              <UModal title="Delete Board" description="Are you sure you want to delete this board ?" :ui="{ body: 'bg-[var(--secondary-grey)] flex flex-col items-center justify-center gap-2', content: 'bg-[var(--secondary-grey)] ring-0 w-80', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                <UButton label="Open" color="secondary" variant="ghost" size="md" :ui="{ base: 'rounded-sm w-60 text-[var(--text-color)]'}">Delete Board</UButton>
                <template #body v-if=" auth.user.email == boardOwnerEmail">
                    <UButton size="md" color="error"  :ui="{base: 'text-[var(--ui-primary)]'}" @click.stop="deleteBoard()">Delete</UButton>
                  </template>
                  <template #body v-else>
                    <h2>You do not have the permission to delete this board</h2>
                    <UButton size="md" color="error" disabled :ui="{base: 'text-[var(--ui-primary)] mt-4 disabled:opacity-50'}" @click.stop="deleteBoard()">Delete</UButton>
                </template>
              </UModal>
            </div>
          </template>
        </UPopover>
        <UPopover title="Archived task" :content="{side: 'bottom', sideOffset: 8 }" :ui="{content: 'bg-[var(--main-grey)] w-70 px-6 py-4'}">
          <UButton icon="i-lucide-archive" color="secondary" variant="ghost"/>
          <template #content>
            <div class="flex flex-col items-center justify-center gap-4 mb-4">
              <h2 class="text-highlighted font-semibold">
                Archived tasks
              </h2>
              <UInput v-model="archiveSearch" icon="i-lucide-search" color="info" placeholder="Search archived tasks..." size="md" :ui="{ base: 'bg-[var(--secondary-grey)] ring-0 text-text-color' }" />
            </div>

            <div v-if="archivedTasks.length === 0" class="text-sm opacity-70 text-center py-6">
              No archived tasks
            </div>
            <div v-else class="space-y-4">
              <div v-if="filteredArchivedTasks.length === 0" class="text-sm opacity-60 text-center py-6">
                No archived tasks found
              </div>
              <div v-for="task in filteredArchivedTasks" :key="task.id">
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
import { useAuthStore } from '~/store/auth';
import type { Task, Column } from '~/composables/types/board';
import { useBoardSocket } from '~/composables/useBoardSocket';

const route = useRoute()
const boardID = computed(() => {
  const id = route.params.boardID
  return Array.isArray(id) ? id[0] : id
})

const { $bridge } = useNuxtApp()
const api = $bridge
const ws = useBoardSocket(boardID.value!)
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

const color = ref('#1f1f21')
const NewBoardName = ref('')
const router = useRouter()
const toast = useToast()

const archivedTasks = ref<Task[]>([])
const selectedTask = ref<Task | null>(null)
const taskModalOpen = ref(false)
const archiveSearch = ref('')

const getBoardData = async () => {
  if (!auth.authenticated || !auth.jwt || !boardID.value) return
  api.setjwt(auth.jwt)
  const data = await api.getBoardData(boardID.value).catch((error) => {
    console.error(error);
  });
  boardName.value = data.title
  NewBoardName.value = data.title
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
  ws.connect()
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

async function updateBoardColor() {
  if (!boardID.value) return

  try {
    api.setjwt(auth.jwt)

    await api.updateBoard(boardID.value, {
      color: color.value
    })

    boardColor.value = color.value
  } catch (err) {
    console.error(err)
  }
}

function openArchivedTask(task: Task) {
  selectedTask.value = { ...task }
  taskModalOpen.value = true
}

async function restoreTask(task: Task) {
  if (!boardID.value) return

  try {
    const categoryExists = board.value.some(c => c.id === task.category)
    if (!categoryExists) {
      const nextCategories = [...board.value.map(c => c.id), task.category]
      console.log(task.category, nextCategories)

      await api.updateCategories(boardID.value, {
        categories: nextCategories
      })

      board.value.push({
        id: task.category,
        title: task.category,
        cards: []
      })
    }

    await api.restoreArchive(boardID.value, task.id)
    await getBoardData()
  } catch (err) {
    console.error(err)
  }
}

async function updateBoardName() {
  if (!boardID.value) return

  try {
    api.setjwt(auth.jwt)

    await api.updateBoard(boardID.value, {
      title: NewBoardName.value
    })

    boardName.value = NewBoardName.value
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

async function deleteBoard() {
  if (!boardID.value) return

  try {
    api.setjwt(auth.jwt)

    await api.deleteBoard(boardID.value)

    toast.add({
      title: 'Board deleted',
      description: 'The board has been deleted successfully.',
      color: 'info',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })

    router.push('/')
  } catch (err) {
    console.error(err)

    toast.add({
      title: 'Error',
      description: 'Failed to delete board.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
  }
}

const filteredArchivedTasks = computed(() => {
  if (!archiveSearch.value.trim()) return archivedTasks.value

  const q = archiveSearch.value.toLowerCase()

  return archivedTasks.value.filter(task =>
    task.title.toLowerCase().includes(q)
  )
})

ws.onMessage((event) => {
  console.log('[WS EVENT]', event.type)
  console.log(event.event_from_uuid)
  if (event.event_from_uuid === auth.user.id) {
    console.log(event.event_from_uuid, auth.user.id)
    return
  }

  switch (event.type) {

    case 'f_update_board':
      boardName.value = event.board_title
      boardColor.value = event.board_color
      boardOwnerEmail.value = event.board_owner.email
      break

    case 'f_update_categories':
      console.log(event)
      board.value = event.categories.map((cat: string) => ({
        id: cat,
        title: cat,
        cards: board.value.find(c => c.id === cat)?.cards ?? []
      }))
      break

    case 'f_create_task':
    case 'f_update_task':
    case 'f_restore_task':
      getBoardData()
      break

    case 'f_delete_task':
    case 'f_deleteforce_task':
      archivedTasks.value = archivedTasks.value.filter(t => t.id !== event.id)
      board.value.forEach(col => {
        col.cards = col.cards.filter(t => t.id !== event.id)
      })
      break

    case 'f_invit_board':
    case 'f_update_role':
    case 'f_delete_member':
      getBoardData()
      break

    default:
      console.warn('[WS] unknown event', event)
  }
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
