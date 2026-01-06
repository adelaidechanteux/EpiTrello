<template>
    <TopBar></TopBar>
    <Board />
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth'

const route = useRoute()
const boardID = computed(() => {
  const id = route.params.boardID
  return Array.isArray(id) ? id[0] : id
})


const { $bridge } = useNuxtApp()
const api = $bridge

const auth = useAuthStore()
const boardData = ref<any[]>([])

const getBoardData = async () => {
  if (!auth.authenticated || !auth.jwt || !boardID.value) return
  api.setjwt(auth.jwt)
  const data = await api.getBoardData(boardID.value).catch((error) => {
    console.error(error);
  });
  boardData.value = data;
  console.log(boardData.value)
}

onMounted(async () => {
  await getBoardData();
})


</script>
