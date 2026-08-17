<template>
  <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />

  <ComponentCard title="Messagerie">
    <div class="flex h-[calc(100vh-220px)] overflow-hidden rounded-xl border border-gray-200 dark:border-gray-700">

      <!-- ── Sidebar ── -->
      <aside class="w-72 flex-shrink-0 border-r border-gray-200 dark:border-gray-700 flex flex-col">

        <!-- Header sidebar -->
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">Conversations</span>
          <button
            @click="openModal"
            class="p-1.5 rounded-lg text-gray-400 hover:text-brand-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition"
            title="Nouvelle conversation"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
          </button>
        </div>

        <!-- Espace commun admins -->
        <!-- <button
          @click="openSharedAdmin"
          class="flex items-center gap-3 mx-3 my-2 px-3 py-2.5 rounded-xl text-left transition"
          :class="activeType === 'shared_admin'
            ? 'bg-brand-50 dark:bg-brand-900/20 border border-brand-200 dark:border-brand-700'
            : 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-900/30'"
        > -->
        <button
          class="flex items-center gap-3 mx-3 my-2 px-3 py-2.5 rounded-xl text-left transition"
          :class="activeType === 'shared_admin'
            ? 'bg-brand-50 dark:bg-brand-900/20 border border-brand-200 dark:border-brand-700'
            : 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-900/30'"
        >
          <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/40 shrink-0">
            <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 20h5v-2a4 4 0 00-5-3.87M9 20H4v-2a4 4 0 015-3.87m6-4a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
          </div>
          <div class="min-w-0">
            <p class="text-sm font-medium text-blue-700 dark:text-blue-300 truncate">Espace admins</p>
            <p class="text-xs text-blue-500 dark:text-blue-400 truncate">Commun à tous les admins</p>
          </div>
        </button>

        <!-- Séparateur -->
        <p class="px-4 pt-2 pb-1 text-xs font-medium uppercase tracking-wider text-gray-400 dark:text-gray-500">
          Mes conversations
        </p>

        <!-- Liste conversations -->
        <div class="flex-1 overflow-y-auto">
          <div v-if="store.loading" class="flex justify-center items-center py-8">
            <div class="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          </div>

          <button
            v-for="conv in convsFiltrees"
            :key="conv.id"
            @click="openConv(conv.id)"
            class="w-full flex items-center gap-3 px-4 py-3 text-left transition border-b border-gray-100 dark:border-gray-800"
            :class="store.activeConvId === conv.id
              ? 'bg-brand-50 dark:bg-brand-900/20'
              : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'"
          >
            <!-- Avatar -->
            <div class="flex items-center justify-center w-9 h-9 rounded-full shrink-0 text-sm font-semibold"
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
                    : 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'"
                >
                  {{ conv.type === 'group' ? 'Groupe' : 'Privé' }}
                </span>
              </div>
              <p class="text-xs text-gray-400 dark:text-gray-500 truncate mt-0.5">
                {{ conv.last_message?.content ?? 'Aucun message' }}
              </p>
            </div>
          </button>

          <div
            v-if="!store.loading && convsFiltrees.length === 0"
            class="py-8 text-center text-sm text-gray-400 dark:text-gray-500"
          >
            Aucune conversation
          </div>
        </div>
      </aside>

      <!-- ── Zone chat ── -->
      <div class="flex-1 flex flex-col overflow-hidden">

        <div v-if="store.activeConv" class="flex items-center justify-between px-5 py-3 border-b border-gray-200 dark:border-gray-700">
          <!-- Gauche — nom + membres count -->
          <div class="flex items-center gap-3">
            <div class="flex items-center justify-center w-8 h-8 rounded-full text-sm font-semibold bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300">
              {{ store.activeConv.name?.[0]?.toUpperCase() }}
            </div>
            <div>
              <p class="text-sm font-semibold text-gray-800 dark:text-white">{{ store.activeConv.name }}</p>
              <p class="text-xs text-gray-400">{{ store.activeConv.members.length }} membre(s)</p>
            </div>
          </div>

          <!-- Droite — avatars + menu -->
          <div class="flex items-center gap-3">

            <!-- Avatars membres -->
            <div class="flex items-center -space-x-2">
              <div
                v-for="m in store.activeConv.members.slice(0, 5)"
                :key="m.user_id"
                class="w-7 h-7 rounded-full border-2 border-white dark:border-gray-900 flex items-center justify-center text-xs font-medium"
                :class="m.role === 'admin'
                  ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300'
                  : 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300'"
                :title="m.username"
              >
                {{ m.username[0]?.toUpperCase() }}
              </div>
              <div
                v-if="store.activeConv.members.length > 5"
                class="w-7 h-7 rounded-full border-2 border-white dark:border-gray-900 bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-xs text-gray-600 dark:text-gray-300"
              >
                +{{ store.activeConv.members.length - 5 }}
              </div>
            </div>

            <!-- Menu actions admin -->
            <div v-if="authStore.user?.role === 'admin'" class="relative" ref="menuRef">
              <button
                @click="showConvMenu = !showConvMenu"
                class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01"/>
                </svg>
              </button>

              <div
                v-if="showConvMenu"
                class="absolute right-0 top-8 w-52 bg-white dark:bg-gray-900 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 z-10"
              >
                <button
                  v-if="store.activeConv.type === 'group'"
                  @click="openAddMember"
                  class="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-t-xl"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                  </svg>
                  Ajouter un membre
                </button>

                <button
                  v-if="store.activeConv.type === 'group'"
                  @click="openRemoveMember"
                  class="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7a4 4 0 11-8 0 4 4 0 018 0zM9 14a6 6 0 00-6 6v1h12v-1a6 6 0 00-6-6zM21 12h-6"/>
                  </svg>
                  Retirer un membre
                </button>

                <button
                  @click="confirmDeleteConv"
                  class="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-b-xl"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                  Supprimer la conversation
                </button>
              </div>
            </div>

          </div>
        </div>

        <!-- #########################"" -->
        <!-- Messages -->
        <div class="flex-1 overflow-y-auto p-5 space-y-4" ref="scrollRef">

          <!-- État vide -->
          <div v-if="!store.activeConv" class="h-full flex flex-col items-center justify-center gap-3 text-gray-400 dark:text-gray-500">
            <svg class="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
            <p class="text-sm">Sélectionnez une conversation</p>
          </div>

          <!-- Bulles messages -->
          <template v-else>
            <div
              v-for="msg in store.messages"
              :key="msg.id"
              class="flex gap-3 group"
              :class="msg.sender_id === authStore.user?.id ? 'flex-row-reverse' : 'flex-row'"
            >
              <!-- Avatar sender -->
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold shrink-0"
                :class="msg.sender_role === 'admin'
                  ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300'
                  : 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300'"
                :title="msg.sender_name"
              >
                {{ msg.sender_name[0]?.toUpperCase() }}
              </div>

              <div class="max-w-[65%] flex flex-col gap-1"
                :class="msg.sender_id === authStore.user?.id ? 'items-end' : 'items-start'"
              >
                <div class="flex items-baseline gap-2">
                  <span class="text-xs font-medium text-gray-500 dark:text-gray-400">{{ msg.sender_name }}</span>
                  <span class="text-xs text-gray-400 dark:text-gray-500">{{ formatTime(msg.sent_at) }}</span>
                </div>
                <div class="flex items-center gap-1"
                  :class="msg.sender_id === authStore.user?.id ? 'flex-row-reverse' : 'flex-row'"
                  >
                  <div
                    class="px-4 py-2.5 rounded-2xl text-sm leading-relaxed"
                    :class="msg.sender_id === authStore.user?.id
                      ? 'bg-brand-500 text-white rounded-tr-sm'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-tl-sm'"
                  >
                    {{ msg.content }}
                  </div>

                  <button
                    v-if="msg.sender_id === authStore.user?.id || authStore.user?.role === 'admin'"
                    @click="deleteMsg(msg.id)"
                    class="opacity-0 group-hover:opacity-100 transition-opacity p-1 text-gray-400 hover:text-red-500 rounded"
                    title="Supprimer"
                  >
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- Input message -->
        <div v-if="store.activeConv" class="px-4 py-3 border-t border-gray-200 dark:border-gray-700">
          <div class="flex items-end gap-3">
            <TextareaInput
              v-model="draft"
              :rows="1"
              placeholder="Votre message… (Entrée pour envoyer)"
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
        </div>
      </div>
    </div>
  </ComponentCard>

  <!-- ── Modal nouvelle conversation ── -->
  <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="w-full max-w-lg bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">

      <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
        Nouvelle conversation
      </h2>

      <!-- Tabs type -->
      <div class="flex gap-2 mb-5">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="mode = tab.value"
          class="flex-1 py-2 text-sm rounded-lg border font-medium transition"
          :class="mode === tab.value
            ? 'bg-brand-500 border-brand-500 text-white'
            : 'border-gray-300 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Nom du groupe -->
      <div v-if="mode === 'group'" class="mb-4">
        <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
          Nom du groupe
        </label>
        <input
          v-model="groupName"
          type="text"
          placeholder="Ex : Site TNR"
          class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-sm px-3 py-2.5 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-brand-400 transition"
        />
      </div>

      <!-- Message broadcast -->
      <div v-if="mode === 'broadcast'" class="mb-4">
        <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
          Message à diffuser
        </label>
        <TextareaInput
          v-model="broadcastContent"
          :rows="3"
          placeholder="Ce message sera envoyé à chaque tech sélectionné…"
          class="w-full resize-none rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-sm px-3 py-2.5 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-brand-400 transition"
        />
      </div>

      <!-- Sélection techs -->
      <div class="mb-5">
        <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-400">
          Sélectionner les techniciens
        </label>
        <div class="max-h-48 overflow-y-auto space-y-1 border border-gray-200 dark:border-gray-700 rounded-lg p-2">
            
            <!-- Checkbox "Tous" au-dessus de la liste -->
            <label v-if="mode === 'broadcast'" class="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition border-b border-gray-200 dark:border-gray-700 mb-1">
              <input
                type="checkbox"
                :checked="selectedTechs.length === techList.length && techList.length > 0"
                :indeterminate="selectedTechs.length > 0 && selectedTechs.length < techList.length"
                @change="toggleAll"
                class="accent-brand-500 w-4 h-4"
              />
              <div class="flex items-center justify-center w-7 h-7 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs font-semibold shrink-0">
                <CheckIcon/>
              </div>
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Tous</span>
            </label>

            <!-- Spinner chargement -->
            <div v-if="techsLoading" class="flex justify-center items-center py-6">
                <div class="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
            
            <!-- Liste techs -->
            <template v-else>
              <div v-if="techList.length === 0" class="py-3 text-center text-sm text-gray-400">
                  Aucun technicien trouvé
              </div>
              <label
                  v-for="tech in techList"
                  :key="tech.value"
                  class="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition"
              >
                  <input type="checkbox" :value="tech.value" v-model="selectedTechs" class="accent-brand-500 w-4 h-4" />
                  <div class="flex items-center justify-center w-7 h-7 rounded-full bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-300 text-xs font-semibold shrink-0">
                  {{ tech.label?.[0]?.toUpperCase() ?? '?' }}
                  </div>
                  <span class="text-sm text-gray-700 dark:text-gray-300">{{ tech.label }}</span>
              </label>
            </template>
        </div>
      </div>

      <!-- Actions modal -->
      <div class="flex justify-end gap-3">
        <button
          @click="closeModal"
          class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-800 transition"
        >
          Annuler
        </button>
        <button
          @click="createConversation"
          :disabled="!canCreate"
          class="px-4 py-2 text-sm text-white bg-brand-500 rounded-lg hover:bg-brand-600 disabled:opacity-40 disabled:cursor-not-allowed transition"
        >
          {{ mode === 'broadcast' ? 'Envoyer à tous' : 'Créer' }}
        </button>
      </div>
    </div>
  </div>


  <!-- Modal choix envoi — apparaît au clic sur le bouton send -->
  <div v-if="showSendChoice" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="w-full max-w-xs bg-white dark:bg-gray-900 rounded-xl shadow-xl p-5">
      <h2 class="text-base font-semibold text-gray-800 dark:text-white mb-4">
        Choisir le mode d'envoi
      </h2>

      <div class="space-y-2">
        <!-- Instantané -->
        <button
          @click="sendInstant"
          class="w-full flex items-center gap-3 px-4 py-3 text-sm text-left rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-brand-50 hover:border-brand-300 dark:hover:bg-gray-700/20 transition"
        >
          <span class="text-gray-400 text-lg"><SmsIcon/></span>
          <div>
            <p class="font-medium text-gray-800 dark:text-white">Instantané</p>
            <p class="text-xs text-gray-400">Envoyé dans l'espace de discussion</p>
          </div>
        </button>

        <!-- Personnel SMS -->
        <button
          @click="sendSmsChoice"
          class="w-full flex items-center gap-3 px-4 py-3 text-sm text-left rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-orange-50 hover:border-orange-300 dark:hover:bg-orange-900/20 transition"
        >
          <span class="text-gray-400 text-lg"><PhoneIcon/></span>
          <div>
            <p class="font-medium text-gray-800 dark:text-white">Personnel (SMS)</p>
            <p class="text-xs text-gray-400">
              Envoyé au numéro personnel du technicien
            </p>
          </div>
        </button>
      </div>

      <div class="flex justify-end mt-4">
        <button
          @click="showSendChoice = false"
          class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400"
        >
          Annuler
        </button>
      </div>
    </div>
  </div>

  <!-- Modal confirmation SMS -->
  <div v-if="showSmsConfirm" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/50">
    <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
      <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
        Messagerie personnelle (SMS)
      </h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">
        Message à envoyer :
      </p>
      <p class="truncate text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-3">
        {{ draft }}
      </p>
      <p class="flex items-center gap-2 text-xs text-orange-500 mb-4">
        <WarningTriangleIcon
          class="text-orange-500"
        /> 
        Le technicien ne pourra pas répondre à ce SMS.
      </p>

      <!-- Résultat -->
      <div v-if="smsResult" class="mb-4 space-y-1">
        <p class="flex items-center gap-2 text-sm text-green-600">
          <checkIcon/> {{ smsResult.total_envoye }} SMS envoyé(s)
        </p>
        <p v-if="smsResult.total_erreur > 0" class=" text-sm text-red-500">
          <div 
            v-for="e in smsResult.errors" 
            :key="e.tech" 
            class="block text-xs">
              <div class="flex items-center gap-2 text-sm text-red-500">
                <ErrorCircleIcon /> {{ smsResult.total_erreur }} erreur(s) :
              </div>
              <p v-if="e.error === 'Numéro de téléphone manquant'">
                {{ e.tech }} n'a pas de numéro téléphone enregistré.
              </p>
              <p v-else>
                <!-- {{ e.tech }} — {{ e.error }} -->
                Une erreur s'est produite veuillez reéssayer ulterieurement!
              </p>
            </div>
        </p>
      </div>

      <div class="flex justify-end gap-3">
        <button
          @click="showSmsConfirm = false; smsResult = null"
          class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700"
        >
          {{ smsResult ? 'Fermer' : 'Annuler' }}
        </button>
        <button
          v-if="!smsResult"
          @click="confirmSendSms"
          :disabled="smsSending"
          class="px-4 py-2 text-sm text-white bg-orange-500 rounded-lg hover:bg-orange-600 disabled:opacity-40 transition"
        >
          {{ smsSending ? 'Envoi...' : 'Envoyer SMS' }}
        </button>
      </div>
    </div>
  </div>

  <!-- Modal ajouter membre -->
  <div v-if="showAddMemberModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
      <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
        Ajouter un membre
      </h2>

      <div v-if="addableTechs.length === 0" class="text-center text-sm text-gray-400 py-4">
        Tous les techniciens sont déjà membres.
      </div>

      <div v-else class="max-h-60 overflow-y-auto space-y-1 border border-gray-200 dark:border-gray-700 rounded-lg p-2 mb-4">
        <label
          v-for="tech in addableTechs"
          :key="tech.value"
          class="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition"
        >
          <input type="checkbox" :value="tech.value" v-model="selectedToAdd" class="accent-brand-500 w-4 h-4" />
          <div class="flex items-center justify-center w-7 h-7 rounded-full bg-green-100 dark:bg-green-900/40 text-green-700 text-xs font-semibold shrink-0">
            {{ tech.label?.[0]?.toUpperCase() ?? '?' }}
          </div>
          <span class="text-sm text-gray-700 dark:text-gray-300">{{ tech.label }}</span>
        </label>
      </div>

      <div class="flex justify-end gap-3">
        <button @click="showAddMemberModal = false; selectedToAdd = []"
          class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700">
          Annuler
        </button>
        <button
          @click="submitAddMembers"
          :disabled="selectedToAdd.length === 0"
          class="px-4 py-2 text-sm text-white bg-brand-500 rounded-lg hover:bg-brand-600 disabled:opacity-40"
        >
          Ajouter ({{ selectedToAdd.length }})
        </button>
      </div>
    </div>
  </div>

  <!-- Modal retirer membre -->
  <div v-if="showRemoveMemberModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
      <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
        Retirer un membre
      </h2>

      <div class="max-h-60 overflow-y-auto space-y-1 border border-gray-200 dark:border-gray-700 rounded-lg p-2 mb-4">
        <label
          v-for="m in removableMembers"
          :key="m.user_id"
          class="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition"
        >
          <input type="checkbox" :value="m.user_id" v-model="selectedToRemove" class="accent-red-500 w-4 h-4" />
          <div
            class="flex items-center justify-center w-7 h-7 rounded-full text-xs font-semibold shrink-0"
            :class="m.role === 'admin'
              ? 'bg-blue-100 text-blue-700'
              : 'bg-green-100 text-green-700'"
          >
            {{ m.username?.[0]?.toUpperCase() ?? '?' }}
          </div>
          <div>
            <span class="text-sm text-gray-700 dark:text-gray-300">{{ m.username }}</span>
            <span class="text-xs text-gray-400 ml-2">{{ m.role }}</span>
          </div>
        </label>
      </div>

      <div class="flex justify-end gap-3">
        <button @click="showRemoveMemberModal = false; selectedToRemove = []"
          class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700">
          Annuler
        </button>
        <button
          @click="submitRemoveMembers"
          :disabled="selectedToRemove.length === 0"
          class="px-4 py-2 text-sm text-white bg-red-500 rounded-lg hover:bg-red-600 disabled:opacity-40"
        >
          Retirer ({{ selectedToRemove.length }})
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'
import { useMessagingStore, type ConvType,type SmsResultat } from '@/stores/messaging'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import TextareaInput from '@/components/FormElement/TextareaInput.vue'
import CheckIcon from '@/icons/checkIcon.vue'
import SmsIcon from '@/icons/SmsIcon.vue'
import PhoneIcon from '@/icons/PhoneIcon.vue'
import ErrorIcon from '@/icons/ErrorIcon.vue'
import { checkIcon } from '@/icons'
import WarningTriangleIcon from '@/icons/WarningTriangleIcon.vue'
import WarningIcon from '@/icons/WarningIcon.vue'
import ErrorCircleIcon from '@/icons/ErrorCircleIcon.vue'
import API_CONFIG from '@/config/api'

