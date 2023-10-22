
"""| URLS |"""

# Django.
from django.contrib import admin
from django.urls import path, include
# Rest-fremework.
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
# views.
from games.views import (
    GameViewSet,
    ActiveGameViewSet,
    SearchProductsInPriceRange,
    FindPieceOfTextViewSet,
    ByDescendingViewSet
)
from auths.views import (
    UserViewSet
)


router = DefaultRouter()
#* Games routers.
router.register(r'game', GameViewSet, basename='game')
router.register(r'active_game', ActiveGameViewSet, basename='active')
router.register(r'search/range', SearchProductsInPriceRange, basename='range')
router.register(r'search/piece', FindPieceOfTextViewSet, basename='piece')
router.register(r'search/descending', ByDescendingViewSet, basename='descending')

router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls), name='game'),
]
#! JWT.
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
