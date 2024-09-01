from django.urls import path
from app1 import views
from app1.Apii import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'studentViewsets', api.StudentViewsets, basename='studentViewsets')
router1.register(r'studentModelViewSet', api.studentModelViewSet, basename='studentModelViewSet')

urlpatterns = [
    path('students/',views.students),
    path('students/<int:pk>',views.students),

    # apiviews decorator
    path('student_views/',api.students),
    path('student_views/<int:pk>',api.students),

    # apiviews
    path('StudentAPIView/',api.StudentAPIView.as_view()),
    path('StudentAPIView/<int:pk>',api.StudentAPIView.as_view()),
    
    # generics views
    path('StudentGenericsView/',api.StudentGenericsView.as_view()),
    path('StudentGenericsView/<int:pk>',api.StudentGenericsDetailView.as_view()),
    path('StudentGenericsfilter/',api.StudentGenericsfilter.as_view()),
    # http://127.0.0.1:8000/api/StudentGenericsfilter/?name=pankaj


    # mixins
    path('StudentMixins/',api.StudentMixins.as_view()),
    path('StudentMixins/<int:pk>',api.StudentMixinDetail.as_view()),
]

urlpatterns = router.urls
urlpatterns = router1.urls