const currentPageTitle = ref('Messagerie')
const store     = useMessagingStore()
const authStore = useAuthStore()
const route     = useRoute()
const router    = useRouter()

// --- Chat ---------------------------------------------------------
const draft     = ref('')
const scrollRef = ref<HTMLElement | null>(null)
const activeType = computed(() => store.activeConv?.type)

const convsFiltrees = computed(() =>
  store.conversations.filter(c => c.type !== 'shared_admin')
)

onMounted(async () => {
  await store.fetchConversations()
  const id = Number(route.params.convId)
  if (id) store.fetchMessages(id)
})

watch(() => route.params.convId, id => {
  if (id) store.fetchMessages(Number(id))
})

watch(() => store.messages, () => {
  nextTick(() => {
    if (scrollRef.value)
      scrollRef.value.scrollTop = scrollRef.value.scrollHeight
  })
}, { deep: true })

function openConv(id: number): void {
  router.push({ name: 'admin-messaging-conv', params: { convId: id } })
}

async function openSharedAdmin(): Promise<void> {
  await store.fetchSharedAdmin()
  if (store.activeConvId) {
    router.push({ name: 'admin-messaging-conv', params: { convId: store.activeConvId } })
  }
}

async function send(): Promise<void> {
  if (!draft.value.trim() || !store.activeConvId) return

  // Si admin -> proposer le choix
  if (authStore.user?.role === 'admin') {
    showSendChoice.value = true
    return
  }


  // Si tech -> envoyer directement en instantané
  await sendInstant()

}

