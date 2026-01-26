<template>
  <div class="flex gap-4 p-4 overflow-x-auto">
    <Draggable v-model="board" item-key="id" @end="onColumnReorder" group="columns" class="flex gap-4 p-4 overflow-x-auto" :animation="200">
      <template #item="{ element: column }">
        <div class="min-w-[260px] bg-(--ui-black) rounded-xl p-3 flex flex-col shadow hover:shadow-lg">
          <div class="flex items-center justify-between mb-3 pl-3 group">
          <h3 class="font-semibold" >{{ column.title }}</h3>
          <UButton v-if="column.cards.length === 0" icon="i-lucide-trash-2" size="xs" color="error" variant="ghost" class="opacity-0 group-hover:opacity-100 transition-opacity" @click.stop="deleteColumn(column.id)"/>
          </div>

          <Draggable v-model="column.cards" item-key="id"  @end="onTaskReorder" group="cards" class="space-y-2 min-h-[40px]">
            <template #item="{ element }">
              <div class="group relative bg-(--secondary-grey) rounded-lg p-2 text-sm shadow cursor-pointer hover:border-2 border-info flex items-center gap-2 overflow-hidden" @click="openTask(element)">
                <UButton
                  :color="element.completed ? 'success' : 'secondary'"
                  variant="soft"
                  :icon="element.completed ? 'i-lucide-circle-check' : ''"
                  class="transition-all duration-500 ease-out cursor-pointer
                    rounded-full w-5 h-5 p-0
                    -ml-6 opacity-0 translate-x-[-6px]
                    group-hover:ml-0 group-hover:opacity-100 group-hover:translate-x-0"
                  :class="element.completed
                    ? 'ml-0 opacity-100 translate-x-0'
                    : 'border-2 border-(--fixed-text-color)'"
                  @click.stop="toggleCompleted(element)"
                />

                <span
                  class="flex-1 transition-all">
                  {{ element.title }}
                </span>
              </div>
            </template>

            <template #footer v-if="column.cards.length === 0">
              <div class="h-10 rounded-xl border-2 border-dashed border-gray-300 dark:border-gray-700 text-sm text-gray-400 flex items-center justify-center">
                Drop here
              </div>
            </template>
          </Draggable>
          <div class="mt-2 flex flex-col gap-1">
            <UButton v-if="!addingCard[column.id]" icon="i-lucide-plus" :ui="{ base: 'bg-transparent hover:bg-(--ui-hover) text-left text-sm px-2 py-2 rounded-lg text-text-color' }" class="justify-start" @click="addingCard[column.id] = true">
              Add a card
            </UButton>

            <div v-else class="flex flex-col gap-1">
              <UInput v-model="newCardTitles[column.id]" placeholder="Enter a title" color="info" :ui="{ base: 'bg-[var(--secondary-grey)] ring-0 rounded-lg pb-8 text-text-color' }" @keyup.enter="addCard(column)"/>

              <div class="flex gap-2 mt-1">
                <UButton color="info" :ui="{ base: 'text-sm font-medium rounded shadow-none' }" @click="addCard(column)">
                  Add card
                </UButton>

                <UButton icon="i-lucide-x" variant="ghost" color="secondary" size="md" :ui="{ base: 'rounded-sm'}" @click="cancelAddCard(column)"/>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <div class="min-w-[260px] flex-shrink-0">
          <div v-if="!addingColumn">
            <UButton icon="i-lucide-plus" :ui="{ base: 'bg-transparent hover:bg-(--ui-hover) text-left text-sm px-2 py-2 rounded-lg text-[var(--text-color)]' }" class="justify-start" @click="addingColumn = true">
              Add another list
            </UButton>
          </div>
          <div v-else class="flex flex-col gap-1 bg-(--ui-black) rounded-xl p-3">
            <UInput v-model="newColumnTitle" placeholder="Enter list title..." color="info" :ui="{ base: 'bg-[var(--secondary-grey)] ring-0 rounded-lg text-text-color' }" @keyup.enter="addColumn"/>
            <div class="flex gap-2 mt-1">
              <UButton color="info" :ui="{ base: 'text-sm font-medium rounded shadow-none' }" @click="addColumn">
                Add List
              </UButton>
              <UButton icon="i-lucide-x" variant="ghost" color="secondary" size="md" :ui="{ base: 'rounded-sm'}" @click="cancelAddColumn"/>
            </div>
          </div>
        </div>
      </template>
    </Draggable>
  </div>
   <TaskModal v-if="selectedTask" :open="taskModalOpen" :task="selectedTask" :boardID="boardID!" :categories="board.map(c => c.id)" @close="taskModalOpen = false" :archived="false" @updated="onTaskUpdated"/>
