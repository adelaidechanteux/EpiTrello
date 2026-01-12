<template>
  <div class="board-overview">
      <div class="board-overview-header" :style="{ backgroundColor: color }"/>
      <div class="board-overview-body">
        {{ title }}
      </div>
    </div>
</template>

<script setup lang="ts">

const props = defineProps({
  color: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: false
  }
})

const { color } = props
</script>


<style>
.board-overview {
    display: flex;
    flex-direction: column;
    width: 220px;
    height: 128px;
    box-shadow: 0px 0px 5px 0px rgba(0,0,0,0.65);
    border-radius: 8px;
}

.board-overview-header {
    width: 220px;
    height: 72px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

.board-overview-body{
    height: 56px;
    padding: 8px;
    color: var(--text-color);
    font-size: 14px;
    overflow: scroll;
}
</style>