//Envoi instantané — dans la conversation
async function sendInstant(): Promise<void> {
  showSendChoice.value = false
  if (!draft.value.trim() || !store.activeConvId) return
  await store.sendMessage(store.activeConvId, draft.value.trim())
  draft.value = ''
}

//Choix SMS — ouvrir confirmation
function sendSmsChoice(): void {
  showSendChoice.value = false
  showSmsConfirm.value = true
}

// Confirmer et envoyer SMS
async function confirmSendSms(): Promise<void> {
  smsSending.value = true
  try {
    // Récupérer les membres de la conversation (hors admin)
    const conv = store.activeConv
    if (!conv) return

    const techIds = conv.members
      .filter(m => m.role === 'tech')
      .map(m => m.user_id)

    const result = await store.sendSms(techIds, draft.value.trim())
    smsResult.value = result

    // Si tout envoyé -> vider le draft
    if (result.total_erreur === 0) {
      draft.value = ''
    }

  } catch (err) {
    console.error('Erreur SMS:', err)
  } finally {
    smsSending.value = false
  }
}

// --- Modal groupe-------------------------------------------------------------
const showModal = ref(false)
const mode = ref<'private' | 'broadcast' | 'group'>('private')
const groupName = ref('')
const broadcastContent = ref('')
const selectedTechs = ref<number[]>([])
const techList = ref<{ value: number; label: string }[]>([])
const techsLoaded = ref(false)   
const techsLoading = ref(false)