</template>

<script setup lang="ts">
import Draggable from 'vuedraggable';
import type { Task, Column } from '~/composables/types/board';
import { useRoute } from 'vue-router';

const props = defineProps<{
  board: Column[]
}>()

const { $bridge } = useNuxtApp()
const api = $bridge
const route = useRoute()
const boardID = route.params.boardID as string

const newCardTitles = ref<Record<string, string>>({})
const addingCard = ref<Record<string, boolean>>({})
const addingColumn = ref(false)
const newColumnTitle = ref('')
const board = defineModel<Column[]>('board', { required: true })

const selectedTask = ref<Task | null>(null)
const selectedColumnId = ref<string | null>(null)
const taskModalOpen = ref(false)
const toast = useToast()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'updated'): void
}>()

async function addCard(column: Column) {
  const title = newCardTitles.value[column.id]?.trim()
  if (!title) return

  const placeholder: Task = {
    id: '',
    title,
    description: '',
    category: column.id,
    color: null,
    date_start: null,
    date_end: null,
    assigned: null,
    completed: false
  }

  column.cards.push(placeholder)

  newCardTitles.value[column.id] = ''
  addingCard.value[column.id] = false

  try {
    const createdTask = await api.createTask(boardID, {
      title,
      description: '',
      category: column.id,
      color: null,
      date_start: null,
      date_end: null,
      assigned: null,
    })

    const index = column.cards.indexOf(placeholder)
    if (index !== -1) {
      column.cards[index] = createdTask
    }
  } catch (err) {
    console.error(err)
    column.cards = column.cards.filter(c => c !== placeholder)
    toast.add({
      title: 'Error',
      description: 'Failed to add task.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
  }
}

function cancelAddCard(column: Column) {
  console.log(props.board)
  addingCard.value[column.id] = false
  newCardTitles.value[column.id] = ''
}

async function addColumn() {
  const title = newColumnTitle.value.trim()
  if (!title) return

  const nextCategories = [...board.value.map(col => col.title), title]
  try {
    await api.updateCategories(
      boardID,
      {
        categories: nextCategories,
      })
    board.value.push({
      id: title,
      title,
      cards: [],
    })

    newColumnTitle.value = ''
    addingColumn.value = false
  } catch (err) {
    console.error('Failed to add column', err)
    toast.add({
      title: 'Error',
      description: 'Failed to add column.',
      color: 'error',
      ui: {
        root: 'bg-[var(--secondary-grey)]',
      },
    })
  }
}

async function onColumnReorder() {
  try {
    await api.updateCategories(boardID, {
      categories: board.value.map(col => col.title),
    })
  } catch (err) {
    console.error(err)
  }
}

async function onTaskReorder() {
  try {
    const updates: Promise<any>[] = []

    for (const column of board.value) {
      for (const task of column.cards) {
        updates.push(
          api.updateTask(boardID, task.id, {
            category: column.id
          })
        )
      }
    }

    await Promise.all(updates)
  } catch (err) {
    console.error(err)
  }
}

function cancelAddColumn() {
  newColumnTitle.value = ''
  addingColumn.value = false
}

function openTask(card: Task) {
  selectedTask.value = {
    id: card.id,
    title: card.title,
    description: card.description,
    category: card.category,
    color: card.color,
    date_start: card.date_start,
    date_end: card.date_end,
    assigned: card.assigned,
    completed: card.completed
  }
  taskModalOpen.value = true
}

function onTaskUpdated(updatedTask: Task) {
  emit('updated')
}

async function deleteColumn(columnId: string) {
  const updatedColumns = board.value.filter(col => col.id !== columnId)

  try {
    await api.updateCategories(boardID, {
      categories: updatedColumns.map(col => col.id)
    })

    board.value = updatedColumns
  } catch (err) {
    console.error('Failed to delete column', err)
  }
}

async function toggleCompleted(task: Task) {
  const previous = task.completed
  task.completed = !task.completed

  try {
    await api.updateTask(boardID, task.id, {
      completed: task.completed,
    })
  } catch (err) {
    console.error('Failed to update task', err)
    task.completed = previous // rollback
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

</script>
