from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.warehouses.urls')),
    path('api/v1/', include('apps.suppliers.urls')),
    path('api/v1/', include('apps.customers.urls')),
    path('api/v1/', include('apps.transport.urls')),
    path('api/v1/', include('apps.products.urls')),
    path('api/v1/', include('apps.drivers.urls')),
    path('api/v1/', include('apps.routes.urls')),
    path('api/v1/', include('apps.tables.urls')),
    path('api/v1/', include('apps.reservations.urls')),
    path('api/v1/', include('apps.shipments.urls')),
    path('api/v1/auth/', include('apps.authentication.urls')),
]
