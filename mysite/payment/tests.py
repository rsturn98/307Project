from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from . import views

# Create your tests here.
class PaymentTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jimmy', password='top_secret')
    
    def test_payment(self):
        request = self.factory.get('/pay/')
        #...
    
    def test_charge(self):
        request = self.factory.get('/pay/charge')
        #...
