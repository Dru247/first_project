from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


User = get_user_model()


class GeneralAppTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Batman')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_urls_not_exists_at_desired_locations(self):
        """Urls not exists anonymous users"""
        urls_subtests = (
            ('/', 'Страница / не доступна анонимному пользователю'),
            ('/clients/', 'Страница /clients/ не доступна анонимному пользователю'),
            ('/deletesim/', 'Страница /deletesim/ не доступна анонимному пользователю'),
            ('/maks-func/', 'Страница /maks-func/ не доступна анонимному пользователю'),
        )
        for url, subtest_description in urls_subtests:
            with self.subTest(subtest_description):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

    def test_urls_exists_at_desired_locations_authorized(self):
        """Urls exists authorizers users"""
        urls_subtests = (
            ('/', 'Страница / доступна авторизированному пользователю'),
            ('/clients/', 'Страница /clients/ доступна авторизированному пользователю'),
            ('/deletesim/', 'Страница /deletesim/ доступна авторизированному пользователю'),
            ('/maks-func/', 'Страница /maks-func/ доступна авторизированному пользователю'),
        )
        for url, subtest_description in urls_subtests:
            with self.subTest(subtest_description):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)
