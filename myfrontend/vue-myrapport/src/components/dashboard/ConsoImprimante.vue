<template>
  <div class="overflow-hidden rounded-2xl border border-gray-200 bg-white px-4 pb-3 pt-4 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6">
    <div class="flex flex-col gap-2 mb-4 sm:flex-row sm:items-center sm:justify-between">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-white/90">
        Consommation imprimante
      </h3>
    </div>

    <div class="max-w-full overflow-x-auto custom-scrollbar">
      <table class="min-w-full">
        <thead>
          <tr class="border-t border-gray-100 dark:border-gray-800">
            <th class="py-3 text-left">
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">Couleur</p>
            </th>

            <!-- Colonnes boxop dynamiques -->
            <th
              v-for="box in boxops"
              :key="box.id"
              class="py-3 text-left"
            >
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">
                {{ box.numero }}
              </p>
            </th>

            <th class="py-3 text-left">
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">Nombre de Bouteilles</p>
            </th>
            <th class="py-3 text-left">
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">Statut</p>
            </th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="(product, index) in products"
            :key="index"
            class="border-t border-gray-100 dark:border-gray-800"
          >
            <!-- Couleur -->
            <td class="py-3 whitespace-nowrap">
              <div class="flex items-center gap-2">
                <span
                  class="w-3 h-3 rounded-full shrink-0"
                  :style="{ backgroundColor: couleurHex(product.couleur) }"
                ></span>
                <p class="font-medium text-gray-800 text-theme-sm dark:text-white/90">
                  {{ product.couleur }}
                </p>
              </div>
            </td>

            <!-- Niveau par boxop -->
            <td v-for="box in boxops" :key="box.id" class="py-3 whitespace-nowrap">
              <!-- Éditable — select -->
              <select
                v-if="editable && localProducts[index]"
                v-model="localProducts[index].niveaux[box.id]"
                class="text-sm border border-gray-300 rounded-lg px-2 py-1 dark:border-gray-700 dark:bg-gray-900 dark:text-white outline-none focus:border-brand-400"
              >
                <option v-for="n in niveaux" :key="n.value" :value="n.value">{{ n.label }}</option>
              </select>
              

              <!-- ReadOnly — texte -->
              <p v-else class="text-gray-500 text-theme-sm dark:text-gray-400">
                {{ product.niveaux?.[box.id] ?? '—' }}
              </p>
            </td>

            <!-- Réserve -->
            <td class="py-3 whitespace-nowrap">

              <!--  Éditable — input number -->
              <input
                v-if="editable && localProducts[index]"
                v-model.number="localProducts[index].nbr_bouteil"
                type="number"
                min="0"
                class="w-16 px-2 py-1 text-sm border border-gray-300 rounded-lg dark:border-gray-700 dark:bg-gray-900 dark:text-white text-center focus:border-brand-400 outline-none"
              />

              <!-- ReadOnly — texte -->
              <p v-else class="text-gray-500 text-theme-sm dark:text-gray-400">
                {{ product.nbr_bouteil }}
              </p>

            </td>

            <!-- Statut -->
            <td class="py-3 whitespace-nowrap">
              <span
                class="rounded-full px-2 py-0.5 text-theme-xs font-medium"
                :class="statusClass(product.status)"
              >
                {{ product.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface BoxOp {
  id: number
  numero: string
}

interface Product {
  couleur: string
  couleur_id: number
  niveaux: Record<number, string>  // { boxop_id: '100%' }
  nbr_bouteil: number | string
  status: string
}

const props = defineProps<{
  products: Product[]
  boxops: BoxOp[]
  editable?: boolean  // false par défaut = readonly
}>()

const emit = defineEmits<{
  (e: 'update:products', value: Product[]): void
}>()

// Copie locale pour l'édition — ne modifie pas le parent directement
const localProducts = ref<Product[]>(JSON.parse(JSON.stringify(props.products)))

// Sync si le parent met à jour les données
watch(() => props.products, (val) => {
  localProducts.value = JSON.parse(JSON.stringify(val))
}, { deep: true })

watch(localProducts, (val) => {
  emit('update:products', val)
}, { deep: true })

const niveaux = [
  { label: '100%', value: '100%' },
  { label: '95%',  value: '95%'  },
  { label: '90%',  value: '90%'  },
  { label: '85%',  value: '85%'  },
  { label: '80%',  value: '80%'  },
  { label: '75%',  value: '75%'  },
  { label: '70%',  value: '70%'  },
  { label: '65%',  value: '65%'  },
  { label: '60%',  value: '60%'  },
  { label: '55%',  value: '55%'  },
  { label: '50%',  value: '50%'  },
  { label: '45%',  value: '45%'  },
  { label: '40%',  value: '40%'  },
  { label: '35%',  value: '35%'  },
  { label: '25%',  value: '25%'  },
  { label: 'Vide', value: '0%'   },
]

const statusClass = (status: string): string => {
  if (status === 'Disponible')     return 'bg-green-50 text-green-600 dark:bg-green-500/15 dark:text-green-500'
  if (status === 'presque épuisé') return 'bg-orange-50 text-orange-600 dark:bg-orange-500/15 dark:text-orange-400'
  return 'bg-red-50 text-red-600 dark:bg-red-500/15 dark:text-red-500'
}

const couleurHex = (nom: string): string => {
  const map: Record<string, string> = {
    'Noir': '#1a1a1a', 'Noire': '#1a1a1a',
    'Bleu': '#3b82f6', 'Blue': '#3b82f6',
    'Rouge': '#ef4444',
    'Jaune': '#eab308',
  }
  return map[nom] || '#6b7280'
}
</script>