from pprint import pprint
from random import randrange
from django.http import HttpResponseRedirect, request
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# Create your views here.
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, ListView
from werkzeug.debug import console

from Snowmance import settings
from app.froms.profile import FormProfile
from app.froms.register import FormRegister
from app.models.person import Person
from app.models.question import Question


def signup(self):
    if self.method == 'POST':
        form = FormRegister(self.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password_1')
            user = authenticate(username=username, password=raw_password)
            login(self, user)
            return redirect('home')
    else:
        form = FormRegister()
    return render(self, 'register.html', {'form': form})


class IndexView(TemplateView):
    template_name = 'index.html'
    model = Person


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            print("hello")
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        print(username)
        return render(request, self.template_name)


class RegisterView(FormView):
    model = Question
    template_name = 'register.html'
    form_class = FormRegister

    def form_valid(self, form):
        avatar = form.cleaned_data.get('avatar');
        birth = form.cleaned_data.get('birth')
        last_name = form.clean_last_name()
        first_name = form.clean_first_name()
        personality = form.cleaned_data.get('personality')
        hobby = form.cleaned_data.get('hobby')
        way_of_life = form.cleaned_data.get('way_of_life')
        username = form.clean_last_name() + str(randrange(0, 101, 2))
        username.replace(" ", "")
        email = form.cleaned_data.get('email')
        password_1 = form.cleaned_data.get('password_1')
        password_2 = form.cleaned_data.get('password_2')
        user = User.objects.create_user(username=username, email=email,
                                        password=password_1, first_name=first_name, last_name=last_name)
        Person.objects.create(user=user, birth=birth, personality=personality, way_of_life=way_of_life, hobby=hobby,
                              avatar=avatar)
        print("OK")
        console.log("OK")
        return HttpResponseRedirect(settings.LOGIN_URL)


class PersonSearchView(ListView):
    template_name = 'index.html'
    model = Person

    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        person = Person.objects.get(user=user)
        user_person = Person.objects.filter(Q(hobby_id=person.hobby_id) | Q(way_of_life_id=person.way_of_life_id) | Q(
            personality_id=person.personality_id))[:10]
        print(user_person)
        return user_person


class PersonSearchTagView(ListView):
    template_name = 'index.html'
    model = Person

    def get_queryset(self):
        tag = self.kwargs.get('pk', '')
        return Person.objects.filter(Q(hobby_id=tag) | Q(way_of_life_id=tag) | Q(personality_id=tag))

class ProfileView(FormView):
    model = Question
    template_name = 'profile.html'
    form_class = FormProfile
