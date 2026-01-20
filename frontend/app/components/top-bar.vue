<template>
    <div class="top-bar">
        <UButton color="secondary" variant="ghost" size="sm"  :ui="{base: 'rounded-sm'}" to="/">
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
                            <UInput v-model="state.name" maxlength="49" class="w-full" size="md" color="secondary" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm'}"/>
                        </UFormField>
                        <UPopover>
                            <UButton label="Choose color" color="neutral" variant="outline" :ui="{base: 'bg-[var(--secondary-grey)] rounded-sm'}">
                                <template #leading>
                                    <span :style="chip" class="size-3 rounded-full" />
                                </template>
                            </UButton>
                            <template #content>
                                <UColorPicker v-model="color"></UColorPicker>
                            </template>
                        </UPopover>
                        <UButton type="submit" color="info" size="md" :ui="{ base: 'rounded-sm flex justify-center items-center text-center' }" class="w-full ">
                        Create
                        </UButton>
                    </UForm>
                </template>
            </UPopover>
        </div>
        <ClientOnly>
            <UDropdownMenu :items="profile" :ui="{content: 'bg-[var(--secondary-grey)] rounded-sm'}">
                <UButton :avatar="{src: auth.user.profile_picture, size: 'xs'}" color="secondary" variant="ghost" size="md" :ui="{ base: 'p-1 rounded-sm'}"/>
            </UDropdownMenu>
        </ClientOnly>
    </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth';
import type { DropdownMenuItem, FormError, FormSubmitEvent } from '@nuxt/ui'

const { $bridge } = useNuxtApp()
const api = $bridge
const auth = useAuthStore();
const router = useRouter();
const toast = useToast()

const items = ref(['Backlog', 'Todo', 'In Progress', 'Done'])
const value = ref('')
const profile: DropdownMenuItem[] = [{
    label: 'Log Out',
    onSelect() {
        auth.logUserOut();
        router.push('/login');
    }
}]

const state = reactive({
    name: undefined
})

const color = ref('#1f1f21')
const chip = computed(() => ({ backgroundColor: color.value }))

type Schema = typeof state

function validate(state: Partial<Schema>): FormError[] {
    const errors = []
    if (!state.name) errors.push({name: 'name', message: 'Required'})
    return errors
}

async function onSubmit(event: FormSubmitEvent<Schema>) {
    if (!state.name) return

    try {
        api.setjwt(auth.jwt)

        const result = await api.createBoard({
            title: state.name,
            color: color.value})

        toast.add({
            title: 'Success',
            description: 'Board created successfully.',
            color: 'info',
            ui: {
                root: 'bg-[var(--secondary-grey)]',
            },
        })

        state.name = undefined
        color.value = '#1f1f21'

        router.push(`/boards/${result.id}`)
    } catch (err) {
        console.error(err)
        toast.add({
        title: 'Error',
        description: 'Failed to create board.',
        color: 'error',
        ui: {
                root: 'bg-[var(--secondary-grey)]',
            },
        })
    }
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