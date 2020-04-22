import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

class HomePageView(TemplateView):
    template_name = 'payment/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

# Create your views here.
@login_required(login_url="/login")
def charge(request):
    context = {}
    if request.method == 'POST':
        filterCharge = list(filter(lambda value: value.description==str(request.user), stripe.Charge.list()))
        if not filterCharge: 
            charge = stripe.Charge.create(
                amount=500,
                currency='usd',
                description= str(request.user),
                source=request.POST['stripeToken']
            )
            context['check'] = True
    return render(request, 'payment/charge.html')

def account(request):
    return HttpResponseRedirect('/accounts/characters')