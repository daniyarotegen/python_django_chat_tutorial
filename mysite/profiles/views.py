from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .forms import ProfileForm, CustomUserCreationForm

User = get_user_model()


class SignUpView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'profiles/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'profiles/login.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class ProfileListView(LoginRequiredMixin, View):
    def get(self, request):
        q = request.GET.get('q', '')
        profiles = User.objects.exclude(id=request.user.id)
        if q:
            profiles = profiles.filter(Q(username__icontains=q))
        return render(request, 'profiles/profile_list.html', {'profiles': profiles})


class OtherProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        profile = User.objects.get(username=username)
        if request.user.username == username:
            return redirect('profile')
        return render(request, 'profiles/other_profile.html', {'profile': profile})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = User.objects.get(username=request.user.username)
        return render(request, 'profiles/profile.html', {'profile': profile})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'profiles/edit_profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)
        return render(request, 'profiles/edit_profile.html', {'form': form})
