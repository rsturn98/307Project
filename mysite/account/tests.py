from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from . import views

# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jimmy', password='top_secret')
    
    def loginFail(self):
        

    def loginSuccess(self):
        request = self.factory.get('/accounts/login/')
        request.user = self.user
        response = views.do_login(request)
        self.assertEqual(response.status_code, 200)


    

