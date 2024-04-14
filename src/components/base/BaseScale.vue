<template>
  <div class="w-full flex flex-col gap-2">
    <div class="w-full h-8 border border-gray-300 rounded-lg overflow-hidden relative">
      <div class="h-full" :class="scoreColor" :style="{ width: `${10 * score}%` }" />
    </div>
    <div class="text-2xl font-bold text-white -translate-x-4 rounded-full flex items-center justify-center w-8 h-8"
      :class="scoreColor" :style="{ marginLeft: `${10 * score}%` }">
      {{ score }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  score?: number;
}

const props = withDefaults(defineProps<Props>(), {
  score: 0,
})

const scoreColor = computed(() => {
  switch (props.score) {
    case 1:
      return 'bg-red-900'
    case 2:
      return 'bg-red-700'
    case 3:
      return 'bg-red-600'
    case 4:
      return 'bg-orange-600'
    case 5:
      return 'bg-orange-500'
    case 6:
      return 'bg-amber-500'
    case 7:
      return 'bg-amber-400'
    case 8:
      return 'bg-yellow-300'
    case 9:
      return 'bg-lime-500'
    case 10:
      return 'bg-lime-600'
    default:
      return ''
  }
})

// 1-2 бордовый
// 3-4 - красный
// 5-6 - оранжевый
// 7-8 - желтый
// 9-10 зеленый
</script>
