// src/stores/messaging.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

// --- Types -----------------------------------------------------

export type ConvType = 'shared_admin' | 'private' | 'group'

export interface Member {
  user_id:  number
  username: string
  role:     'admin' | 'tech'
}

export interface LastMessage {
  id:          number
  content:     string
  sent_at:     string
  sender_name: string
  sender_role: 'admin' | 'tech'
}

export interface Conversation {
  id:           number
  name:         string
  type:         ConvType
  created_at:   string
  members:      Member[]
  last_message: LastMessage | null
}

export interface Message {
  id:          number
  content:     string
  sent_at:     string
  sender_id:   number
  sender_name: string
  sender_role: 'admin' | 'tech'
}

export interface SmsResultat {
  results: { tech: string; phone: string; status: string }[]
  errors: { tech: string; error: string }[]
  total_envoye: number
  total_erreur: number
}

export interface BroadcastResult {
  conversation_id: number
  tech:            string
  message_id:      number
  sent_at:         string
}
// --- ajout token ---------------------------------------------------------
function authHeaders() {
  const token = sessionStorage.getItem('token')
  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  }
}
// --- Store ---------------------------------------------------------------

export const useMessagingStore = defineStore('messaging', () => {
  const conversations = ref<Conversation[]>([])
  const activeConvId  = ref<number | null>(null)
  const messages      = ref<Message[]>([])
  const loading       = ref(false)
  const error         = ref<string | null>(null)

  const activeConv = computed<Conversation | undefined>(
    () => conversations.value.find(c => c.id === activeConvId.value)
  )

  // --- Conversations -----------------------------------------------------

  async function fetchConversations(): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      const { data } = await axios.get<Conversation[]>(`http://localhost:8000/api/messaging/conversations/`,
        authHeaders()
      )
      conversations.value = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Erreur de chargement'
      conversations.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchSharedAdmin(): Promise<void> {
    try {
      const { data } = await axios.get<Conversation>(`http://localhost:8000/api/messaging/conversations/shared-admin/`,
        authHeaders()
      )
      // Ajoute ou met à jour dans la liste
      const idx = conversations.value.findIndex(c => c.id === data.id)
      if (idx === -1) conversations.value.unshift(data)
      else conversations.value[idx] = data
      activeConvId.value = data.id
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Erreur'
    }
  }

  // --- Messages ---------------------------------------------------------

  async function fetchMessages(convId: number): Promise<void> {
    activeConvId.value = convId
    try {
      const { data } = await axios.get<Message[]>(
        `http://localhost:8000/api/messaging/conversations/${convId}/messages/`,
        authHeaders()
      )
      messages.value = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Erreur'
    }
  }

  async function sendMessage(convId: number, content: string): Promise<void> {
    try {
      const { data } = await axios.post<Message>(
        `http://localhost:8000/api/messaging/conversations/${convId}/messages/`,
        { content },
        authHeaders()
      )
      messages.value.push(data)
      // Met à jour le last_message dans la liste
      const conv = conversations.value.find(c => c.id === convId)
      if (conv) conv.last_message = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Erreur envoi'
    }
  }

  // --- Actions admin ------------------------------------------------------------
  async function createPrivateConv(techIds: number[]): Promise<Conversation[]> {
    const token = sessionStorage.getItem('token')
    const { data } = await axios.post<Conversation[]>(
      `http://localhost:8000/api/messaging/conversations/private/`,
      { tech_ids: techIds },
      authHeaders()
    )
    await fetchConversations()
    return data
  }

  async function createGroup(name: string, techIds: number[]): Promise<Conversation> {
    const { data } = await axios.post<Conversation>(
      `http://localhost:8000/api/messaging/conversations/group/`,
      { name, tech_ids: techIds },
      authHeaders()
    )
    await fetchConversations()
    return data
  }

  async function broadcastMessage(
    techIds: number[],
    content: string
  ): Promise<BroadcastResult[]> {
    const { data } = await axios.post<BroadcastResult[]>(
      `http://localhost:8000/api/messaging/conversations/broadcast/`,
      { tech_ids: techIds, content },
      authHeaders()
    )
    await fetchConversations()
    return data
  }

  function clearMessages(): void {
    messages.value    = []
    activeConvId.value = null
  }

  // --- send sms ---------------------------------------------------------
  async function sendSms(
    techIds: number[],
    content: string
  ): Promise<SmsResultat> {
    const { data } = await axios.post(
      'http://localhost:8000/api/messaging/sms/',
      { tech_ids: techIds, content },
      authHeaders()
    )
    return data
  }

  async function addMember(convId: number, userId: number): Promise<void> {
    await axios.post(
      `http://localhost:8000/api/messaging/conversations/${convId}/members/add/`,
      { user_id: userId },
      authHeaders()
    )
    await fetchConversations()
  }

  async function removeMember(convId: number, userId: number): Promise<void> {
    await axios.delete(
      `http://localhost:8000/api/messaging/conversations/${convId}/members/${userId}/remove/`,
      authHeaders()
    )
    await fetchConversations()
  }

  async function deleteConversation(convId: number): Promise<void> {
    await axios.delete(
      `http://localhost:8000/api/messaging/conversations/${convId}/delete/`,
      authHeaders()
    )
    conversations.value = conversations.value.filter(c => c.id !== convId)
    if (activeConvId.value === convId) {
      activeConvId.value = null
      messages.value = []
    }
  }

  async function deleteMessage(convId: number, msgId: number): Promise<void> {
    await axios.delete(
      `http://localhost:8000/api/messaging/conversations/${convId}/messages/${msgId}/delete/`,
      authHeaders()
    )
    messages.value = messages.value.filter(m => m.id !== msgId)
  }

  return {
    // State
    conversations, activeConvId, messages, loading, error,
    // Getters
    activeConv,
    // Actions
    fetchConversations, fetchSharedAdmin,
    fetchMessages, sendMessage, clearMessages,
    createPrivateConv, createGroup, broadcastMessage,
    sendSms, addMember, removeMember, deleteConversation, deleteMessage,
  }
})