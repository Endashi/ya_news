import pytest
from django.shortcuts import reverse
from pytest_django.asserts import assertRedirects, assertFormError
from news.models import Comment
from news.forms import BAD_WORDS, WARNING
from http import HTTPStatus


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.pk,))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    comments_count = Comment.objects.filter(news=news).count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, news_pk, form_data, author):
    url = reverse('news:detail', args=news_pk)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.pk == news_pk[0]
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_user_cant_use_bad_words(author_client, news_pk, form_data):
    url = reverse('news:detail', args=news_pk)
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(
        url,
        data=bad_words_data
    )
    assertFormError(response, 'form', 'text', WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, comment):
    delete_url = reverse('news:delete', args=(comment.pk,))
    response = author_client.delete(delete_url)
    assertRedirects(response, f'/news/{comment.pk}/#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(reader_client, comment):
    delete_url = reverse('news:delete', args=(comment.pk,))
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(author_client, comment):
    edit_url = reverse('news:edit', args=(comment.pk,))
    form_data = {'text': 'Обновленный комментарий'}
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, f'/news/{comment.pk}/#comments')
    comment.refresh_from_db()
    assert comment.text == 'Обновленный комментарий'


def test_user_cant_edit_comment_of_another_user(reader_client, comment):
    edit_url = reverse('news:edit', args=(comment.pk,))
    form_data = {'text': 'Обновленный комментарий'}
    response = reader_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'
