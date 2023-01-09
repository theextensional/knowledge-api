from django.urls import path

from pages.views import (
    AboutProjectView,
    LoginView,
    LogoutView,
    MapInfoResourcesView,
    MapMaterialResourcesView,
    ServiceServerView,
)

urlpatterns = [
    path('map_info_resources', MapInfoResourcesView.as_view(), name='map_info_resources'),
    path('map_material_resources', MapMaterialResourcesView.as_view(), name='map_material_resources'),
    path('service_server', ServiceServerView.as_view(), name='service_server'),
    path('login/', LoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(), name='custom_logout'),
    path('', AboutProjectView.as_view(), name='about_project'),
]
