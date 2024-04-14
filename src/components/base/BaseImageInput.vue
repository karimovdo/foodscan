<template>
  <div class="flex items-center w-full flex-col gap-2">
    <div
      class="relative flex items-center justify-center w-full min-h-[300px] cursor-pointer group border-2 transition border-gray-300 rounded-lg overflow-hidden hover:border-gray-400"
      @click="!preview && inputElement?.click()">
      <img v-if="preview" ref="imageElement" class="block w-full h-full object-contain" :src="preview" />
      <svg v-if="!preview" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
        class="text-gray-400 w-6 sm:w-12 h-6 sm:h-12">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
          d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <div v-if="cropper && preview" class="flex gap-2 absolute top-4 right-4 z-10 justify-end items-center">
        <button
          class="w-10 h-10 bg-blue-600 transition hover:bg-blue-500 p-1.5 rounded-lg flex items-center justify-center"
          @click="onZoom(-0.1)">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="text-white w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14" />
          </svg>
        </button>
        <button
          class="w-10 h-10 bg-blue-600 transition hover:bg-blue-500 p-1.5 rounded-lg flex items-center justify-center"
          @click="onZoom(0.1)">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="text-white w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
        </button>
        <button
          class="w-10 h-10 bg-blue-600 transition hover:bg-blue-500 p-1.5 rounded-lg flex items-center justify-center"
          @click="onRotate">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="text-white w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round"
              d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
        </button>
        <button
          class="w-10 h-10 bg-red-600 transition hover:bg-red-500 p-1.5 rounded-lg flex items-center justify-center"
          @click="onDelete">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="text-white w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round"
              d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
          </svg>
        </button>
      </div>
    </div>
    <div v-if="getDeviceType() === 'mobile'" class="flex gap-2">
      <button class="bg-amber-400 p-1.5 rounded-lg" @click="inputElement?.click()">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
          class="text-white w-6 sm:w-12 h-6 sm:h-12">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </button>
      <button class="bg-orange-500 p-1.5 rounded-lg" @click="inputCameraElement?.click()">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
          class="text-white w-6 sm:w-12 h-6 sm:h-12">
          <path strokeLinecap="round" strokeLinejoin="round" stroke-width="1.5"
            d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z" />
          <path strokeLinecap="round" strokeLinejoin="round" stroke-width="1.5"
            d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0ZM18.75 10.5h.008v.008h-.008V10.5Z" />
        </svg>
      </button>
    </div>
    <input ref="inputElement" class="hidden" type="file" @change="onChange" :accept="accept.join(', ')" />
    <input ref="inputCameraElement" class="hidden" type="file" @change="onChange" :accept="accept.join(', ')"
      capture="environment" />
  </div>

</template>

<script setup lang='ts'>
import { ref, nextTick } from 'vue'
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'

const emit = defineEmits(['upload', 'delete'])

const inputElement = ref<HTMLInputElement | undefined>(undefined)
const inputCameraElement = ref<HTMLInputElement | undefined>(undefined)
const preview = ref<any>(null)
const cropper = ref<Cropper | null>(null)
const imageElement = ref<HTMLImageElement | null>(null)
const fileType = ref('image/jpeg')
const fileName = ref('')

const accept = ['image/png', 'image/jpg', 'image/jpeg']

function save() {
  const canvas = cropper.value?.getCroppedCanvas()

  if (!canvas) { return }

  canvas.toBlob(
    (blob) => {
      if (!blob) {
        return
      }

      const file = new File(
        [blob],
        fileName.value,
        {
          lastModified: Date.now(),
          type: fileType.value,
        }
      )

      emit('upload', file)
    },
    fileType.value,
    1
  )
}


function onRotate() {
  if (!cropper.value) {
    return
  }

  cropper.value.rotate(90)
  save()
}

async function onZoom(zoom: number) {
  cropper.value?.zoom(zoom)
  save()
}


async function initCropper(file: File | null) {
  if (file) {
    await nextTick()

    if (imageElement.value) {
      if (cropper.value) {
        cropper.value.destroy()
      }

      cropper.value = new Cropper(imageElement.value, {
        viewMode: 2,
        autoCropArea: 0.9,
        minContainerHeight: 200,
        zoomOnWheel: false,
        cropend: () => save(),
      })
    }
  }
}

function onDelete() {
  preview.value = undefined
  cropper.value?.destroy()
  emit('delete')
}

function getDeviceType() {
  const userAgent = navigator.userAgent.toLowerCase();
  const isMobile = /mobile|iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(userAgent);

  if (isMobile) {
    return "mobile";
  } else {
    return "desktop";
  }
}

async function readFile(file: File) {
  return new Promise(resolve => {
    if (!file) {
      resolve('')
    }
    const reader = new FileReader()

    reader.addEventListener('load', () => resolve(reader.result), false)
    reader.readAsDataURL(file)
  })
}

async function onChange(event: Event) {
  const target = event.target as HTMLInputElement

  if (target && target.files?.length) {
    const file = target.files[0]

    if (accept.includes(file.type)) {
      const fileData = await readFile(file) as File
      preview.value = fileData
      fileName.value = file.name
      fileType.value = file.type
      initCropper(fileData)
      emit('upload', file)
    }
  }
}
</script>
