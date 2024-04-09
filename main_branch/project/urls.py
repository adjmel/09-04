# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# # Créer une instance de DefaultRouter
# router = DefaultRouter()

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls')),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/', include(router.urls))  # Inclure les URL générées par le router
# ]


from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
# Créer une instance de DefaultRouter pour gérer les ViewSets
#router = DefaultRouter()
from django.contrib.auth.models import User
# Enregistrer vos ViewSets avec le router (remplacez `UserViewSet` par le nom de votre ViewSet)
 # router.register(r'users', UserViewSet)

# class OTPAdmin(OTPAdminSite):
#     pass

# admin_site = OTPAdmin(name='OTPAdmin')
# admin_site.register(User)
# admin_site.register(TOTPDevice, TOTPDeviceAdmin)

# Définir les URL patterns
urlpatterns = [
    # URL pour l'administration Django
    path('admin/', admin.site.urls),

    # URL pour l'authentification de l'API (facultatif)
    path('api-auth/', include('rest_framework.urls')),

    # URL pour obtenir un token JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # URL pour rafraîchir un token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inclure les URL générées par le router pour les ViewSets
    # Assurez-vous d'avoir enregistré vos ViewSets avec le router
    #path('api/', include(router.urls)),
    path('', include('myapp.urls')),
]
