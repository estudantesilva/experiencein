from django.urls import path, re_path, include
from perfis import views as auth_views
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('perfis', views.perfilviewSet)

urlpatterns = [
 path('', include(router.urls)),
 path('perfil/', views.get_meu_perfil, nome='perfil'),
 path('convites/', views.get_convites, nome='convites'),
 path('convites/convidar/<int:perfil_id>', views.convidar, name='convidar'),
 path('convites/aceitar/<int:convite_id>', views.aceitar, name='aceitar'),
 path('login/', auth_views.obtain_auth_token, nome='login')
]