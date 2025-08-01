# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import viewsets

# from rest_framework.renderers import JSONRenderer, HTMLFormRenderer, TemplateHTMLRenderer, StaticHTMLRenderer, BrowsableAPIRenderer
# from rest_framework.decorators import renderer_classes
# from rest_framework import generics
# from rest_framework.permissions import AllowAny
# from rest_framework.decorators import permission_classes
# from .renderers import UppercaseRenderer
# from collections import defaultdict
# from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET', 'POST'])
@csrf_exempt
@permission_classes([AllowAny])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
@permission_classes([AllowAny])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     permission_classes = [AllowAny]
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [AllowAny]
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# @csrf_exempt
# def snippet_list(request, format=None):
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     permission_classes = [AllowAny]
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [AllowAny]
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# @api_view(['GET', 'POST'])
# def snippet_list(request, format = None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([AllowAny])
# @renderer_classes([JSONRenderer, BrowsableAPIRenderer])
# def snippet_detail(request, pk,format = None):
#     """
#     Retrieve, update or delete a code snippet.
#     """

#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         permission_classes = [AllowAny]
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class SnippetCount(APIView):
#     renderer_classes = [JSONRenderer]
#     def get(self, request, format=None):
#         snippet_count = Snippet.objects.count()
#         content = {'snippet_count': snippet_count}
#         return Response(content)

# @api_view(['GET'])
# @renderer_classes([JSONRenderer])
# def snippet_count(request, format=None):
#     snippet_count = Snippet.objects.count()
#     content = {'snippet_count': snippet_count}
#     permission_classes = [AllowAny]
#     return Response(content, content_type='application/json', headers={'Indent': '4'})

# class snippet_details(generics.RetrieveAPIView):
#     queryset = Snippet.objects.all()

#     renderer_classes = [TemplateHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return Response({'snippet': self.object}, template_name='snippets/snippet_detail.html')

# @api_view(['GET'])
# @renderer_classes([StaticHTMLRenderer])
# def simple_html_view(request):
#     data = '<html><body><h1>Hello, world</h1></body></html>'
#     return Response(data)

# class snippetView(viewsets.ReadOnlyModelViewSet):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [AllowAny]

#     renderer_classes = [JSONRenderer,BrowsableAPIRenderer]



# class snippetView(viewsets.ReadOnlyModelViewSet):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [AllowAny]
#     renderer_classes = [ UppercaseRenderer]

# RUN IT IN SHELL
# snippet = Snippet.objects.first()
# serializer = SnippetSerializer(snippet)
# serializer.data

# from rest_framework.renderers import JSONRenderer

# json = JSONRenderer().render(serializer.data)
# print(json)

# from rest_framework.parsers import JSONParser
# import io

# data = b'{"title":"Hi","code":"print(\'Hi\')","created":"2025-07-23T12:00:00Z"}'
# stream = io.BytesIO(data)
# parsed_data = JSONParser().parse(stream)

# serializer = SnippetSerializer(data=parsed_data)
# serializer.is_valid()

 # serializer.validated_data
 
# class SnippetParserView(APIView):
#     stream = io.BytesIO(b'{"title":"Hi","code":"print(\'Hi\')","created":"2025-07-23T12:00:00Z"}')
#     data = JSONParser().parse(stream)
#     serializer = SnippetSerializer(data=data)
#     serializer.is_valid()
#     serializer.validated_data
#     print(serializer.validated_data)
#     def post(self, request, *args, **kwargs):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# class ProjectViewSet(viewsets.ModelViewSet):
#     #queryset = Project.objects.prefetch_related('snippets')
#     #queryset = Project.objects.all()
#     projects = Project.objects.all()
#     for project in projects:
#         project.snippets_list = list(Snippet.objects.filter(project=project))
#     queryset = projects
#     serializer_class = ProjectSerializer
#     permission_classes = [AllowAny]
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     lookup_field = 'id'

# class createSnippet(generics.CreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [IsAuthenticated]
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# class ProjectViewSet(viewsets.ModelViewSet):
    
#     queryset = Snippet.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [AllowAny]
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     lookup_field = 'id'

# from rest_framework.permissions import IsAuthenticatedOrReadOnly

# class SnippetView(generics.ListCreateAPIView):
    
#     #queryset = Snippet.objects.all()
#     queryset = Snippet.objects.select_related("project").all()
#     serializer_class = SnippetSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     renderer_classes = [ JSONRenderer, BrowsableAPIRenderer]

# from django.contrib.auth.models import User


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

