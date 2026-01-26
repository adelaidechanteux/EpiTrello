<template>
  <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click="emit('close')">
    <div class="bg-(--secondary-grey) rounded-xl p-6 max-w-xl w-full shadow-lg">
      <div class="flex items-center justify-between mb-4">
        <span class="text-lg font-semibold text-[var(--text-color)]">
          Task details
        </span>
        <div v-if="!archived">
          <UButton icon="i-lucide-archive" color="error" variant="ghost" size="sm" @click="archive"> Archive</UButton>
        </div>
        <div v-else>
          <UButton icon="i-lucide-archive" color="neutral" variant="ghost" size="sm" @click="restoreTask">Restore from Archives</UButton>
        </div>
      </div>
      <div class="mb-4">
        <UInput v-model="form.title" size="lg" class="font-semibold w-full" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm'}" placeholder="Task title" />
      </div>
      <div class="space-y-4">
        <UTextarea v-model="form.description" placeholder="Add a description..." autoresize class="w-full" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm'}" />
        <USelect v-model="form.category" :items="categories" label="Column" class="w-full" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm', item: [ `bg-[var(--secondary-grey)] hover:bg-[var(--ui-secondary)]/20
            active:bg-[var(--ui-secondary)]/10`], group: 'p-0', empty:'bg-[var(--secondary-grey)]'}"/>
        <div class="flex gap-2">
          <UInput type="date" v-model="form.date_start" label="Start date" class="w-1/2" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm'}"/>
          <UInput type="date" v-model="form.date_end" label="End date" class="w-1/2" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm'}"/>
        </div>
        <UInput v-model="form.assigned" placeholder="Assign to (email)" class="w-full" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm'}" />
      </div>
      <div class="mt-4 flex justify-between">
        <UButton variant="ghost" color="secondary" @click="close">Cancel</UButton>
        <UButton color="info" @click="save">Save</UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '~/composables/types/board'

const props = defineProps<{
  open: boolean
  task: Task
  boardID: string
  categories: string[]
  archived: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'updated', task: Task): void
}>()

const { $bridge } = useNuxtApp()
const api = $bridge

const form = reactive({
  ...props.task,
  date_start: toDateInput(props.task.date_start),
  date_end: toDateInput(props.task.date_end),
})

watch(
  () => props.task,
  (t) => {
    Object.assign(form, {
      ...t,
      date_start: toDateInput(t.date_start),
      date_end: toDateInput(t.date_end),
    })
  }
)

function toDateInput(value?: string | null): string | null {
  if (!value) return null

  const date =
    value.includes('T')
      ? value.split('T')[0]
      : value.split(' ')[0]

  return date ?? null
}

function close() {
    console.log(props.categories)
  emit('close')
}

async function save() {
  try {
    const payload: Task = {
      ...form,
      description: form.description === "" ? null : form.description,
      color: form.color === "" ? null : form.color,
      date_start: form.date_start === "" ? null : form.date_start,
      date_end: form.date_end === "" ? null : form.date_end,
      assigned: form.assigned === "" ? null : form.assigned,
    }

    await api.updateTask(props.boardID, props.task.id, payload)
    emit('updated', { ...payload })
    close()
  } catch (err) {
    console.error(err)
  }
}

async function archive() {
  try {
    await api.deleteTask(props.boardID, props.task.id)
    emit('updated', { ...props.task })
    close()
  } catch (err) {
    console.error(err)
  }
}

async function restoreTask() {
  try {

    const categoryExists = props.categories.some(c => c === props.task.category)
    if (!categoryExists) {
      const nextCategories = [...props.categories.map(c => c), props.task.category]

      await api.updateCategories(props.boardID, {
        categories: nextCategories
      })
    }

    await api.restoreArchive(props.boardID, props.task.id)
    emit('updated', { ...props.task })
    close()
  } catch (err) {
    console.error(err)
  }
}

</script>
