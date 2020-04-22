from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User

# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jimmy', password='top_secret')
    


    

