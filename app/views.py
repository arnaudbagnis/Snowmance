from pprint import pprint
from random import randrange
from urllib.parse import urlunparse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, request, QueryDict
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME, user_logged_out
from django.contrib.auth.models import User
# Create your views here.
from django.db.models import Q
from django.shortcuts import redirect, render, resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, FormView, ListView
from legacy import urlparse
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


def logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', True):
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    # remember language choice saved to session
    language = request.session.get(LANGUAGE_SESSION_KEY)

    request.session.flush()

    if language is not None:
        request.session[LANGUAGE_SESSION_KEY] = language

    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()


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


class PersonSearchView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Person

    def get_queryset(self):
        print("yee")
        user = User.objects.get(username=self.request.user)
        person = Person.objects.get(user=user)
        user_person = Person.objects.filter(
            Q(hobby_id=person.hobby_id) | Q(way_of_life_id=person.way_of_life_id) | Q(
                personality_id=person.personality_id))[:10]
        print(user_person)
        return user_person


class PersonSearchTagView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Person

    def get_queryset(self):
        tag = self.kwargs.get('pk', '')
        return Person.objects.filter(Q(hobby_id=tag) | Q(way_of_life_id=tag) | Q(personality_id=tag))


class ProfileView(LoginRequiredMixin, FormView):
    model = Question
    template_name = 'profile.html'
    form_class = FormProfile


class LogoutView(SuccessURLAllowedHostsMixin, TemplateView):
    """
    Log out the user and display the 'You are logged out' message.
    """
    next_page = '/login'
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/logged_out.html'
    extra_context = None

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        return self.get(request, *args, **kwargs)

    def get_next_page(self):
        if self.next_page is not None:
            next_page = resolve_url(self.next_page)
        else:
            next_page = self.next_page

        if (self.redirect_field_name in self.request.POST or
                self.redirect_field_name in self.request.GET):
            next_page = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name)
            )
            url_is_safe = is_safe_url(
                url=next_page,
                allowed_hosts=self.get_success_url_allowed_hosts(),
                require_https=self.request.is_secure(),
            )
            # Security check -- Ensure the user-originating redirection URL is
            # safe.
            if not url_is_safe:
                next_page = self.request.path
        return next_page


def logout_then_login(request, login_url=None):
    """
    Log out the user if they are logged in. Then redirect to the login page.
    """
    login_url = resolve_url(login_url or settings.LOGIN_URL)
    return LogoutView.as_view(next_page=login_url)(request)


def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirect the user to the login page, passing the given 'next' page.
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))


