from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from . import views

# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jimmy', password='top_secret')
    
    def test_loginSuccess(self):
        request = self.factory.get('/accounts/login/')
        request.user = self.user
        response = views.do_login(request)
        self.assertEqual(response.status_code, 200)

    #failed login - password or username problem

    #successful createaccount

    #failed createaccount - username taken or passwords don't match

    #successful character

    #failed character select


    

