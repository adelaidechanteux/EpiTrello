<template>
    <div class="top-bar">
        <UButton color="secondary" variant="ghost" size="sm"  :ui="{base: 'rounded-sm'}">
            <img src="~/assets/images/trello_logo.png" class="logo-button" alt="trello logo"/>
        </UButton>
        <div class="middle">
            <UInputMenu v-model="value" :items="items" class="search-bar" color="info" placeholder="Search" icon="i-lucide-search"
            open-on-focus highlightOnHover size="md" :ui="{ base: 'bg-[var(--secondary-grey)] rounded-sm', item: [ `bg-[var(--secondary-grey)] hover:bg-[var(--ui-secondary)]/20
            active:bg-[var(--ui-secondary)]/10 focus:bg-[var(--ui-secondary)] focus:ring-0 `],
            group: 'p-0', empty:'bg-[var(--secondary-grey)]'}"/>
            <UPopover :content="{ align: 'start', side: 'bottom', sideOffset: 8 }" :ui="{content: 'bg-[var(--secondary-grey)]'}">
                <UButton color="info" size="md" :ui="{ base: 'rounded-sm' }">
                Create
                </UButton>

                <template #content>
                    <div class="popover-title">
                        <h1>Create board</h1>
                    </div>
                    <UForm :validate="validate" :state="state" class="space-y-4 p-4" @submit="onSubmit" >
                        <UFormField label="Board title" name="name" size="xs">
                        <UInput v-model="state.name" class="w-full" size="md" color="secondary" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm'}"/>
                        </UFormField>
                        <UButton type="submit" color="info" size="md" :ui="{ base: 'rounded-sm flex justify-center items-center text-center' }" class="w-full ">
                        Create
                        </UButton>
                    </UForm>
                </template>
            </UPopover>
        </div>
        <UButton :avatar="{src: 'https://github.com/nuxt.png', size: 'xs'}" color="secondary" variant="ghost" size="md" :ui="{ base: 'p-1 rounded-sm'}"/>
    </div>
</template>

<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '@nuxt/ui'

const items = ref(['Backlog', 'Todo', 'In Progress', 'Done'])
const value = ref('')

const state = reactive({
    name: undefined
})

type Schema = typeof state

function validate(state: Partial<Schema>): FormError[] {
    const errors = []
    if (!state.name) errors.push({name: 'name', message: 'Required'})
    return errors
}

const toast = useToast()
async function onSubmit(event: FormSubmitEvent<Schema>) {
    toast.add({title: 'Success', description: 'The board is being created.', color: 'info'})
    console.log(event.data)
}
</script>

<style>
.top-bar {
    display: flex;
    align-items: center;
    height: fit-content;
    padding: 8px;
    justify-content: space-between;
}

.logo-button {
    height: 20px;
}

.middle {
    display: flex;
    flex: 1 0 auto;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.search-bar {
    width: 40%;
}

.popover-title {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 10px;
}
</style>