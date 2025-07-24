from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet, User, Project
from snippets.serializers import SnippetSerializer, UserSerializer, ProjectSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, HTMLFormRenderer, TemplateHTMLRenderer, StaticHTMLRenderer, BrowsableAPIRenderer
from rest_framework.decorators import renderer_classes
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .renderers import UppercaseRenderer
# @csrf_exempt
# def snippet_list(request):
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many = True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser.parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 201)
#         return JsonResponse(serializer.errors, status = 400)

# @csrf_exempt
# def snippet_detail(request, pk):
    
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)

@api_view(['GET', 'POST'])
def snippet_list(request, format = None):
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
@permission_classes([AllowAny])
def snippet_detail(request, pk,format = None):
    """
    Retrieve, update or delete a code snippet.
    """

    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        permission_classes = [AllowAny]
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


# class SnippetCount(APIView):
#     renderer_classes = [JSONRenderer]
#     def get(self, request, format=None):
#         snippet_count = Snippet.objects.count()
#         content = {'snippet_count': snippet_count}
#         return Response(content)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def snippet_count(request, format=None):
    snippet_count = Snippet.objects.count()
    content = {'snippet_count': snippet_count}
    permission_classes = [AllowAny]
    return Response(content, content_type='application/json', headers={'Indent': '4'})

# class snippet_details(generics.RetrieveAPIView):
#     queryset = Snippet.objects.all()

#     renderer_classes = [TemplateHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return Response({'snippet': self.object}, template_name='snippets/snippet_detail.html')

@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def simple_html_view(request):
    data = '<html><body><h1>Hello, world</h1></body></html>'
    return Response(data)

# class snippetView(viewsets.ReadOnlyModelViewSet):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [AllowAny]

#     renderer_classes = [JSONRenderer,BrowsableAPIRenderer]



class snippetView(viewsets.ReadOnlyModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [AllowAny]
    renderer_classes = [ UppercaseRenderer]

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

from rest_framework.parsers import JSONParser
import io

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('snippets')
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    lookup_field = 'id'


