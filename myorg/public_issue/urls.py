
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, IssueViewSet, RatingViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'ratings', RatingViewSet)


urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('signin/', views.signin_view, name='signin'),
    path('reportissue/', views.reportissue_view, name='reportissue'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('profile/', views.profile_view, name='profile'), 
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('rating/<str:issue_id>/', views.give_rating, name='give_rating'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_status/<str:issue_id>/', views.update_status, name='update_status'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
