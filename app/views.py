from random import randrange

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, ListView
from werkzeug.debug import console

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
        return super().form_valid(form)

class PersonSearchDetailView(ListView):
    template_name = 'index.html'
    model = Person

    def get_queryset(self):
        title = self.kwargs.get('slug', '')
        return Person.objects.filter(title__contains=title)
