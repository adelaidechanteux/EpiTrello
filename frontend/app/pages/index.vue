<template>
    <TopBar></TopBar>
    <UPage>
    <UPageHeader title="Your boards" class="flex justify-center items-center text-center"/>
    <UPageBody>
      <UContainer class="max-w-[914px] w-[914]">
        <div class="board-overview-container">
          <BoardOverview v-for="(test, index) in test" :key="index" v-bind="test"/>
        </div>
      </UContainer>
    </UPageBody>
  </UPage>
</template>

<script setup lang="ts">
const test = ref([
    {
        color: '#666666',
        title: 'test1'
    },
    {
        color: '#000000',
        title: 'test2'
    },{
        color: '#FFFFFF',
        title: 'testdeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee3'
    },
])
</script>

<style>
.board-post {
    width: 220px;
}

.board-overview-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    row-gap: 12px;
    column-gap: 12px;
}
</style>