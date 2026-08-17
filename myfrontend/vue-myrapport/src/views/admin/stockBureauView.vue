<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle"/>
    <ComponentCard title="Stock">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-5">
            <SelectInput
              label="consommable"
              placeholder="choisissez le consommable"
              :options="stockBureauOptions"
              v-model="formData.consommable"
            />
            <PlaceholderInput
              v-model="stockBureau.qte_entree_bureau"
              type="number"
              label="Entrée :"
              placeholder="0"
            />
            <PlaceholderInput
              v-model="stockBureau.qte_restant_bureau"
              type="number"
              label="Reste :"
              placeholder="0"
              :readonly="true"
            />
            <PlaceholderInput
              v-model="stockBureau.qte_envoye"
              type="number"
              label="envoyé :"
              placeholder="0"
            />
            <SelectInput
              label="vers :"
              placeholder="Choisissez un site"
              :options="siteOptions"
              v-model="stockBureau.site"
            />
        </div>
        
        <div class="flex mt-4 justify-end">
            <ValideBtn @click="submitStock" :loading="loadingStock"/>
        </div>
    </ComponentCard>
</template>
<script setup lang="ts">
    import { ref, reactive, onMounted, watch } from 'vue';
    import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
    import ComponentCard from '@/components/common/ComponentCard.vue';
    import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
    import ValideBtn from '@/components/buttons/ValideBtn.vue';
    import SelectInput from '@/components/FormElement/SelectInput.vue';
    import axios from 'axios';
    import { useAlertNotifStore } from '@/stores/AlertNotif';
    import API_CONFIG from '@/config/api';

    const currentPageTitle = ref('Mouvement de stock');

    interface Option{
    label: string
    value: string | number
    raw: any
    }

    const stockBureauOptions = ref<Option[]>([])

    const fetchConsommable = async () => {
        try {
            const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/consommables/`)

            stockBureauOptions.value = res.data.map((c: any) => ({
            label: c.nom_consommable,  // ce que tu veux afficher
            value: c.id,               // ce que tu envoies au backend
            raw : c 
            }))

        } catch (err) {
            console.error(err)
        }

    }
    onMounted(() => {
        fetchConsommable()
    })


    const stockBureau = reactive({
        qte_entree_bureau: 0,
        qte_envoye: 0,
        qte_restant_bureau: 0,
        site: '',
    })

    const formData = reactive({
        consommable: '',
    })

    const siteOptions = [
        { label: "DIE", value: "DIE" },
        { label: "FTU", value: "FTU" },
        { label: "MJU", value: "MJU" },
        { label: "NOS", value: "NOS" },
        { label: "TNR", value: "TNR" },
        { label: "TMM", value: "TMM" },
        { label: "TLE", value: "TLE" },
        { label: "SMS", value: "SMS" },
    ];

    const loadingStock = ref(false)

    const errorMsg   = ref('')
    const successMsg = ref('')
    const alert = useAlertNotifStore()

    watch(() => formData.consommable, async (newId) => {
        if (!newId) return

        errorMsg.value = ''
        successMsg.value = ''

        // Reset champs
        stockBureau.qte_entree_bureau = 0
        stockBureau.qte_envoye = 0
        stockBureau.site = ''

        try {
            const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/stock-bureau/`, {
            params: { consommable_id: newId }
            })
            stockBureau.qte_restant_bureau = res.data.qte_restant_bureau
        } catch (err) {
            stockBureau.qte_restant_bureau = 0
        }
    })

    const submitStock = async () => {
        errorMsg.value = ''
        successMsg.value = ''
        loadingStock.value = true

        // Validation frontend
        if (!formData.consommable) {
            alert.showAlertNotif(
                "une erreur s'est produit",
                "error"
            )
            errorMsg.value = 'Veuillez choisir un consommable.'
            loadingStock.value = false
            return
        }

        if (stockBureau.qte_entree_bureau === 0 && stockBureau.qte_envoye === 0) {
            alert.showAlertNotif(
                "erreur de champs non renseigner",
                "error"
            )
            errorMsg.value = 'Saisir soit au moins une entrée ou un envoi.'
            loadingStock.value = false
            return
        }

        // Si un envoi est présent, le site est obligatoire
        if (stockBureau.qte_envoye > 0 && !stockBureau.site) {
            alert.showAlertNotif(
                "site non renseigné",
                "error"
            )
            errorMsg.value = 'Veuillez indiquer le site de destination.'
            loadingStock.value = false
            return
        }

        try {
            const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/stock-bureau/`, {
            consommable_id: formData.consommable,
            qte_entree_bureau: stockBureau.qte_entree_bureau,
            qte_envoye:        stockBureau.qte_envoye,
            qte_restant_bureau: stockBureau.qte_restant_bureau,
            site: stockBureau.site,
            })

            successMsg.value = res.data.message
            alert.showAlertNotif(
                "Enregistrement effectué avec succès",
                "success"
            )
            stockBureau.qte_restant_bureau = res.data.qte_restant_bureau
            stockBureau.qte_entree_bureau  = 0
            stockBureau.qte_envoye         = 0
            stockBureau.site               = ''

        } catch (err) {
            if (axios.isAxiosError(err) && err.response?.data?.error) {
                alert.showAlertNotif(
                "Une erreur s'est produite lors de l'enregistrement",
                "error"
                )
                errorMsg.value = err.response.data.error
            } else {
                alert.showAlertNotif(
                "Une erreur s'est produite lors de l'enregistrement",
                "error"
                )
                errorMsg.value = 'Erreur lors de l\'enregistrement.'
            }
        } finally {
            loadingStock.value = false
        }
    }

    const fetchAlertesStock = async () => {
        try {
            const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/stock-bureau/alertes/`)

            res.data.forEach((item: any) => {
                alert.showAlertNotif(
                    `"${item.nom_consommable}" est presque épuisé, il reste ${item.qte_restant_bureau}`,
                    "warning",
                    10000 // durée d'affichage en ms
                )
            })
        } catch (err) {
            console.error(err)
        }
    }

    onMounted(() => {
        fetchConsommable()
        fetchAlertesStock()
    })
</script>