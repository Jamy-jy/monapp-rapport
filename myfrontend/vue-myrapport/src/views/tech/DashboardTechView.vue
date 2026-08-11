<template>
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
        <h3 class="text-xl font-semibold text-gray-800 dark:text-white/90" x-text="pageTitle">
            technicien en service hier : 
            <span v-if="techInfo">
                {{ techInfo.prenom }} {{ techInfo.email }}
            </span>
            <span v-else class="text-gray-400 font-normal text-base">
                Aucun rapport hier
            </span>
        </h3>
    </div>
    <div class="grid grid-cols-12 gap-4 md:gap-6">
        <div class="col-span-12 space-y-6 xl:col-span-7">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:gap-6">
                <CardTech
                    titre="Etiquette"
                    :qte_entree="qte_entree_bob"
                    :qte_sortie="qte_sortie_bob"
                    :qte_restant="qte_restant_bob"
                />
                <CardTech
                    titre="Ruban"
                    :qte_entree="qte_entree_r"
                    :qte_sortie="qte_sortie_r"
                    :qte_restant="qte_restant_r"
                />
            </div>
           <LastRecapVol @tech="techInfo = $event"/>
        </div>
        <div class="col-span-12 xl:col-span-5">
            <ConsoPapier
              :nbr_entree_ram="nbr_entree_ram"
              :nbr_sortie_ram="nbr_sortie_ram"
              :nbr_restant_ram="nbr_restant_ram"
              />
        </div>
    </div>

    <div class="col-span-12 my-6">
        <ConsoImprimante 
            :products="encreProducts"
            :boxops="encreBoxops"
        />
    </div>
    
</template>
<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import CardTech from '@/components/dashboard/CardTech.vue';
    import ConsoImprimante from '@/components/dashboard/ConsoImprimante.vue';
    import ConsoPapier from '@/components/dashboard/ConsoPapier.vue';
    import LastRecapVol from '@/components/dashboard/LastRecapVol.vue';
    import axios from 'axios'
    import { useAlertNotifStore } from '@/stores/AlertNotif';

    const encreProducts = ref<any[]>([])
    const encreBoxops = ref<any[]>([])

    const nbr_entree_ram = ref(0)
    const nbr_restant_ram = ref(0)
    const nbr_sortie_ram = ref(0)

    const qte_entree_bob = ref(0)
    const qte_sortie_bob = ref(0)
    const qte_restant_bob = ref(0)

    const qte_entree_r = ref(0)
    const qte_sortie_r = ref(0)
    const qte_restant_r = ref(0)


    const alert = useAlertNotifStore()

    interface TechInfo {
        prenom: string
        nom: string
        email: string
    }

    const techInfo = ref<TechInfo | null>(null)

    const fetchEncre = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/encre/')

            // Construire la structure attendue par le composant
            encreBoxops.value = res.data.boxops

            encreProducts.value = res.data.data.map((row: any) => ({
            couleur: row.couleur,
            nbr_bouteil: row.reserve,
            status: row.status,
            // niveaux : { boxop_id: '75%' }
            niveaux: Object.fromEntries(
                Object.entries(row.niveaux).map(([boxId, info]: [string, any]) => [
                Number(boxId),
                info.niveau + '%'
                ])
            )
            }))

        } catch (err) {
            console.error('Erreur chargement encre:', err)
        }
    }

    const fetchConsoRam = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/stock/dernier/', {
            params: { nom: 'ram papier' }
            })
            nbr_entree_ram.value = res.data.qte_entree
            nbr_restant_ram.value = res.data.qte_restant
            nbr_sortie_ram.value = res.data.qte_sortie
        } catch (err) {
            console.error(err)
            alert.showAlertNotif(
                "Erreur lors de l'affichage",
                "error"
            )
        }
    }

    const fetchConsoBobine = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/stock/dernier/', {
            params: { nom: 'etiquette' }  // insensible à la casse côté backend
            })
            qte_entree_bob.value = res.data.qte_entree
            qte_sortie_bob.value = res.data.qte_sortie
            qte_restant_bob.value = res.data.qte_restant
        } catch (err) {
            console.error(err)
        }
    }

    const fetchConsoRuban = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/stock/dernier/', {
            params: { nom: 'ruban' }
            })
            qte_entree_r.value = res.data.qte_entree
            qte_sortie_r.value = res.data.qte_sortie
            qte_restant_r.value = res.data.qte_restant
        } catch (err) {
            console.error(err)
            alert.showAlertNotif(
                    "Erreur lors de l'affichage",
                    "error"
                )
        }
    }

    onMounted(() => {
        fetchEncre()
        fetchConsoRam()
        fetchConsoBobine()
        fetchConsoRuban()
        })

</script>