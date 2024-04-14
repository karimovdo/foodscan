<template>
  <div class="flex flex-col gap-10">
    <div class="w-full flex flex-col items-center gap-10">
      <div class="text-3xl sm:text-4xl text-center w-full font-medium">Провести анализ</div>
      <div class="flex flex-col gap-6 w-full">
        <div class="text-lg text-center">Выберите 3 фото для анализа продукта питания и обрежьте для лучшего распознавания</div>
        <div
          class="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-x-2 gap-y-6 sm:gap-x-6 items-end justify-center mx-auto">
          <div class="flex flex-col items-center gap-1">
            <div class="text-center text-gray-400">Лицевая сторона</div>
            <BaseImageInput @upload="(file: File) => onFileChange(file, 1)" @delete="onFileDelete(1)" />
          </div>
          <div class="flex flex-col items-center gap-1">
            <div class="text-center text-gray-400">Оборотная сторона</div>
            <BaseImageInput @upload="(file: File) => onFileChange(file, 2)" @delete="onFileDelete(2)" />
          </div>
          <div class="flex flex-col items-center gap-1">
            <div class="text-center text-gray-400">Состав</div>
            <BaseImageInput @upload="(file: File) => onFileChange(file, 3)" @delete="onFileDelete(3)" />
          </div>
        </div>
      </div>
      <button
        class="text-xl uppercase bg-orange-500 hover:bg-orange-400 transition duration-150 text-white py-3 px-5 flex items-center justify-center gap-4 font-medium sm:w-64 rounded-lg"
        :class="Object.keys(files).length < 3 && 'opacity-30 pointer-events-none'" @click="submit">
        <div class="text-xl uppercase">
          Провести анализ
        </div>
      </button>
      <div v-if="errorText"
        class="fixed flex gap-4 items-center bottom-4 right-4 bg-white border-2 border-red-600 rounded-xl p-6 z-50">
        <div class="text-red-600 w-6">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
            class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
          </svg>
        </div>
        <div class="text-lg">
          {{ errorText }}
        </div>
      </div>
    </div>
    <div ref="resultBlock" class="w-full max-w-xl flex justify-center mx-auto">
      <div v-if="isLoading" class="flex flex-col gap-4 items-center">
        <BaseSpinner size="xl" />
        <div class="text-center">{{ loadingTextList[loadingTextIndex] }}</div>
      </div>
      <div v-else-if="result" class="w-full flex flex-col gap-6 items-stretch lg:text-lg py-12 lg:py-24">
        <div class="font-medium text-5xl text-center">{{ result.Brand || 'Описание продукта' }}</div>
        <div>
          <div class="font-medium text-lg text-center mb-2">Оценка продукта</div>
          <BaseScale :score="result.Final_Score" />
        </div>

        <div v-if="result.Category_Description">
          <div class="font-bold uppercase text-xl text-orange-500">Категория</div>
          <div>{{ result.Category_Description }}</div>
        </div>

        <div>
          <div class="font-bold uppercase text-xl text-orange-500">Рекомендации по возрасту</div>
          <div>{{ result.Age_Recommendation === "Не обнаружено" ? result.Age_Recommendation : `Рекомендовано с ${result.Age_Recommendation} месяца/месяцев` }}</div>
        </div>

        <div>
          <div class="font-bold uppercase text-xl text-orange-500">Основные показатели</div>
          <div v-if="result.kcal !== 'Значение не найдено'">Калорийность: <span class="font-bold">{{ result.kcal }}
              ккал</span></div>
          <div v-if="result.Sodium !== 'Не указано'">Натрий: <span class="font-bold">{{ result.Sodium }} г</span></div>
          <div v-if="result.Protein !== 'Не указано'">Белки: <span class="font-bold">{{ result.Protein }} г</span></div>
          <div v-if="result.Carbohydrate !== 'Не указано'">Углеводы: <span class="font-bold">{{ result.Carbohydrate }}
              г</span></div>
          <div v-if="typeof result.Fat === 'number'">Жиры: <span class="font-bold">{{ result.Fat }} г</span></div>
          <div v-if="typeof result.Sugar === 'number'">Сахар: <span class="font-bold">{{ result.Sugar }} г</span></div>
          <div>Фрукты: <span class="font-bold">{{ result.Fruits }}</span></div>
        </div>

        <div>
          <div class="font-bold uppercase text-xl text-orange-500">Требования к содержанию и маркировке продукта</div>
          <div>Энергетическая ценность: <span class="font-bold">{{ result.Energy_Compliance }}</span></div>
          <div>Содержание натрия: <span class="font-bold">{{ result.Sodium_Compliance }}</span></div>
          <div>Содержание углеводов: <span class="font-bold">{{ result.Carbohydrates_Compliance }}</span></div>
          <div>Добавленный сахар или подсластитель: <span class="font-bold">{{ result.Sugar_Absence_Compliance }}</span>
          </div>
          <div>Общий белок: <span class="font-bold">{{ result.Protein_Compliance }}</span></div>
          <div>Общие жиры: <span class="font-bold">{{ result.Fat_Compliance }}</span></div>
          <div>Содержание фруктов: <span class="font-bold">{{ result.Fruits_Compliance }}</span></div>
        </div>

        <div>
          <div class="font-bold uppercase text-xl text-orange-500">Недопустимые маркетинговые заявления о составе
            продукции</div>
          <div>Поддержка и защита грудного вскармливания: <span class="font-bold">{{ result.Breastfeeding_Support
              }}</span></div>

          <div>Недопустимые заявления о составе продукции в рекламе:
            <span class="font-bold">{{
              result.Found_Health_Claims === 'Нет' ? 'Нет' : 'Да' }}</span>
            <span v-if="result.Found_Health_Claims !== 'Нет'" class="text-gray-400 font-light">
              (обнаружены ключевые слова: {{ result.Found_Health_Claims }})</span>
          </div>

          <div>Заявления об идеальном вкусе:
            <span class="font-bold">{{ result.Found_Taste_Claims === 'Нет' ? 'Нет' : 'Да' }}</span>
            <span v-if="result.Found_Taste_Claims !== 'Нет'" class="text-gray-400 font-light">
              (обнаружены ключевые слова: {{ result.Found_Taste_Claims }})</span>
          </div>

          <div>Заявления о высоком качестве продукции:
            <span class="font-bold">{{ result.Found_Quality_Claims === 'Нет' ? 'Нет' : 'Да' }}</span>
            <span v-if="result.Found_Quality_Claims !== 'Нет'" class="text-gray-400 font-light">
              (обнаружены ключевые слова: {{ result.Found_Quality_Claims }})</span>
          </div>

          <div>{{ result.Expert_Support_Compliance }}</div>
        </div>

        <div>
          <div class="font-bold uppercase text-xl text-orange-500">Микроэлементы и витамины</div>
          <div v-if="result.Клетчатка">Клетчатка: <span class="font-bold">{{ result.Клетчатка.toFixed(2) }} г</span></div>
          <div v-if="result.Vit_A">Витамин A: <span class="font-bold">{{ result.Vit_A.toFixed(2) }} мкг</span></div>
          <div v-if="result.Vit_B1">Витамин B1: <span class="font-bold">{{ result.Vit_B1.toFixed(2) }} мг</span></div>
          <div v-if="result.Vit_B2">Витамин B2: <span class="font-bold">{{ result.Vit_B2.toFixed(2) }} мг</span></div>
          <div v-if="result.Vit_B6">Витамин B6: <span class="font-bold">{{ result.Vit_B6.toFixed(2) }} мг</span></div>
          <div v-if="result.Vit_B12">Витамин B12: <span class="font-bold">{{ result.Vit_B12.toFixed(2) }} мкг</span>
          </div>
          <div v-if="result.Vit_C">Витамин C: <span class="font-bold">{{ result.Vit_C.toFixed(2) }} мг</span></div>
          <div v-if="result.Vit_PP">Витамин PP: <span class="font-bold">{{ result.Vit_PP.toFixed(2) }} мг</span></div>
          <div v-if="result.Натрий">Натрий: <span class="font-bold">{{ result.Натрий.toFixed(2) }} мг</span></div>
          <div v-if="result.Калий">Калий: <span class="font-bold">{{ result.Калий.toFixed(2) }} мг</span></div>
        </div>

        <div>
          <div class="font-bold uppercase text-xl text-orange-500">Дополнительная информация</div>
          <div>{{ result.Percentage_Presence }}</div>
        </div>
      </div>
      <div v-else-if="errorText">
        {{ errorText }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// import { reactive, ref } from 'vue';
import { ref, onUnmounted } from 'vue';
import axios from 'axios';
import BaseSpinner from './base/BaseSpinner.vue';
import BaseScale from './base/BaseScale.vue';
import BaseImageInput from "./base/BaseImageInput.vue";

const baseUrl = 'http://62.84.121.107:5000'
// const baseUrl = 'http://127.0.0.1:5000'

interface ResultInterface {
  "Brand": string;
  "Age_Recommendation": string | number
  "Breastfeeding_Support": string;
  "Carbohydrate": string | number;
  "Carbohydrates_Compliance": string;
  "Category": number;
  "Category_Description": string;
  "Energy_Compliance": string;
  "Expert_Support_Compliance": string;
  "Fat": string | number;
  "Fat_Compliance": string;
  "Final_Score": number;
  "Found_Health_Claims": string;
  "Found_Quality_Claims": string;
  "Found_Taste_Claims": string;
  "Fruits": string;
  "Fruits_Compliance": string;
  "Health_Claims_Compliance": string;
  "Percentage_Presence": string;
  "Protein": string;
  "Protein_Compliance": string;
  "Quality_Claims_Compliance": string;
  "Sodium": number | string;
  "Sodium_Compliance": string;
  "Sugar": string | number;
  "Sugar_Absence_Compliance": string;
  "Taste_Claims_Compliance": string;
  "Vit_A": number;
  "Vit_B1": number;
  "Vit_B12": number;
  "Vit_B2": number;
  "Vit_B6": number;
  "Vit_C": number;
  "Vit_D": number;
  "Vit_PP": number;
  "kcal": string | number;
  "Белки": number;
  "Жиры": number;
  "Калий": number;
  "Клетчатка": number;
  "Натрий": number;
  "Углеводы": number;
  "банан": number;
  "брокколи": number;
  "вода": number;
  "говядина": number;
  "груша": number;
  "индейка": number;
  "кабачок": number;
  "калорийность": number;
  "камедь": number;
  "крахмал": number;
  "кролик": number;
  "кукуруза": number;
  "кукурузная": number;
  "курица": number;
  "молоко": number;
  "морковь": number;
  "мультизлак": number;
  "овсяная": number;
  "персик": number;
  "пшеничная": number;
  "рис": number;
  "сахар": number;
  "слива": number;
  "соль": number;
  "творожок": number;
  "тыква": number;
  "цветная капуста": number;
  "яблоко": number;
}

const result = ref<undefined | ResultInterface>(undefined)
const errorText = ref('')
const isLoading = ref(false)
const resultBlock = ref<HTMLDivElement | undefined>(undefined)
const files = ref<Record<number, File>>({})

const loadingTextList = [
  'Пожалуйста, подождите, мы тщательно анализируем упаковку',
  'Проводим дегустацию на молекулярном уровне. Ваши данные скоро будут готовы',
  'Расшифровываем коды Е... Это как детектив, только про еду',
  'Секундочку, мы проверяем, не затесался ли сюда какой-нибудь скрытый сахар.',
  'Исследуем каждую калорию. У них нет шансов скрыться!',
  'Профессионально вглядываемся в список ингредиентов. Даже мелкий шрифт не помеха!',
  'Ведем переговоры с антиоксидантами. Пытаемся узнать их планы на будущее',
  'Сравниваем с дневной нормой витаминов. Ваши запасы в порядке?',
]
const loadingTextIndex = ref(0)

let intervalId: any = null

const submit = async () => {
  result.value = undefined
  window.scrollTo({ left: 0, top: (resultBlock.value?.offsetTop || 0) - 200, behavior: "smooth" })
  isLoading.value = true

  loadingTextIndex.value = 0 // Сбросить индекс, если нужно начинать сначала при каждом вызове
  intervalId = setInterval(() => {
    if (loadingTextIndex.value < loadingTextList.length - 1) {
      loadingTextIndex.value += 1
    } else {
      loadingTextIndex.value = 0
    }
  }, 4000)

  const formData = new FormData()

  Object.keys(files.value).forEach(ind => {
    formData.append(ind, files.value[Number(ind)])
  });

  try {
    const response = await axios.post(`${baseUrl}/analyse`, formData) as { data: { result: ResultInterface[] } }

    result.value = response.data.result[0]
  } catch (error: any) {
    console.error('Error making the request:', error);

    if (error.message === 'Network Error') {
      errorText.value = 'Извините, произошла ошибка, попробуйте еще раз.'
    } else {
      errorText.value = 'Ошибка в запросе'
    }
    setTimeout(() => {
      errorText.value = ''
    }, 2000)
  } finally {
    isLoading.value = false
    clearInterval(intervalId)
  }
}

async function onFileDelete(index: number) {
  delete files.value[index]
}

async function onFileChange(file: File, index: number) {
  console.log('🚀 ~ onFileChange ~ file:', file)
  files.value[index] = file
}

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>