from django.core.urlresolvers import reverse

from django_webtest import WebTest


class HomeTest(WebTest):
    def test_home(self):
        url = reverse('home')
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notes')
