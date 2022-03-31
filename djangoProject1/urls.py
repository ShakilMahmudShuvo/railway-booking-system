"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
import booking.views as booking_views
import login.views
import login.views as login_views
import dashboard.views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', booking_views.load),
    path('login', login_views.load),
    path('', booking_views.load),
    path('logout', login_views.logout),
    path('dashboard', dashboard_views.load),
    path('register', login.views.register),
    path('search', booking_views.search),
    path('booking_details', booking_views.booking_details),
    path('booking_proceed', booking_views.booking_proceed),
    path('ticket_order_placed', booking_views.ticketOrderPlaced),
    path('approve_<int:trx_id>', booking_views.approve_order),
    path('refund_<int:trx_id>',booking_views.refund),
    path('approve_refund_<int:bkash>',booking_views.approve_refund_req),

]
