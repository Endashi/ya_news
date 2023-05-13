import pytest
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок новости',
        text='Текст новости',
        date=timezone.now()
    )
    return news


@pytest.fixture
def news_pk(news):
    return news.pk,


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
