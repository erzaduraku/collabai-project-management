from django.urls import path

from .views import (
    AIConfigView,
    AIRequestHistoryView,
    RAGQueryView,
    RAGReindexView,
    SemanticSearchView,
    TextAnalyzeView,
)
from .views.chatbot import ChatBotView

urlpatterns = [
    path('chatbot/', ChatBotView.as_view(), name='ai-chatbot'),
    path('analyze/', TextAnalyzeView.as_view(), name='ai-text-analyze'),
    path('search/', SemanticSearchView.as_view(), name='ai-semantic-search'),
    path('query/', RAGQueryView.as_view(), name='ai-rag-query'),
    path('reindex/', RAGReindexView.as_view(), name='ai-rag-reindex'),
    path('history/', AIRequestHistoryView.as_view(), name='ai-request-history'),
    path('config/', AIConfigView.as_view(), name='ai-config'),
]
