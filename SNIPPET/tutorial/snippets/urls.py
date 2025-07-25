from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from rest_framework.routers import DefaultRouter
from snippets.views import SnippetView, ProjectViewSet

urlpatterns = [
   # path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
    path('snippets/count/', views.snippet_count),
    #path('snippetView/', views.snippetView.as_view({'get': 'list'})),
    #path('', include(router.urls)),
    #path('snippetView/<int:pk>/', views.snippetView.as_view({'get': 'retrieve'})),
    #path('SnippetParserView/', views.SnippetParserView.as_view()),
    path('snippets/', views.SnippetView.as_view()),
    path('snippet-create/', views.createSnippet.as_view()),
    path('snippets/<int:id>/', views.SnippetView.as_view()),
    path('projects/', views.ProjectViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

# router = DefaultRouter()
# router.register(r'snippetView', SnippetView, basename='snippet')
# router.register(r'projects', ProjectViewSet, basename='project')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
urlpatterns = format_suffix_patterns(urlpatterns)


