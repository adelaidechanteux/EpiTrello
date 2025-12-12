<template>
    <div class="top-bar">
        <UButton color="secondary" variant="ghost" size="sm">
            <img src="~/assets/images/trello_logo.png" class="logo-button" alt="trello logo"/>
        </UButton>
        <UInputMenu v-model="value" :items="items" class="search-bar" color="info" placeholder="Search" icon="i-lucide-search"
        open-on-focus highlightOnHover :ui="{ base: 'bg-[var(--secondary-grey)]', item: [ `bg-[var(--secondary-grey)] hover:bg-[var(--ui-secondary)]/20
        active:bg-[var(--ui-secondary)]/10 focus:bg-[var(--ui-secondary)] focus:ring-0 `],
        group: 'p-0', empty:'bg-[var(--secondary-grey)]'}"/>
    </div>
</template>

<script setup lang="ts">
const items = ref(['Backlog', 'Todo', 'In Progress', 'Done'])
const value = ref('')
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

.search-bar {
    width: 60%;
}
</style>