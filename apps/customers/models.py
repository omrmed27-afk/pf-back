from django.db import models


class Customer(models.Model):
    COMPANY = 'company'
    INDIVIDUAL = 'individual'
    CUSTOMER_TYPE_CHOICES = [
        (COMPANY, 'Empresa'),
        (INDIVIDUAL, 'Persona'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES, default=INDIVIDUAL)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
