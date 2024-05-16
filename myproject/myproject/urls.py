"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from kharin.views import ClientListView, ClientDetailView, ClientSessionCreateView, ClientUpdateView,\
    ClientDeleteView, MainView, SessionsByEmailView , EditSessionView , DeleteSessionView, AllSessionsView,\
    CancelSessionView, ConfirmCompletionView, CompletedSessionsView, LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='index'),
    path('client-list/', ClientListView.as_view(), name='client-list'),
    path('sessions_by_email/', SessionsByEmailView.as_view(), name='sessions-by-email'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('edit_session/<int:session_id>/', EditSessionView.as_view(), name='edit-session'),
    path('delete_session/<int:session_id>/', DeleteSessionView.as_view(), name='delete-session'),
    path('all_sessions/', AllSessionsView.as_view(), name='all-sessions'),
    path('cancel_session/<int:session_id>/', CancelSessionView.as_view(), name='cancel-session'),
    path('confirm_completion/<int:session_id>/', ConfirmCompletionView.as_view(), name='confirm-completion'),
    path('completed_sessions/', CompletedSessionsView.as_view(), name='completed-sessions'),
    path('client/create/', ClientSessionCreateView.as_view(), name='client-create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
]







