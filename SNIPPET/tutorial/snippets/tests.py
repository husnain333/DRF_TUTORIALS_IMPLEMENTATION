from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APIRequestFactory, APITestCase, APIClient, force_authenticate

from snippets.models import Snippet
from snippets.views import SnippetList, SnippetDetail
from snippets.serializers import SnippetSerializer

def test_snippet_highlighting_logic():
    snippet = Snippet(
        code='print("Hello, World!")',
        language='python',
        style='friendly',
        linenos=True,
        title="Test Snippet",
        owner=User.objects.create_user(username='dummy')
    )
    snippet.save()
    assert "Hello, World!" in snippet.highlighted
    assert "<div class=" in snippet.highlighted

def test_snippet_list_get_with_request_factory():
    factory = APIRequestFactory()
    user = User.objects.create_user(username='admin', password='123')
    view = SnippetList.as_view()

    request = factory.get('/snippets/')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 200


def test_snippet_detail_patch_with_request_factory():
    user = User.objects.create_user(username='admin', password='123')
    snippet = Snippet.objects.create(code="code1", owner=user)

    factory = APIRequestFactory()
    view = SnippetDetail.as_view()

    request = factory.patch(f'/snippets/{snippet.pk}/', {"title": "Updated title"}, format='json')
    force_authenticate(request, user=user)

    response = view(request, pk=snippet.pk)
    assert response.status_code == 200
    assert response.data['title'] == "Updated title"


def test_api_client_snippet_crud_flow():
    client = APIClient()
    user = User.objects.create_user(username='clientuser', password='123')
    client.force_authenticate(user=user)

    response = client.post('/snippets/', {
        "code": "print(123)",
        "language": "python",
        "style": "friendly",
        "title": "My Snippet"
    }, format='json')
    assert response.status_code == 201
    snippet_id = response.data["id"]

    response = client.get(f'/snippets/{snippet_id}/')
    assert response.status_code == 200
    assert response.data['code'] == "print(123)"

    response = client.delete(f'/snippets/{snippet_id}/')
    assert response.status_code == 204


class SnippetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='apitest', password='123')
        self.client.force_authenticate(user=self.user)

    def test_create_snippet(self):
        url = reverse('snippet-list')
        data = {
            "code": "print('DRF')",
            "language": "python",
            "style": "friendly"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(Snippet.objects.get().owner, self.user)

    def test_list_snippets(self):
        Snippet.objects.create(code="sample", owner=self.user)
        url = reverse('snippet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_snippet_detail(self):
        snippet = Snippet.objects.create(code="xyz", owner=self.user)
        url = reverse('snippet-detail', kwargs={"pk": snippet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['code'], "xyz")


def test_reverse_and_highlight_view(client):
    user = User.objects.create_user(username='urluser', password='123')
    snippet = Snippet.objects.create(code="code", owner=user)
    url = reverse('snippet-highlight', kwargs={"pk": snippet.pk})

    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert "<div" in response.content.decode()