// --- Modal sms ------------------------------------------------------------
const showSendChoice = ref(false)
const showSmsConfirm = ref(false)
const smsSending     = ref(false)
const smsResult      = ref<SmsResultat | null>(null)

//Menu membres
const showConvMenu          = ref(false)
const showAddMemberModal    = ref(false)
const showRemoveMemberModal = ref(false)
const menuRef               = ref<HTMLElement | null>(null)
const selectedToAdd         = ref<number[]>([])
const selectedToRemove      = ref<number[]>([])


const tabs = [
  { value: 'private'   as const, label: 'Privée' },
  { value: 'broadcast' as const, label: 'Diffusion' },
  { value: 'group'     as const, label: 'Groupe' },
]

const canCreate = computed(() => {
  if (!selectedTechs.value.length) return false
  if (mode.value === 'group'     && !groupName.value.trim()) return false
  if (mode.value === 'broadcast' && !broadcastContent.value.trim()) return false
  return true
})

async function loadTechs(): Promise<void> {
    if (techsLoaded.value) return 
    techsLoading.value = true

    try{
       const token = sessionStorage.getItem('token')
        const { data } = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/tech`,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        )
        console.log('API users response:', JSON.stringify(data, null, 2))
        const list = Array.isArray(data) ? data : (data.results ?? [])
        techList.value = list.filter((u: any) => u && u.value && u.label)
        techsLoaded.value = true
    } catch (err) {
        console.error('Erreur chargement techs:', err)
    } finally {
        techsLoading.value = false
    }
  
}

function openModal(): void {
  // Réinitialise l'état du modal avant de l'ouvrir
  mode.value             = 'private'
  groupName.value        = ''
  broadcastContent.value = ''
  selectedTechs.value    = []
  showModal.value        = true
  loadTechs()   // charge les techs (idempotent grâce à techsLoaded)
}

async function createConversation(): Promise<void> {
  if (!canCreate.value) return
  try{
      if (mode.value === 'private')   await store.createPrivateConv(selectedTechs.value)
      if (mode.value === 'broadcast') await store.broadcastMessage(selectedTechs.value, broadcastContent.value)
      if (mode.value === 'group')     await store.createGroup(groupName.value, selectedTechs.value)
      closeModal()
  } catch (err) {
    console.error('Erreur création conversation:', err)
  }
}

function closeModal(): void {
  showModal.value     = false
  mode.value          = 'private'
  groupName.value     = ''
  broadcastContent.value = ''
  selectedTechs.value = []
}

// Ajouter dans le script
const toggleAll = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked
  if (checked) {
    selectedTechs.value = techList.value.map(t => t.value)  // sélectionner tous
  } else {
    selectedTechs.value = []  // désélectionner tous
  }
}

// Fermer menu membre si clic extérieur
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (menuRef.value && !menuRef.value.contains(e.target as Node)) {
      showConvMenu.value = false
    }
  })
})

// Supprimer message
async function deleteMsg(msgId: number): Promise<void> {
  if (!store.activeConvId) return
  await store.deleteMessage(store.activeConvId, msgId)
}

//Supprimer conversation
async function confirmDeleteConv(): Promise<void> {
  showConvMenu.value = false
  if (!store.activeConvId) return
  if (!confirm('Supprimer cette conversation ?')) return
  await store.deleteConversation(store.activeConvId)
}

// Techs pas encore dans la conversation
const addableTechs = computed(() => {
  if (!store.activeConv) return []
  const memberIds = store.activeConv.members.map(m => m.user_id)
  return techList.value.filter(t => !memberIds.includes(t.value))
})

// Membres retirables (pas le créateur)
const removableMembers = computed(() => {
  if (!store.activeConv) return []
  return store.activeConv.members.filter(m => m.role === 'tech')
})

// Ouvrir modal ajout — charger techs si pas encore fait
const openAddMember = async () => {
  showConvMenu.value = false
  await loadTechs()
  selectedToAdd.value = []
  showAddMemberModal.value = true
}

const openRemoveMember = () => {
  showConvMenu.value = false
  selectedToRemove.value = []
  showRemoveMemberModal.value = true
}

// Soumettre ajout — un par un
const submitAddMembers = async () => {
  if (!store.activeConvId) return
  try {
    for (const userId of selectedToAdd.value) {
      await store.addMember(store.activeConvId, userId)
    }
    showAddMemberModal.value = false
    selectedToAdd.value = []
    // Rafraîchir la conversation active
    await store.fetchConversations()
  } catch (err) {
    console.error('Erreur ajout membre:', err)
  }
}


// Soumettre retrait — un par un
const submitRemoveMembers = async () => {
  if (!store.activeConvId) return
  try {
    for (const userId of selectedToRemove.value) {
      await store.removeMember(store.activeConvId, userId)
    }
    showRemoveMemberModal.value = false
    selectedToRemove.value = []
    await store.fetchConversations()
  } catch (err) {
    console.error('Erreur retrait membre:', err)
  }
}

// --- Helpers --------------------------------------------------------------------
const formatTime = (iso: string): string =>
  new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
</script>