<template>
  <div class="flex gap-4 p-4 overflow-x-auto">
    <Draggable v-model="board" item-key="id" group="columns" class="flex gap-4 p-4 overflow-x-auto" :animation="200">
      <template #item="{ element: column }">
        <div class="min-w-[260px] bg-(--ui-black) rounded-xl p-3 flex flex-col shadow hover:shadow-lg">
          <h3 class="font-semibold mb-3 pl-3" >{{ column.title }}</h3>

          <Draggable v-model="column.cards" item-key="id" group="cards" class="space-y-2 min-h-[40px]">
            <template #item="{ element }">
              <div class="bg-(--secondary-grey) color-(--ui-info) rounded-lg p-2 text-sm shadow">
                {{ element.title }}
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
            <UButton icon="i-lucide-plus" :ui="{ base: 'bg-transparent hover:bg-(--ui-hover) text-left text-sm px-2 py-2 rounded-lg text-text-color' }" class="justify-start" @click="addingColumn = true">
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
</template>

<script setup lang="ts">
import Draggable from 'vuedraggable';
import type { Card, Column } from '~/composables/types/board';

const newCardTitles = ref<Record<string, string>>({})
const addingCard = ref<Record<string, boolean>>({})
const addingColumn = ref(false)
const newColumnTitle = ref('')

const board = ref<Column[]>([
  {
    id: 'todo',
    title: 'To Do',
    cards: [
      { id: '1', title: 'Setup Nuxt 4' },
      { id: '2', title: 'Design UI' }
    ]
  },
  {
    id: 'doing',
    title: 'Doing',
    cards: [{ id: '3', title: 'Build board' }]
  }
])

function addCard(column: Column) {
  const title = newCardTitles.value[column.id]?.trim()
  if (!title) return

  const newCard: Card = {
    id: Date.now().toString(),
    title
  }

  column.cards.push(newCard)
  newCardTitles.value[column.id] = ''
  addingCard.value[column.id] = false
}

function cancelAddCard(column: Column) {
  addingCard.value[column.id] = false
  newCardTitles.value[column.id] = ''
}

function addColumn() {
  const title = newColumnTitle.value?.trim()
  if (!title) return

  const newCol: Column = {
    id: Date.now().toString(),
    title,
    cards: []
  }

  board.value.push(newCol)
  newColumnTitle.value = ''
  addingColumn.value = false
}

function cancelAddColumn() {
  newColumnTitle.value = ''
  addingColumn.value = false
}

</script>
