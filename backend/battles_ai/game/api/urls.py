from django.urls import path, include
from rest_framework.routers import DefaultRouter
from game.api.views import ChatSessionViewSet, MessageViewSet, LeaderboardViewSet
from game.api.util import calc_score

router = DefaultRouter()
router.register(r'sessions', ChatSessionViewSet, basename='session')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path('', include(router.urls)),
    path('calc_score/', calc_score, name='calc_score')
]