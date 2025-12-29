<template>
    <TopBar></TopBar>
    <Board />
</template>

<script setup lang="ts">
const route = useRoute()
const boardID = route.params.boardID
</script>
