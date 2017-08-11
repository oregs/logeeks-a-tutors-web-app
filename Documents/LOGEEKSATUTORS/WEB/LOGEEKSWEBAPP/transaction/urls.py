from django.conf.urls import url, include

from transaction import views


app_name = 'transaction'
urlpatterns = [
    url(r'^initializing/$', views.initialize_transaction, name='initialize_transaction'),
    url(r'^confirm/$', views.confirm_transaction, name='confirm_transation')
]
