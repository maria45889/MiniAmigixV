from django.urls import path

from .service_types_views import service_types_detail, service_types_list_create
from .vehicle_services_views import vehicle_services_detail, vehicle_services_list_create

urlpatterns = [
    path("service-types/", service_types_list_create, name="service-types-list"),
    path("service-types/<str:id>/", service_types_detail, name="service-types-detail"),
    path("vehicle-services/", vehicle_services_list_create, name="vehicle-services-list"),
    path("vehicle-services/<str:id>/", vehicle_services_detail, name="vehicle-services-detail"),
]
