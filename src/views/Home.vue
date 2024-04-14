<template>
  <div class="text-gray-800">
    <!-- header -->
    <div class="sticky top-0 bg-white z-30 px-8 py-4" :class="scrollHeight > 10 && 'shadow-md'">
      <div
        class="mx-auto max-w-screen-xl flex flex-col sm:flex-row gap-x-4 gap-y-2 sm:gap-10 items-center justify-between">
        <button class="mt-2 w-10 shrink-0 sm:w-16 hover:opacity-80" @click="scrollTo('top')">
          <img class="w-full" src="/apple.svg" alt="home" />
        </button>

        <div class="flex items-center gap-6 text-lg uppercase font-medium text-sky-950">
          <button class="hover:opacity-80 transition duration-150" @click="scrollTo('analysis')">Анализ</button>
          <button class="hover:opacity-80 transition duration-150" @click="scrollTo('about')">Принцип работы</button>
        </div>
      </div>
    </div>

    <!-- main block -->
    <div class="px-8 py-24 sm:py-40 lg:py-64 bg-center bg-cover bg-[url('/12.jpg')]">
      <div class="flex flex-col items-center gap-4 sm:gap-8 mx-auto max-w-md lg:max-w-xl uppercase">
        <div class="text-center text-3xl sm:text-4xl lg:text-5xl font-bold text-sky-950">
          Будьте уверены в том, чем питается ваш ребенок
        </div>
        <button
          class="flex bg-orange-500 hover:bg-orange-400 transition duration-150 text-white py-3 px-5 text-md sm:text-xl uppercase items-center justify-center gap-4 font-medium w-max rounded-lg"
          @click="scrollTo('analysis')">
          Проанализировать продукт
        </button>
      </div>
    </div>

    <!-- about block -->
    <div ref="aboutBlock" class="px-6 sm:px-8 pt-10 sm:pt-16">
      <div class="mx-auto max-w-screen-xl">
        <AboutBlock />
      </div>
    </div>

    <!-- analysis block -->
    <div ref="analysisBlock" class="px-6 sm:px-8 py-12 sm:py-16">
      <div class="mx-auto max-w-screen-xl">
        <AnalysisBlock />
      </div>
    </div>

    <div class="w-full px-6 sm:px-8 py-10 sm:py-16 bg-center bg-cover bg-[url('/5.jpg')]">
      <div class="mx-auto max-w-screen-xl h-full flex flex-col gap-4 justify-center">
        <div class="text-3xl sm:text-4xl font-bold">
          Лучшее для детей
        </div>
        <div class="w-2/3 sm:w-1/2 text-base sm:text-xl">
          Мы провели тщательное исследование, изучив научные работы и сотрудничая с экспертами в области педиатрии и
          диетологии. Наши рекомендации основаны на анализе сотен этикеток детского питания с использованием
          искусственного интеллекта для расчета полезности продукта.
        </div>
      </div>
    </div>

    <!-- questions block -->
    <div ref="questionsBlock" class="px-6 sm:px-8 pt-10 sm:pt-16">
      <div class="mx-auto max-w-screen-xl">
        <QuestionsBlock />
      </div>
    </div>

    <button
      class="transition-all z-40 bg-orange-500 hover:bg-orange-400 text-white font-bold rounded-full fixed bottom-10 right-10 h-14 w-14 text-4xl flex items-center justify-center pb-1 hover:pb-2 duration-150"
      :class="scrollHeight > 10 ? 'opacity-100' : 'opacity-0'" @click="scrollTo('top')">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
        class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 19.5v-15m0 0l-6.75 6.75M12 4.5l6.75 6.75" />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import AboutBlock from "../components/AboutBlock.vue";
import QuestionsBlock from "../components/QuestionsBlock.vue";
import AnalysisBlock from "../components/AnalysisBlock.vue";

const analysisBlock = ref<HTMLDivElement | undefined>(undefined)
const aboutBlock = ref<HTMLDivElement | undefined>(undefined)
const questionsBlock = ref<HTMLDivElement | undefined>(undefined)
const scrollHeight = ref(0)

const scrollTo = (id: string) => {
  let top = 0
  const offset = 100

  switch (id) {
    case 'analysis':
      top = (analysisBlock.value?.offsetTop || 0) - offset
      break;
    case 'about':
      top = (aboutBlock.value?.offsetTop || 0) - offset
      break;
    case 'top':
      break;
    default:
      break;
  }

  window.scrollTo({ left: 0, top: top, behavior: "smooth" })
}

const updateScroll = () => {
  scrollHeight.value = window.scrollY || document.documentElement.scrollTop
}

onMounted(() => {
  window.addEventListener('scroll', updateScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', updateScroll)
})
</script>
