# Create your tests here.
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from authorization.views import sign_in
from main.views import focls, hardware_create, users
from unittest.mock import Mock


class SharedTestRights(object):
    """Набор тестов для проверки прав доступа"""

    def test_login(self):
        """Проверка страницы авторизации"""
        request = self.factory.get(self.pages['unauthorized'])
        request.user = self.user
        response = sign_in(request)

        self.assertEqual(response.status_code, self.expected_codes['unauthorized'])

    def test_many_objects(self):
        """Проверка страницы с множеством объектов"""
        request = self.factory.get(self.pages['reader'])
        request.user = self.user
        response = focls(request)

        self.assertEqual(response.status_code, self.expected_codes['reader'])

    def test_creation(self):
        """Проверка страницы с созданием объекта"""
        request = self.factory.get(self.pages['redactor'])
        request.user = self.user
        response = hardware_create(request)

        self.assertEqual(response.status_code, self.expected_codes['redactor'])

    def test_users(self):
        """Проверка страницы со списком пользователей"""
        request = self.factory.get(self.pages['admin'])
        request.user = self.user
        response = users(request)

        self.assertEqual(response.status_code, self.expected_codes['admin'])


class TestUnauthorized(TestCase, SharedTestRights):
    """Тестирование прав доступа неавторизованного пользователя.

    Ожидаемые результаты для страниц:
    Страница авторизации: код ответа 200 OK;
    Страница с множеством объектов: код ответа 302 Found (перенаправление);
    Страница с созданием объекта: код ответа 302 Found (перенаправление);
    Страница со списком пользователей: код ответа 302 Found (перенаправление);
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.pages = {'unauthorized': "/auth/",
                      'reader': "/focls/",
                      'redactor': "/hardware/new/",
                      'admin': "/users/"}
        self.expected_codes = {'unauthorized': 200,
                               'reader': 302,
                               'redactor': 302,
                               'admin': 302}


class TestReader(TestCase, SharedTestRights):
    """Тестирование прав доступа пользователя-читателя.

    Ожидаемые результаты для страниц:
    Страница авторизации: код ответа 302 Found (перенаправление);
    Страница с множеством объектов: код ответа 200 OK;
    Страница с созданием объекта: код ответа 302 Found (перенаправление);
    Страница со списком пользователей: код ответа 302 Found (перенаправление);
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Mock(last_name="myuserlastname", first_name="myusername", password="password",
                         email="abc@testmail.com", is_active=True, is_writer=False, is_superuser=False)
        self.pages = {'unauthorized': "/auth/",
                      'reader': "/focls/",
                      'redactor': "/hardware/new/",
                      'admin': "/users/"}
        self.expected_codes = {'unauthorized': 302,
                               'reader': 200,
                               'redactor': 302,
                               'admin': 302}


class TestRedactor(TestCase, SharedTestRights):
    """Тестирование прав доступа пользователя-редактора.

    Ожидаемые результаты для страниц:
    Страница авторизации: код ответа 302 Found (перенаправление);
    Страница с множеством объектов: код ответа 200 OK;
    Страница с созданием объекта: код ответа 200 OK;
    Страница со списком пользователей: код ответа 302 Found (перенаправление);
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Mock(last_name="myuserlastname", first_name="myusername", password="password",
                         email="abc@testmail.com", is_active=True, is_writer=True, is_superuser=False)
        self.pages = {'unauthorized': "/auth/",
                      'reader': "/focls/",
                      'redactor': "/hardware/new/",
                      'admin': "/users/"}
        self.expected_codes = {'unauthorized': 302,
                               'reader': 200,
                               'redactor': 200,
                               'admin': 302}


class TestAdmin(TestCase, SharedTestRights):
    """Тестирование прав доступа администратора.

    Ожидаемые результаты для страниц:
    Страница авторизации: код ответа 302 Found (перенаправление);
    Страница с множеством объектов: код ответа 200 OK;
    Страница с созданием объекта: код ответа 200 OK;
    Страница со списком пользователей: код ответа 200 OK;
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Mock(last_name="myuserlastname", first_name="myusername", password="password",
                         email="abc@testmail.com", is_active=True, is_writer=True, is_superuser=True)
        self.pages = {'unauthorized': "/auth/",
                      'reader': "/focls/",
                      'redactor': "/hardware/new/",
                      'admin': "/users/"}
        self.expected_codes = {'unauthorized': 302,
                               'reader': 200,
                               'redactor': 200,
                               'admin': 200}
