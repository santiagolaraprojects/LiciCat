from django.urls import path, include
from api.views import *
from . import views
from publicdata.views import get_data

urlpatterns = [
    path('licitacions', LicitacionsList.as_view()),
    path('licitacions/public', LicitacionsPubliquesList.as_view()),
    path('licitacions/private', LicitacionsPrivadesList.as_view()),
    path('licitacions/private/my_licitacions', LicitacionsPrivadesUser.as_view()),
    path('licitacions/private/my_licitacions/aplicants', LicitacionsPrivadesUserAplicants.as_view()),
    path('licitacions/private/my_licitacions/aplicants/accept', AcceptAplicant.as_view()),
    path('licitacions/private/my_licitacions/aplicants/decline', DeclineAplicant.as_view()),
    path('licitacions/favorites', LicitacionsFavoritesList.as_view()),
    path('licitacions/following', LicitacionsSeguidesList.as_view()),
    path('licitacions/preferences', LicitacionsPreferencesList.as_view()),
    path('licitacions/aplied', LicitacionsApliedList.as_view()),
    path('licitacions/<int:pk>/', LicitacioDetailView.as_view()),
    path('licitacions/<int:pk>/save', Add_to_favorites.as_view()),
    path('licitacions/<int:pk>/follow', Seguir.as_view()),
    path('licitacions/<int:pk>/aply', Aply.as_view()),
    path('licitacions/<int:pk>/estadistiques', Estadistiques.as_view()),
    path('localitzacions', LocalitzacionsInfo.as_view()),
    path('ambits', AmbitsInfo.as_view()),
    path('departaments', DepartamentsInfo.as_view()),
    path('organs', OrgansInfo.as_view()),
    path('tipus_contracte', TipusContracteInfo.as_view()),
    
    path('users/following/licitacions', LicitacionsFollowingList.as_view()),
    path('updateBD/', get_data, name='update_BD'),
  
    path('cron/', CronTests.as_view()),
    path('candidatura/<int:pk>', VisualitzarCandidatura.as_view()),
  
    # Users URLs
    path("users/", include("users.urls")),
    #path('preferences', Add_to_preferences.as_view()),
]
