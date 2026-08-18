"""
URL configuration for project.

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
from mouvement_vol.views import categorieSejourViewset, ExternalolView, MouvementVolCreateView, RecapHierView
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

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('check-statut/', CheckStatutView.as_view(), name='check-statut'),
    
    path('send-email/', SendEmailView.as_view(), name='send-email'),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    
    path('recap-hier/', RecapHierView.as_view(), name='recap-hier'),

    path('export/stock/', export_stock_consommable),
    path('export/vol/', export_vol, name='export-vol'),
    
    path('stock/dernier/', DernierRestantView.as_view(), name='stock-dernier'),
    path('stock/ram/', RamPapierView.as_view(), name='stock-ram'),
    path('stock/conso-mensuelle/', ConsoMensuelleView.as_view(), name='conso-mensuelle'),
    path('stock/alertes-rapport/', AlerteRapportStockView.as_view(), name='stock-alertes'),
    
    path('rapports/recus/', RapportJournalRecuListView.as_view(), name='rapports-recus'),
    path('rapports/recus/<int:pk>/', RapportJournalRecuDetailView.as_view(), name='rapports-recus-detail'),
    path('rapports/recus/<int:pk>/delete/', RapportJournalDeleteView.as_view(), name='rapport-delete'),
    
    path('rapports/', RapportJournalListView.as_view(), name='rapports-list'),
    path('rapports/<int:pk>/', RapportJournalDetailView.as_view(), name='rapports-detail'),

    path('proxy/report-visa/', ExternalolView.as_view(), name='proxy-report-visa'),

    path('mouvements-vol/', MouvementVolCreateView.as_view(), name='mouvements-vol'),

    path('encre/', NiveauEncreListView.as_view(), name='encre-list'),
    path('encre/update/', NiveauEncreUpdateView.as_view(), name='encre-update'),
    path('encre/reserve/', ReserveEncreUpdateView.as_view(), name='encre-reserve'),

    path('historique/', HistoriqueStockView.as_view(), name='historique'),
    path('historique/delete/', HistoriqueDeleteView.as_view(), name='historique-delete'),

    path('text-model/create/', TextModelCreateView.as_view(),name="text-model-create"),
    path('text-model/list/', TextModelListView.as_view(),name="text-model-list"),
    path('text-model/update/<int:pk>/', TextModelUpdateView.as_view()),
    path('text-model/delete/<int:pk>/', TextModelDeleteView.as_view()),

    path('incidents/', IncidentsListCombinesView.as_view(), name='incidents-combines'),
    path('systemes/system-list/', SystemeListView.as_view(), name='systemes-list'),
    path('systemes/create/', SystemeCreateView.as_view(), name='systemes-create'),
    path('systemes/<int:pk>/update/', SystemeUpdateView.as_view(), name='systemes-update'),
    path('systemes/<int:pk>/delete/', SystemeDeleteView.as_view(), name='systemes-delete'),
    
    path('materiels/materiel-list/', MaterielListView.as_view(), name='materiels-list'),
    path('materiels/create/', MaterielCreateView.as_view(), name='materiels-create'),
    path('materiels/<int:pk>/update/', MaterielUpdateView.as_view(), name='materiels-update'),
    path('materiels/<int:pk>/delete/', MaterielDeleteView.as_view(), name='materiels-delete'),

    path('reseaux/reseau-list/', ReseauListView.as_view(), name='reseaux-list'),
    path('reseaux/create/', ReseauCreateView.as_view(), name='reseaux-create'),
    path('reseaux/<int:pk>/update/', ReseauUpdateView.as_view(), name='reseaux-update'),
    path('reseaux/<int:pk>/delete/', ReseauDeleteView.as_view(), name='reseaux-delete'),

    path('incidents-survenus/create/', IncidentSurvenuCreateView.as_view(), name='incidents-survenus-create'),
    path('incidents-survenus/dernier/', DernierIncidentUserView.as_view(), name='dernier-incident-user'),
    path('incidents-survenus/list/', TechlistIncidentSurvenuView.as_view(), name='list-incident-survenu'),
    path('incidents-survenus/serchTechlist/', SearchTechIncidentView.as_view(), name='incidents-survenus-list'),

    path('messaging/conversations/', my_conversations, name='my-conversations'),
    path('messaging/sms/', send_sms, name='send-sms'),
    path('messaging/conversations/shared-admin/', shared_admin_conversation, name='shared-admin'),
    path('messaging/conversations/private/', create_private_conversation, name='create-private'),
    path('messaging/conversations/group/', create_group, name='create-group'),
    path('messaging/conversations/broadcast/', broadcast_message, name='broadcast'),
    path('messaging/conversations/<int:conv_id>/messages/', MessageListCreate.as_view(), name='messages'),
    path('messaging/conversations/<int:conv_id>/members/add/',    add_member,          name='add-member'),
    path('messaging/conversations/<int:conv_id>/members/<int:user_id>/remove/', remove_member, name='remove-member'),
    path('messaging/conversations/<int:conv_id>/delete/',         delete_conversation, name='delete-conversation'),
    path('messaging/conversations/<int:conv_id>/messages/<int:msg_id>/delete/', delete_message, name='delete-message'),

    path('stock-bureau/', StockBureauView.as_view(), name='stock-bureau'),
    path('stock-bureau/alertes/', StockBureauAlerteView.as_view(), name='stock-alertes'),

    path('transfert-stock/en-attente/', TransfertPendingListView.as_view(), name='transfert-pending'),
    path('transfert-stock/<int:transfert_id>/valider/', TransfertValiderView.as_view(), name='transfert-valider'),
    path('transfert-stock/<int:transfert_id>/refuser/', TransfertRefuserView.as_view(), name='transfert-refuser'),

    path('composant-group/alertes/', alertes_materiel),
    path('composant-group/a-verifier/', materiels_a_verifier),
    path('composant-group/<int:ancien_id>/remplacer/', remplacer_materiel),

    path('tech/',TechListView.as_view(), name='tech_list'),

    path('upload/', FileUploadView.as_view(), name='upload'),

    path('', include('myrapport.urls')),
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('delete-file/', FileDeleteView.as_view(), name='delete-file'),
]