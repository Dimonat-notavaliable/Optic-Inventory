# Create your tests here.
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from authorization.views import sign_in
from main.views import focls, hardware_create, users
from unittest.mock import Mock


class SharedTestRights(object):
    """Набор тестов для проверки прав доступа.\n

    Проверяет страницы:\n
    Страница авторизации;\n
    Страница с множеством ВОЛС;\n
    Страница с созданием оборудования;\n
    Страница со списком пользователей;
    """

    def test_login(self):
        """Проверка страницы авторизации"""
        request = self.factory.get("/auth/")
        request.user = self.user
        response = sign_in(request)

        self.assertEqual(response.status_code, self.expected_codes["unauthorized"])

    def test_many_objects(self):
        """Проверка страницы с множеством ВОЛС"""
        request = self.factory.get("/focls/")
        request.user = self.user
        response = focls(request)

        self.assertEqual(response.status_code, self.expected_codes["reader"])

    def test_creation(self):
        """Проверка страницы с созданием оборудования"""
        request = self.factory.get("/hardware/new/")
        request.user = self.user
        response = hardware_create(request)

        self.assertEqual(response.status_code, self.expected_codes["redactor"])

    def test_users(self):
        """Проверка страницы со списком пользователей"""
        request = self.factory.get("/users/")
        request.user = self.user
        response = users(request)

        self.assertEqual(response.status_code, self.expected_codes["admin"])


class TestUnauthorized(TestCase, SharedTestRights):
    """Тестирование прав доступа неавторизованного пользователя.\n

    Ожидаемые результаты для страниц:\n
    Страница авторизации: код ответа 200 OK;\n
    Страница с множеством объектов: код ответа 302 Found (перенаправление);\n
    Страница с созданием объекта: код ответа 302 Found (перенаправление);\n
    Страница со списком пользователей: код ответа 302 Found (перенаправление);
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.expected_codes = {
            "unauthorized": 200,
            "reader": 302,
            "redactor": 302,
            "admin": 302,
        }


class TestReader(TestCase, SharedTestRights):
    """Тестирование прав доступа пользователя-читателя.\n

    Ожидаемые результаты для страниц:\n
    Страница авторизации: код ответа 302 Found (перенаправление);\n
    Страница с множеством объектов: код ответа 200 OK;\n
    Страница с созданием объекта: код ответа 302 Found (перенаправление);\n
    Страница со списком пользователей: код ответа 302 Found (перенаправление);
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Mock(
            last_name="myuserlastname",
            first_name="myusername",
            password="password",
            email="abc@testmail.com",
            is_active=True,
            is_writer=False,
            is_superuser=False,
        )
        self.expected_codes = {
            "unauthorized": 302,
            "reader": 200,
            "redactor": 302,
            "admin": 302,
        }


class TestRedactor(TestCase, SharedTestRights):
    """Тестирование прав доступа пользователя-редактора.\n

    Ожидаемые результаты для страниц:\n
    Страница авторизации: код ответа 302 Found (перенаправление);\n
    Страница с множеством объектов: код ответа 200 OK;\n
    Страница с созданием объекта: код ответа 200 OK;\n
    Страница со списком пользователей: код ответа 302 Found (перенаправление);
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Mock(
            last_name="myuserlastname",
            first_name="myusername",
            password="password",
            email="abc@testmail.com",
            is_active=True,
            is_writer=True,
            is_superuser=False,
        )
        self.expected_codes = {
            "unauthorized": 302,
            "reader": 200,
            "redactor": 200,
            "admin": 302,
        }


class TestAdmin(TestCase, SharedTestRights):
    """Тестирование прав доступа администратора.\n

    Ожидаемые результаты для страниц:\n
    Страница авторизации: код ответа 302 Found (перенаправление);\n
    Страница с множеством объектов: код ответа 200 OK;\n
    Страница с созданием объекта: код ответа 200 OK;\n
    Страница со списком пользователей: код ответа 200 OK;
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Mock(
            last_name="myuserlastname",
            first_name="myusername",
            password="password",
            email="abc@testmail.com",
            is_active=True,
            is_writer=True,
            is_superuser=True,
            id=15,
        )
        self.expected_codes = {
            "unauthorized": 302,
            "reader": 200,
            "redactor": 200,
            "admin": 200,
        }
