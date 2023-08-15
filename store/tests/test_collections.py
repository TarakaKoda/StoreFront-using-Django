from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from store.models import Collection
import pytest

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.fixture
def authenticated(api_client):
    def do_authenticated(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticated

@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self, create_collection):
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self,create_collection, authenticated):
        authenticated()

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, api_client, create_collection, authenticated):
        authenticated(is_staff=True)

        response = create_collection({'title':''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, api_client, create_collection, authenticated):
        authenticated(is_staff=True)

        response = create_collection({'title':'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exits_returns_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.pk}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data =={
            'id': collection.pk,
            'title': collection.title,
            'products_count': 0
        }

    def test_if_collection_not_exits_return_204(self, api_client):
        response = api_client.get('/store/collections/100/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateCollection:
    def test_if_collection_updated_method_is_not_allowed_405(self, api_client, authenticated):
        authenticated(is_staff=True)
        collection = baker.make(Collection)

        updated_data = {
            'title': 'new title'
        }
        response = api_client.put(f'/store/collections/{collection.id}/',data=updated_data)
        assert response.status_code == status.HTTP_200_OK
        collection.refresh_from_db()
        assert collection.title == updated_data['title']

