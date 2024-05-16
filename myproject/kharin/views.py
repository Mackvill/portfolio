from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView , TemplateView
from django.urls import reverse_lazy
from .models import Clients, PhotoSessions, CompletedSessions, CustomUser
from .forms import ClientForm, PhotoSessionForm
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group

class MainView(TemplateView):
    template_name = 'index.html'

class ClientListView(ListView):
    model = Clients
    template_name = 'client_list.html'
    context_object_name = 'clients'

class ClientDetailView(DetailView):
    model = Clients
    template_name = 'client_detail.html'
    context_object_name = 'client'


class ClientSessionCreateView(View):
    def get(self, request):
        client_form = ClientForm()
        photo_session_form = PhotoSessionForm()
        return render(request, 'client_form.html', {'client_form': client_form, 'photo_session_form': photo_session_form})

    def post(self, request):
        client_form = ClientForm(request.POST)
        photo_session_form = PhotoSessionForm(request.POST)
        if client_form.is_valid() and photo_session_form.is_valid():
            name = client_form.cleaned_data['name']
            email = client_form.cleaned_data['email']
            phone = client_form.cleaned_data['phone']
            date = photo_session_form.cleaned_data['date']
            duration = photo_session_form.cleaned_data['duration']
            location = photo_session_form.cleaned_data['location']
            notes = photo_session_form.cleaned_data['notes']


            existing_client = Clients.objects.filter(name=name, email=email, phone=phone).first()
            print("oo")
            if existing_client:

                PhotoSessions.objects.create(
                    client=existing_client,
                    date=date,
                    duration=duration,
                    location=location,
                    notes=notes
                )
                print("ok")

            else:

                PhotoSessions.objects.create(
                    client=Clients.objects.create(name=name, email=email, phone=phone),
                    date=date,
                    duration=duration,
                    location=location,
                    notes=notes
                )
                print("okd")


            return redirect('sessions-by-email')
        else:
            print(client_form.errors)
            print(photo_session_form.errors)
            return render(request, 'client_form.html',
                  {'client_form': client_form, 'photo_session_form': photo_session_form})

class ClientUpdateView(UpdateView):
    model = Clients
    template_name = 'client_form.html'
    fields = '__all__'

class ClientDeleteView(DeleteView):
    model = Clients
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('client-list')


class SessionsByEmailView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'sessions_by_email.html')

    def post(self, request):
        email = request.POST.get('email', None)
        if email:
            client = Clients.objects.filter(email=email).first()
            if client:
                sessions = client.photosessions_set.all()
                return render(request, 'sessions_by_email.html', {'client': client, 'sessions': sessions})
        return render(request, 'sessions_by_email.html', {'error': 'No sessions found for this email.'})


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Assuming 'role' is a field in your CustomUser model
            if user.role == 'admin':
                return redirect('all-sessions')  # Example admin dashboard URL name
            elif user.role == 'manager':
                return redirect('all-sessions')  # Example student dashboard URL name

        else:
            error_message = "Invalid username or password."
            return render(request, self.template_name, {'error_message': error_message})




class EditSessionView(View):
    def get(self, request, session_id):
        session = get_object_or_404(PhotoSessions, pk=session_id)
        return render(request, 'edit_session.html', {'session': session})

    def post(self, request, session_id):
        session = get_object_or_404(PhotoSessions, pk=session_id)
        session.date = request.POST['date']
        session.duration = request.POST['duration']
        session.location = request.POST['location']
        session.notes = request.POST.get('notes', '')
        session.save()
        return redirect('sessions-by-email')

class DeleteSessionView(View):
    def get(self, request, session_id):
        session = get_object_or_404(PhotoSessions, pk=session_id)
        return render(request, 'delete_session.html', {'session': session})

    def post(self, request, session_id):
        session = get_object_or_404(PhotoSessions, pk=session_id)
        session.delete()
        return redirect('all-sessions')


class AllSessionsView(View):
    def get(self, request):

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        sessions = PhotoSessions.objects.all()
        if start_date and end_date:
            sessions = sessions.filter(date__range=[start_date, end_date])

        sessions = sessions.order_by('date')

        return render(request, 'all_sessions.html', {'sessions': sessions})

class CancelSessionView(View):
    def post(self, request, session_id):
        session = PhotoSessions.objects.get(pk=session_id)
        session.delete()
        return redirect('all-sessions')

class ConfirmCompletionView(View):
    @method_decorator(user_passes_test(lambda u: u.role == 'Administrator'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, session_id):
        session = PhotoSessions.objects.get(pk=session_id)
        completion = CompletedSessions(session=session, photographer_name=request.user.username, completed_date=date.today())
        completion.save()
        return redirect('all-sessions')

class CompletedSessionsView(View):
    def get(self, request):
        completed_sessions = CompletedSessions.objects.all()
        return render(request, 'completed_sessions.html', {'completed_sessions': completed_sessions})