from django.test import TestCase


class AccountsRoutingTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_person_page_loads_under_accounts_url(self):
        response = self.client.get('/accounts/add-person/')
        self.assertEqual(response.status_code, 200)
