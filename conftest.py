import pytest
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from news.models import Comment, News
from django.shortcuts import reverse
from django.test import Client


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
def reader_client(django_user_model, client):
    reader = django_user_model.objects.create(username='Читатель')
    reader_client = Client()
    reader_client.force_login(reader)
    return reader_client


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


@pytest.fixture()
def news_data():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_with_comments(news, author):
    now = timezone.now()

    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Текст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()

    return news


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }
