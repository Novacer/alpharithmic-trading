"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include
from .api import hello_world
from .api import algo_results

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get/hello/', hello_world.HelloWorld.as_view()),
    path('api/post/hello', hello_world.PostWorld.as_view()),
    path('api/post/buy-apple', algo_results.BuyAppleResult.as_view()),
    path('api/post/mean-reversion', algo_results.MeanReversionResult.as_view()),
    path('api/post/random-forest-regression', algo_results.RandomForestRegressionResult.as_view()),
    path('api/post/result', algo_results.GetResult.as_view()),
    path('django-rq/', include('django_rq.urls'))
]
