
"""| URLS |"""

# Django.
from django.contrib import admin
from django.urls import path, include
# Rest-fremework.
from rest_framework.routers import DefaultRouter
# views.
from games.views import (
    GameViewSet, 
    ActiveGameViewSet,
    SearchProductsInPriceRange
)


router = DefaultRouter()
router.register(r'game', GameViewSet, basename='game')
router.register(r'active_game', ActiveGameViewSet, basename='active')
router.register(r'searchproducts', SearchProductsInPriceRange, basename='serach')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls), name='game'),
]