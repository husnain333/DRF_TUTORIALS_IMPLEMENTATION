from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from rest_framework.routers import DefaultRouter
from snippets.views import snippetView

# router = DefaultRouter()
# router.register(r'snippetView', snippetView, basename='snippetView')

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
    path('snippets/count/', views.snippet_count),
    #path('snippetView/', views.snippetView.as_view({'get': 'list'})),
    #path('', include(router.urls)),
    #path('snippetView/<int:pk>/', views.snippetView.as_view({'get': 'retrieve'})),
    #path('SnippetParserView/', views.SnippetParserView.as_view()),
    path('snippetView/', views.snippetView.as_view({'get': 'list', 'post': 'create'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)