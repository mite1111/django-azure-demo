"""ticketadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from registrationapi.views import RegisterAPI
from registrationapi.views import LoginAPI
from registrationapi.views import ViewProfileAPI, EditProfile
from ticketapi.views import PostTicketAPI
from ticketapi.views import GetMyTicketsAPI, GetTicketById, GetTicketByHashtag, EditTicketAPI
from commentsapi.views import PostCommentAPI, GetCommentsByUserId, GetCommentsByTicketId
from interestsapi.views import PostInterestAPI, GetInterestsByUserid, GetInterestsByTicketId

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #profile apis
    path('api/registrationapi/', RegisterAPI.as_view(), name='registration'),
    path('api/loginapi/', LoginAPI.as_view(), name='login'),
    path('api/viewprofileapi/', ViewProfileAPI.as_view()),
    path('api/editprofileapi/', EditProfile.as_view()),
    #ticket apis
    path('api/postticketapi/', PostTicketAPI.as_view()),
    path('api/getmyticketsapi/', GetMyTicketsAPI.as_view()),
    path('api/getticketbyidapi/', GetTicketById.as_view()),
    path('api/getticketbyhashtagapi/', GetTicketByHashtag.as_view()),
    path('api/editticketapi/', EditTicketAPI.as_view()),
    #comments apis
    path('api/postcommentapi/', PostCommentAPI.as_view()),
    path('api/getcommentsbyuseridapi/', GetCommentsByUserId.as_view()),
    path('api/getcommentsbyticketidapi/', GetCommentsByTicketId.as_view()),
    #interests apis
    path('api/postinterestapi/', PostInterestAPI.as_view()),
    path('api/getinterestsbyuseridapi/', GetInterestsByUserid.as_view()),
    path('api/getinterestsbyticketidapi/', GetInterestsByTicketId.as_view())
    
]
