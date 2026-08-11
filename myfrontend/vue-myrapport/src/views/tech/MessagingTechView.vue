<template>
  <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />

  <ComponentCard title="Mes messages">
    <div class="flex h-[calc(100vh-220px)] overflow-hidden rounded-xl border border-gray-200 dark:border-gray-700">

      <!-- ── Sidebar ── -->
      <aside class="w-72 flex-shrink-0 border-r border-gray-200 dark:border-gray-700 flex flex-col">

        <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
          <p class="text-sm font-semibold text-gray-700 dark:text-gray-200">Mes conversations</p>
        </div>

        <div class="flex-1 overflow-y-auto">
          <div v-if="store.loading" class="flex justify-center items-center py-8">
            <div class="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          </div>

          <button
            v-for="conv in store.conversations"
            :key="conv.id"
            @click="openConv(conv.id)"
            class="w-full flex items-center gap-3 px-4 py-3 text-left transition border-b border-gray-100 dark:border-gray-800"
            :class="store.activeConvId === conv.id
              ? 'bg-brand-50 dark:bg-brand-900/20'
              : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'"
          >
            <div
              class="flex items-center justify-center w-9 h-9 rounded-full shrink-0 text-sm font-semibold"
              :class="conv.type === 'group'
                ? 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300'
                : 'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300'"
            >
              {{ conv.name?.[0]?.toUpperCase() ?? '?' }}
            </div>

            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-1">
                <span class="text-sm font-medium text-gray-800 dark:text-gray-100 truncate">
                  {{ conv.name }}
                </span>
                <span
                  class="text-xs px-1.5 py-0.5 rounded-full font-medium shrink-0"
                  :class="conv.type === 'group'
                    ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                    : conv.type === 'shared_admin'
                    ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                    : 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'"
                >
                  {{ typeLabel(conv.type) }}
                </span>
              </div>
              <p class="text-xs text-gray-400 dark:text-gray-500 truncate mt-0.5">
                {{ conv.last_message?.content ?? 'Aucun message' }}
              </p>
            </div>
          </button>

          <div
            v-if="!store.loading && store.conversations.length === 0"
            class="py-10 text-center text-sm text-gray-400 dark:text-gray-500"
          >
            Aucune conversation
          </div>
        </div>
      </aside>

      <!-- ── Zone chat ── -->
      <div class="flex-1 flex flex-col overflow-hidden">

        <!-- Header -->
        <div v-if="store.activeConv" class="flex items-center justify-between px-5 py-3 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center gap-3">
            <div class="flex items-center justify-center w-8 h-8 rounded-full text-sm font-semibold bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300">
              {{ store.activeConv.name?.[0]?.toUpperCase() }}
            </div>
            <div>
              <p class="text-sm font-semibold text-gray-800 dark:text-white">{{ store.activeConv.name }}</p>
              <p class="text-xs text-gray-400">{{ store.activeConv.members.length }} membre(s)</p>
            </div>
          </div>
          <span
            class="text-xs px-2 py-1 rounded-full font-medium"
            :class="store.activeConv.type === 'group'
              ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
              : store.activeConv.type === 'shared_admin'
              ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
              : 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'"
          >
            {{ typeLabel(store.activeConv.type) }}
          </span>
        </div>

        <!-- Messages -->
        <div class="flex-1 overflow-y-auto p-5 space-y-4" ref="scrollRef">

          <div v-if="!store.activeConv" class="h-full flex flex-col items-center justify-center gap-3 text-gray-400 dark:text-gray-500">
            <svg class="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
            <p class="text-sm">Sélectionnez une conversation</p>
          </div>

          <template v-else>
            <div
              v-for="msg in store.messages"
              :key="msg.id"
              class="flex gap-3"
              :class="msg.sender_id === authStore.user?.id ? 'flex-row-reverse' : 'flex-row'"
            >
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold shrink-0"
                :class="msg.sender_role === 'admin'
                  ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300'
                  : 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300'"
                :title="msg.sender_name"
              >
                {{ msg.sender_name[0]?.toUpperCase() }}
              </div>

              <div
                class="max-w-[65%] flex flex-col gap-1"
                :class="msg.sender_id === authStore.user?.id ? 'items-end' : 'items-start'"
              >
                <div class="flex items-baseline gap-2">
                  <span class="text-xs font-medium text-gray-500 dark:text-gray-400">{{ msg.sender_name }}</span>
                  <span class="text-xs text-gray-400 dark:text-gray-500">{{ formatTime(msg.sent_at) }}</span>
                </div>
                <div
                  class="px-4 py-2.5 rounded-2xl text-sm leading-relaxed"
                  :class="msg.sender_id === authStore.user?.id
                    ? 'bg-brand-500 text-white rounded-tr-sm'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-tl-sm'"
                >
                  {{ msg.content }}
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- Input — tech répond uniquement -->
        <div v-if="store.activeConv" class="px-4 py-3 border-t border-gray-200 dark:border-gray-700">
          <div class="flex items-end gap-3">
            <TextareaInput
              v-model="draft"
              :rows="1"
              placeholder="Répondre… (Entrée pour envoyer)"
              class="flex-1 resize-none rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-sm text-gray-800 dark:text-gray-100 px-4 py-2.5 focus:outline-none focus:border-brand-400 dark:focus:border-brand-500 transition max-h-32"
              @keydown.enter.exact.prevent="send"
            />
            <button
              @click="send"
              :disabled="!draft.trim()"
              class="flex items-center justify-center w-10 h-10 rounded-xl bg-brand-500 hover:bg-brand-600 disabled:opacity-40 disabled:cursor-not-allowed text-white transition shrink-0"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
            </button>
          </div>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-1.5 px-1">
            Vous pouvez répondre uniquement aux conversations où vous êtes inclus
          </p>
        </div>
      </div>
    </div>
  </ComponentCard>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'
import { useMessagingStore, type ConvType } from '@/stores/messaging'
import { useAuthStore } from '@/stores/auth'
import TextareaInput from '@/components/FormElement/TextareaInput.vue'

const currentPageTitle = ref('Messagerie')
const store     = useMessagingStore()
const authStore = useAuthStore()
const route     = useRoute()
const router    = useRouter()
const draft     = ref('')
const scrollRef = ref<HTMLElement | null>(null)

onMounted(async () => {
  await store.fetchConversations()
  const id = Number(route.params.convId)
  if (id && !isNaN(id)){
    await store.fetchMessages(id)
    }
})

watch(() => route.params.convId,  async id => {
   if (id && !isNaN(Number(id))) {
    await store.fetchMessages(Number(id))
  }
}, { immediate: false })

watch(() => store.messages, () => {
   nextTick(() => {
    if (scrollRef.value)
      scrollRef.value.scrollTop = scrollRef.value.scrollHeight
  })
}, { deep: true })

function openConv(id: number): void {
  router.push({ name: 'tech-messaging-conv', params: { convId: id } })
}

async function send(): Promise<void> {
  if (!draft.value.trim() || !store.activeConvId) return
  await store.sendMessage(store.activeConvId, draft.value.trim())
  draft.value = ''
}

const typeLabel = (t: ConvType): string =>
  ({ shared_admin: 'Admins', private: 'Privé', group: 'Groupe' }[t])

const formatTime = (iso: string): string =>
  new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
</script>