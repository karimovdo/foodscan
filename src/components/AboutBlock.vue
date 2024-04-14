<template>
  <div class="flex flex-col gap-6">
    <div class="text-3xl sm:text-4xl text-center font-medium">
      Как мы проводим анализ?
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

      <!-- cart1 -->
      <div class="flex gap-4 bg-gray-100 p-6 rounded-lg">
        <div class="max-sm:hidden w-12 shrink-0 text-orange-400">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
            stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
          </svg>
        </div>
        <div>
          <div class="font-medium text-xl mb-2">Определение питательной ценности</div>
          <div class="text-gray-600">
            Приложение анализирует состав детского питания и определяет его питательную ценность, вычисляя количество
            калорий, белков, углеводов, жиров, витаминов и минералов.
          </div>
        </div>
      </div>

      <!-- cart2 -->
      <div class="flex gap-4 bg-gray-100 p-6 rounded-lg">
        <div class="max-sm:hidden w-12 shrink-0 text-orange-400">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
            stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round"
              d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
          </svg>
        </div>
        <div>
          <div class="font-medium text-xl mb-2">Оценка соответствия рекомендациям</div>
          <div class="text-gray-600">
            Также оценивается состав детского питания с рекомендациями по питанию для детей определенного возраста и
            оценивается, насколько товар соответствует этим рекомендациям.
          </div>
        </div>
      </div>

      <!-- cart3 -->
      <div class="flex gap-4 bg-gray-100 p-6 rounded-lg">
        <div class="max-sm:hidden w-12 shrink-0 text-orange-400">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
            stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round"
              d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
          </svg>
        </div>
        <div>
          <div class="font-medium text-xl mb-2 ">Определение наличия вводящих в заблуждение надписей</div>
          <div class="text-gray-600">
            С помощью методов искусственного интеллекта мы анализируем надписи на этикетке, чтобы определить,
            соответствуют ли они действительности или могут ввести в заблуждение потребителей.
          </div>
        </div>
      </div>

      <!-- cart4 -->
      <div class="flex gap-4 bg-gray-100 p-6 rounded-lg">
        <div class="max-sm:hidden w-12 shrink-0 text-orange-400">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
            stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round"
              d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
          </svg>
        </div>
        <div>
          <div class="font-medium text-xl mb-2">Оценка качества продукта</div>
          <div class="text-gray-600">
            Для более полного анализа мы определяем наличие искусственных консервантов, красителей и других химических
            добавок, а также степень устойчивости к хранению.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>