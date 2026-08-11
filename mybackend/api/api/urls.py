"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from login.views import LoginView, LogoutView, CheckStatutView
from users.views import UserViewSet, TechListView
from consommables.views import consommableViewset, DernierRestantView, RamPapierView, ConsoMensuelleView, NotificationView
from emails_destinataire.views import emails_destinataireViewset
from stock_consommables.views import boxPafViewSet, boxOpViewSet, stockViewSet, vignetteViewSet, bobineViewSet, imprimanteViewSet, NiveauEncreListView, ReserveEncreUpdateView, NiveauEncreUpdateView, HistoriqueStockView, HistoriqueDeleteView, StockBureauView, StockBureauAlerteView, TransfertPendingListView, TransfertValiderView, TransfertRefuserView
from stock_consommables.export import export_stock_consommable, export_vol
from myrapport.views import FileUploadView, FileDeleteView, SendEmailView, RapportJournalListView, RapportJournalDetailView, RapportJournalRecuListView, RapportJournalRecuDetailView, RapportJournalDeleteView, TextModelCreateView, TextModelListView, TextModelUpdateView, TextModelDeleteView, AlerteRapportStockView
from mouvement_vol.views import categorieSejourViewset, ExternalAPIVolView, MouvementVolCreateView, RecapHierView
from incidents.views import SystemeListView, SystemeCreateView, SystemeUpdateView, SystemeDeleteView, MaterielListView, MaterielCreateView, MaterielUpdateView, MaterielDeleteView, ReseauListView, ReseauCreateView, ReseauUpdateView , ReseauDeleteView, IncidentsListCombinesView, IncidentSurvenuCreateView, DernierIncidentUserView, TechlistIncidentSurvenuView, SearchTechIncidentView
from messaging.views import my_conversations, send_sms, shared_admin_conversation, create_private_conversation, create_group, broadcast_message, MessageListCreate, add_member, remove_member, delete_conversation, delete_message
from inventaire.views import GroupInventaireViewset, ComposantGroupViewSet,  alertes_materiel, materiels_a_verifier, remplacer_materiel, SiteViewset
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'consommables', consommableViewset)
router.register(r'emails_destinataire', emails_destinataireViewset)
router.register(r'boxpaf', boxPafViewSet)
router.register(r'boxop', boxOpViewSet)
router.register(r'stock', stockViewSet)
router.register(r'vignettes', vignetteViewSet)
router.register(r'bobines', bobineViewSet)
router.register(r'imprimante', imprimanteViewSet)
router.register(r'sejour_visa', categorieSejourViewset)
router.register(r'inventaire', GroupInventaireViewset)
router.register(r'group-inventaire', GroupInventaireViewset, basename='group-inventaire')
router.register(r'composant-group', ComposantGroupViewSet, basename='composant-group')
router.register(r'site', SiteViewset, basename='site')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    
    path('api/check-statut/', CheckStatutView.as_view(), name='check-statut'),
    
    path('api/send-email/', SendEmailView.as_view(), name='send-email'),
    path('api/notifications/', NotificationView.as_view(), name='notifications'),
    
    path('api/recap-hier/', RecapHierView.as_view(), name='recap-hier'),

    path('api/export/stock/', export_stock_consommable),
    path('api/export/vol/', export_vol, name='export-vol'),
    
    path('api/stock/dernier/', DernierRestantView.as_view(), name='stock-dernier'),
    path('api/stock/ram/', RamPapierView.as_view(), name='stock-ram'),
    path('api/stock/conso-mensuelle/', ConsoMensuelleView.as_view(), name='conso-mensuelle'),
    path('api/stock/alertes-rapport/', AlerteRapportStockView.as_view(), name='stock-alertes'),
    
    path('api/rapports/recus/', RapportJournalRecuListView.as_view(), name='rapports-recus'),
    path('api/rapports/recus/<int:pk>/', RapportJournalRecuDetailView.as_view(), name='rapports-recus-detail'),
    path('api/rapports/recus/<int:pk>/delete/', RapportJournalDeleteView.as_view(), name='rapport-delete'),
    
    path('api/rapports/', RapportJournalListView.as_view(), name='rapports-list'),
    path('api/rapports/<int:pk>/', RapportJournalDetailView.as_view(), name='rapports-detail'),

    path('api/proxy/report-visa/', ExternalAPIVolView.as_view(), name='proxy-report-visa'),

    path('api/mouvements-vol/', MouvementVolCreateView.as_view(), name='mouvements-vol'),

    path('api/encre/', NiveauEncreListView.as_view(), name='encre-list'),
    path('api/encre/update/', NiveauEncreUpdateView.as_view(), name='encre-update'),
    path('api/encre/reserve/', ReserveEncreUpdateView.as_view(), name='encre-reserve'),

    path('api/historique/', HistoriqueStockView.as_view(), name='historique'),
    path('api/historique/delete/', HistoriqueDeleteView.as_view(), name='historique-delete'),

    path('api/text-model/create/', TextModelCreateView.as_view(),name="text-model-create"),
    path('api/text-model/list/', TextModelListView.as_view(),name="text-model-list"),
    path('api/text-model/update/<int:pk>/', TextModelUpdateView.as_view()),
    path('api/text-model/delete/<int:pk>/', TextModelDeleteView.as_view()),

    path('api/incidents/', IncidentsListCombinesView.as_view(), name='incidents-combines'),
    path('api/systemes/system-list/', SystemeListView.as_view(), name='systemes-list'),
    path('api/systemes/create/', SystemeCreateView.as_view(), name='systemes-create'),
    path('api/systemes/<int:pk>/update/', SystemeUpdateView.as_view(), name='systemes-update'),
    path('api/systemes/<int:pk>/delete/', SystemeDeleteView.as_view(), name='systemes-delete'),
    
    path('api/materiels/materiel-list/', MaterielListView.as_view(), name='materiels-list'),
    path('api/materiels/create/', MaterielCreateView.as_view(), name='materiels-create'),
    path('api/materiels/<int:pk>/update/', MaterielUpdateView.as_view(), name='materiels-update'),
    path('api/materiels/<int:pk>/delete/', MaterielDeleteView.as_view(), name='materiels-delete'),

    path('api/reseaux/reseau-list/', ReseauListView.as_view(), name='reseaux-list'),
    path('api/reseaux/create/', ReseauCreateView.as_view(), name='reseaux-create'),
    path('api/reseaux/<int:pk>/update/', ReseauUpdateView.as_view(), name='reseaux-update'),
    path('api/reseaux/<int:pk>/delete/', ReseauDeleteView.as_view(), name='reseaux-delete'),

    path('api/incidents-survenus/create/', IncidentSurvenuCreateView.as_view(), name='incidents-survenus-create'),
    path('api/incidents-survenus/dernier/', DernierIncidentUserView.as_view(), name='dernier-incident-user'),
    path('api/incidents-survenus/list/', TechlistIncidentSurvenuView.as_view(), name='list-incident-survenu'),
    path('api/incidents-survenus/serchTechlist/', SearchTechIncidentView.as_view(), name='incidents-survenus-list'),

    path('api/messaging/conversations/', my_conversations, name='my-conversations'),
    path('api/messaging/sms/', send_sms, name='send-sms'),
    path('api/messaging/conversations/shared-admin/', shared_admin_conversation, name='shared-admin'),
    path('api/messaging/conversations/private/', create_private_conversation, name='create-private'),
    path('api/messaging/conversations/group/', create_group, name='create-group'),
    path('api/messaging/conversations/broadcast/', broadcast_message, name='broadcast'),
    path('api/messaging/conversations/<int:conv_id>/messages/', MessageListCreate.as_view(), name='messages'),
    path('api/messaging/conversations/<int:conv_id>/members/add/',    add_member,          name='add-member'),
    path('api/messaging/conversations/<int:conv_id>/members/<int:user_id>/remove/', remove_member, name='remove-member'),
    path('api/messaging/conversations/<int:conv_id>/delete/',         delete_conversation, name='delete-conversation'),
    path('api/messaging/conversations/<int:conv_id>/messages/<int:msg_id>/delete/', delete_message, name='delete-message'),

    path('api/stock-bureau/', StockBureauView.as_view(), name='stock-bureau'),
    path('api/stock-bureau/alertes/', StockBureauAlerteView.as_view(), name='stock-alertes'),

    path('api/transfert-stock/en-attente/', TransfertPendingListView.as_view(), name='transfert-pending'),
    path('api/transfert-stock/<int:transfert_id>/valider/', TransfertValiderView.as_view(), name='transfert-valider'),
    path('api/transfert-stock/<int:transfert_id>/refuser/', TransfertRefuserView.as_view(), name='transfert-refuser'),

    path('api/composant-group/alertes/', alertes_materiel),
    path('api/composant-group/a-verifier/', materiels_a_verifier),
    path('api/composant-group/<int:ancien_id>/remplacer/', remplacer_materiel),

    path('api/tech/',TechListView.as_view(), name='tech_list'),

    path('upload/', FileUploadView.as_view(), name='upload'),

    path('api/', include('myrapport.urls')),
    path('api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('delete-file/', FileDeleteView.as_view(), name='delete-file'),
]