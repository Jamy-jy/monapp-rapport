<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle"/>
    <ComponentCard title="Stock">
        <!-- Barre recherche + filtre + bouton ajout -->
        <div class="flex items-center gap-3 mb-4">
    
          <!-- Recherche -->
          <div class="relative flex-1">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
              </svg>
            </span>
            <input
              v-model="search"
              type="text"
              placeholder="Recherche..."
              class="w-full pl-9 pr-4 h-10 text-sm border border-gray-300 rounded-lg bg-transparent dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 focus:border-brand-300 focus:outline-none focus:ring-2 focus:ring-brand-500/10"
            />
          </div>
        </div>
    
        <BaseTable
            v-if="StockBureauList.length > 0"
            :columns="columns"
            :rows="StockBureauList"
        />
        <p
          v-else-if="noResult"
          class="text-center text-gray-500 py-4"
        >
          Aucun résultat trouvé
        </p>
    </ComponentCard>
</template>
<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue'
    import ComponentCard from '@/components/common/ComponentCard.vue';
    import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
    import BaseTable from '@/components/table/BaseTable.vue';
    import axios from 'axios';
    import API_CONFIG from '@/config/api';

    const currentPageTitle = ref('Stock')
    // Recherche
    const search = ref('')

    const stockBureau = ref([])

    const columns = [
        { label: 'consommable', field: 'consommable', width: '30%' },
        { label: 'entrée', field: 'qte_entree_bureau', width: '30%' },
        { label: 'envoyé', field: 'qte_envoye_bureau', width: '30%' },
        { label: 'restant', field: 'qte_restant_bureau', width: '30%' },
        { label: 'nom site', field: 'nom_site', width: '30%' },
        { label: 'date', field: 'date_mouvement_bureau', width: '30%' },
        { label: 'acteur', field: 'nom_complet', width: '30%' },
    ]

    // Récupération des données
    const fetchStockBureau = async () => {
      try {
        const url = `${API_CONFIG.LOCAL.BASE_URL}/stock-bureau/list/`
        console.log('URL appelée :', url)
        const res = await axios.get(url)
        stockBureau.value = res.data
      } catch (error) {
        console.error('Erreur lors du chargement du stock bureau :', error)
      }
    }

    onMounted(() => {
      fetchStockBureau()
    })

    // Formatage de la date pour affichage et recherche
    const formatDate = (dateStr: any) => {
      if (!dateStr) return ''
      const d = new Date(dateStr)
      return d.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        //hour: '2-digit',
        //minute: '2-digit',
      })
    }

    // Transformation des lignes pour correspondre aux colonnes (affichage)
    const formattedRows = computed(() =>
      stockBureau.value.map((item: any) => ({
        id: item.id,
        consommable: item.consommable_nom ?? '',
        qte_entree_bureau: item.qte_entree_bureau,
        qte_envoye_bureau: item.qte_envoye_bureau,
        qte_restant_bureau: item.qte_restant_bureau,
        nom_site: item.nom_site ?? '',
        date_mouvement_bureau: formatDate(item.date_mouvement_bureau),
        nom_complet: item.user_nom_complet ?? '',
      }))
    )

    // Filtrage / recherche sur toutes les colonnes concernées
    const StockBureauList = computed(() => {
      const term = search.value.trim().toLowerCase()
      if (!term) return formattedRows.value

      return formattedRows.value.filter((row) => {
        return (
          row.consommable.toLowerCase().includes(term) ||
          row.nom_complet.toLowerCase().includes(term) ||
          row.date_mouvement_bureau.toLowerCase().includes(term)
        )
      })
    })

    // Aucun résultat trouvé
  const noResult = computed(
    () => search.value.trim() !== '' && StockBureauList.value.length === 0
  )
</script>