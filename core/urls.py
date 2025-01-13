from django.contrib import admin
from django.urls import path
from todo import  views
from django.conf import settings
from django.conf.urls.static import static
from todo.views import TodoListView, TodoCreate, TodoConfirm,  TodoDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TodoListView.as_view(),name='base'),
    path('todo/create/', TodoCreate.as_view()),
    path('todo/confirm/', TodoConfirm.as_view()),
    path('todo/delete/', TodoDelete.as_view()),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('custom_logout/',views.custom_logout,name='custom_logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
