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
                    <span v-if="member.email == boardOwnerEmail" class="text-xs opacity-70">
                      Owner
                    </span>
                    <span v-else-if="admins.some(a => a.email === member.email)" class="text-xs opacity-70">
                      Admin
                    </span>
                    <span v-else class="text-xs opacity-70">
                      Member
                    </span>
                  </div>
                </div>
                <div v-if="auth.user.email == boardOwnerEmail">
                  <UModal v-model="confirmOpen" title="Remove member" description="Are you sure you want to remove this member from the board?" :ui="{ body: 'bg-[var(--secondary-grey)]', content: 'bg-[var(--secondary-grey)] ring-0 w-80', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                    <UButton v-if="member.email !== boardOwnerEmail" icon="i-lucide-x" size="xs" color="error" variant="ghost" @click="askRemoveMember(member.email)"/>
                    <template #body>
                      <div class="flex justify-center gap-2">
                        <UButton color="error" @click="confirmRemoveMember"> Remove </UButton>
                      </div>
                    </template>
                  </UModal>
                </div>
                <div v-else-if="admins.some(a => a.email === auth.user.email)">
                  <UModal v-model="confirmOpen" title="Remove member" description="Are you sure you want to remove this member from the board?" :ui="{ body: 'bg-[var(--secondary-grey)]', content: 'bg-[var(--secondary-grey)] ring-0 w-80', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                    <div v-if="member.email === boardOwnerEmail"/>
                    <div v-else-if="admins.find(a => a.email === member.email)">
                      <UTooltip text="You do not have permission to remove users" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                        <UButton disabled icon="i-lucide-x" size="xs" color="error" variant="ghost" @click="askRemoveMember(member.email)"/>
                      </UTooltip>
                    </div>
                    <div v-else>
                        <UButton icon="i-lucide-x" size="xs" color="error" variant="ghost" @click="askRemoveMember(member.email)"/>
                    </div>
                      <template #body>
                      <div class="flex justify-center gap-2">
                        <UButton color="error" @click="confirmRemoveMember"> Remove </UButton>
                      </div>
                    </template>
                  </UModal>
                </div>
                <div v-else>
                  <UModal v-model="confirmOpen" title="Remove member" description="Are you sure you want to remove this member from the board?" :ui="{ body: 'bg-[var(--secondary-grey)]', content: 'bg-[var(--secondary-grey)] ring-0 w-80', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                    <UTooltip text="You do not have permission to remove users" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                      <UButton disabled v-if="member.email !== boardOwnerEmail" icon="i-lucide-x" size="xs" color="error" variant="ghost" @click="askRemoveMember(member.email)"/>
                    </UTooltip>
                    <template #body>
                      <div class="flex justify-center gap-2">
                        <UButton color="error" @click="confirmRemoveMember"> Remove </UButton>
                      </div>
                    </template>
                  </UModal>
                </div>
              </div>
            </div>
          </template>
        </UModal>
        <UPopover :content="{side: 'bottom', sideOffset: 8 }" :ui="{content: 'bg-[var(--main-grey)] w-70 p-4'}">
          <UButton icon="i-lucide-ellipsis" color="secondary" variant="ghost"/>
          <template #content>
            <div v-if=" auth.user.email == boardOwnerEmail || admins.some(a => a.email === auth.user.email)" class="flex flex-col items-center gap-4">
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
                <UTooltip :text="auth.user.email == boardOwnerEmail? 'Delete this board' : 'You do not have permission to delete this board'" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                  <UButton :disabled="auth.user.email == boardOwnerEmail? false : true" label="Open" color="error" variant="ghost" size="md" :ui="{ base: 'rounded-sm w-60'}">Delete Board</UButton>
                </UTooltip>
                  <template #body>
                    <UButton size="md" color="error"  :ui="{base: 'text-[var(--ui-primary)]'}" @click.stop="deleteBoard()">Delete</UButton>
                  </template>
              </UModal>
            </div>
            <div v-else>
              <UModal title="Change Board Color" :ui="{ body: 'bg-[var(--secondary-grey)] flex flex-col items-center justify-center gap-2', content: 'bg-[var(--secondary-grey)] ring-0 w-60', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                <UTooltip text="You do not have permission to modify this board" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                  <UButton disabled label="Open" color="secondary" variant="ghost" size="md" :ui="{ base: 'rounded-sm w-60 text-[var(--text-color)]'}">Board Color</UButton>
                </UTooltip>
                <template #body>
                  <UColorPicker v-model="color"></UColorPicker>
                  <UButton size="md" color="secondary" variant="ghost" :ui="{base: 'text-[var(--text-color)]'}" @click.stop="updateBoardColor()">Change</UButton>
                </template>
              </UModal>

              <UModal title="Change Board Name" :ui="{ body: 'bg-[var(--secondary-grey)] flex flex-col items-center justify-center gap-2', content: 'bg-[var(--secondary-grey)] ring-0 w-60', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                <UTooltip text="You do not have permission to modify this board" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                  <UButton disabled label="Open" color="secondary" variant="ghost" size="md" :ui="{ base: 'rounded-sm w-60 text-[var(--text-color)]'}">Board Name</UButton>
                </UTooltip>
                  <template #body>
                    <UInput v-model="NewBoardName" color="info" :ui="{ base: 'bg-[var(--secondary-grey)] border-[var(--text-color)]'}"/>
                    <UButton size="md" color="secondary" variant="ghost" :ui="{base: 'text-[var(--text-color)]'}" @click.stop="updateBoardName()">Change</UButton>
                  </template>
                </UModal>

                <UModal title="Delete Board" description="Are you sure you want to delete this board ?" :ui="{ body: 'bg-[var(--secondary-grey)] flex flex-col items-center justify-center gap-2', content: 'bg-[var(--secondary-grey)] ring-0 w-80', overlay: 'bg-[var(--ui-overlay)]', header: 'border-[var(--text-color)]', close: 'hover:bg-(--ui-hover)'}">
                  <UTooltip text="You do not have permission to delete this board" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                    <UButton disabled label="Open" color="error" variant="ghost" size="md" :ui="{ base: 'rounded-sm w-60'}">Delete Board</UButton>
                  </UTooltip>
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
                <div class="group relative rounded-lg p-2 text-sm shadow cursor-pointer border-2 hover:border-info flex items-center gap-2 overflow-hidden" :style="{backgroundColor: task.color ?? 'var(--secondary-grey)', borderColor: task.color ?? 'var(--secondary-grey)' }" @click="openArchivedTask(task)">
                  <UIcon name="i-lucide-square-pen" class="absolute top-1 right-1 opacity-0 group-hover:opacity-100"/>
                  <span class="flex-1 flex flex-col transition-all">
                    <div class="mt-1 flex items-center gap-2">
                      <UTooltip :text="task.completed ? 'Mark Uncomplete' : 'Mark Complete'" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                        <UButton :color="task.completed ? 'success' : 'secondary'" variant="soft" :icon="task.completed ? 'i-lucide-circle-check' : ''"
                        class="transition-all duration-500 ease-out cursor-pointer rounded-full w-5 h-5 p-0 -ml-6 opacity-0 translate-x-[-6px] group-hover:ml-0 group-hover:opacity-100 group-hover:translate-x-0"
                        :class="task.completed ? 'ml-0 opacity-100 translate-x-0' : 'border-2 border-(--fixed-text-color)'" @click.stop="toggleCompleted(task)"/>
                      </UTooltip>
                      <span>
                        {{ task.title }}
                      </span>
                    </div>
                    <div class="mt-1 flex items-center gap-2 w-full">
                      <span v-if="task.date_end" class="inline-block text-xs mt-1 p-2 py-0.5 w-14 rounded-md transition-colors" :class="dateColorClass(task)">
                        {{ formatDate(task.date_end) }}
                      </span>
                        <UTooltip text="This task has a description" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                          <UIcon v-if="task.description" name="i-lucide-align-left" class="w-4 h-4 opacity-50 hover:opacity-100 transition-opacity" />
                        </UTooltip>
                        <UAvatarGroup v-if="assignedUsers(task).length" size="sm" max="3" class="ml-auto flex items-center -space-x-2">
                          <UTooltip v-for="(user) in assignedUsers(task)" :key="user.id" :text="user.username" :ui="{ content: 'bg-(--secondary-grey) text-(--fixed-text-color)' }">
                            <UAvatar :src="user.profile_picture" :key="user.id" :alt="user.username" class="w-6 h-6 rounded-full object-cover shadow-sm transition-transform"/>
                          </UTooltip>
                        </UAvatarGroup>
                      </div>
                  </span>
                </div>
                <div class="flex gap-0 mt-1">
                  <UButton size="xs" color="info" variant="ghost" @click.stop="restoreTask(task)">Restore</UButton>
                  <div v-if=" auth.user.email == boardOwnerEmail || admins.some(a => a.email === auth.user.email)">
                    <UButton size="xs" color="error" variant="ghost" @click.stop="deleteTask(task)">Delete</UButton>
                  </div>
                  <div v-else>
                    <UTooltip text="You do not have permission to delete archives" :ui="{ content: 'bg-(--secondary-grey) text-color-(--fixed-text-color)' }">
                      <UButton disabled size="xs" color="error" variant="ghost" @click.stop="deleteTask(task)">Delete</UButton>
                    </UTooltip>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </UPopover>
      </div>
    </div>
    <ClientOnly>
      <Board v-if="board" v-model:board="board" v-model:members="members" @updated="getBoardData"/>
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
const requestUrl = useRequestURL()
const ws = useBoardSocket(boardID.value!, `${requestUrl.hostname}:${requestUrl.port}`)
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
    toast.add({
      title: 'Error',
      description: 'Failed to invite user.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
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
    toast.add({
      title: 'Info',
      description: 'User removed successfully.',
      color: 'info',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
  } catch (err) {
    console.error(err)
    toast.add({
      title: 'Error',
      description: 'Failed to remove user.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
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
    toast.add({
      title: 'Error',
      description: 'Failed to change board color.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
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
    toast.add({
      title: 'Error',
      description: 'Failed to restore task.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
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
    toast.add({
      title: 'Error',
      description: 'Failed to rename board.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
  }
}

async function deleteTask(task: Task) {
  if (!boardID.value) return

  try {
    await api.deleteArchive(boardID.value, task.id)

    archivedTasks.value = archivedTasks.value.filter(t => t.id !== task.id)
  } catch (err) {
    console.error(err)
    toast.add({
      title: 'Error',
      description: 'Failed to delete archive.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
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

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  })
}

function isOverdue(date: string) {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const due = new Date(date)
  due.setHours(0, 0, 0, 0)

  return due <= today
}

function isDueSoon(date: string) {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const due = new Date(date)
  due.setHours(0, 0, 0, 0)

  const diffDays = (due.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)

  return diffDays >= 0 && diffDays < 3
}

function dateColorClass(task: Task) {
  if (task.completed) {
    return 'bg-green-500/20 text-green-700 dark:text-green-400'
  }
  if (task.date_end && isOverdue(task.date_end)) {
    return 'bg-red-500/20 text-red-700 dark:text-red-400'
  }
  if (task.date_end && isDueSoon(task.date_end)) {
    return 'bg-orange-500/20 text-orange-700 dark:text-orange-400'
  }
  return ''
}

function assignedUsers(task: Task) {
  if (!task.assigned) return []
  if (typeof task.assigned === 'object' && task.assigned.email) return [task.assigned]

  return members.value.filter(u => u.email === task.assigned)
}

async function toggleCompleted(task: Task) {
  if (!boardID.value) return
  const previous = task.completed
  task.completed = !task.completed

  try {
    await api.updateTask(boardID.value, task.id, {
      completed: task.completed,
    })
  } catch (err) {
    console.error('Failed to update task', err)
    task.completed = previous
    toast.add({
      title: 'Error',
      description: 'Failed to update task status.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
  }
}

ws.onMessage((event) => {
  console.log('[WS EVENT]', event.type)
  if (event.from_user === auth.user.id) {
    return
  }

  switch (event.type) {

    case 'f_update_board':
      boardName.value = event.board_title
      boardColor.value = event.board_color
      boardOwnerEmail.value = event.board_owner.email
      break

    case 'f_update_categories':
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
