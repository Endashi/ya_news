import pytest
from django.shortcuts import reverse
from django.conf import settings


@pytest.mark.django_db
def test_news_count(client, news_data):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_data):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    first_news_date = object_list[0].date
    all_dates = [news.date for news in object_list]
    assert first_news_date == max(all_dates)


@pytest.mark.django_db
def test_comments_order(client, news_with_comments, detail_url):
    response = client.get(detail_url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_url, news):
    response = client.get(detail_url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(client, detail_url, news, author):
    client.force_login(author)
    response = client.get(detail_url)
    assert 'form' in response.context
