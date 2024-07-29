from django.db import models
from auth_app.models import User

class UpdatedDate(models.Model):
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE, related_name='updated_dates')
    updated_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        if self.updated_date:
            return f"{self.updated_date.strftime('%Y-%m-%d %H:%M:%S')} - {self.domain.domain_name} - {self.domain.user.email}"
        return 'No Updated Date'
    
class CreationDate(models.Model):
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE, related_name='creation_dates')
    creation_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        if self.creation_date:
            return f"{self.creation_date.strftime('%Y-%m-%d %H:%M:%S')} - {self.domain.domain_name} - {self.domain.user.email}"
        return 'No Creation Date'

class ExpirationDate(models.Model):
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE, related_name='expiration_dates')
    expiration_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.expiration_date:
            return f"{self.expiration_date.strftime('%Y-%m-%d %H:%M:%S')} - {self.domain.domain_name} - {self.domain.user.email}"
        return 'No Expiration Date'
    
class Email(models.Model):
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE, related_name='emails')
    emails = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.emails} - {self.domain.domain_name}"

class Domain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain_name = models.CharField(max_length=255)
    registrar = models.CharField(max_length=255, blank=True, null=True)
    whois_server = models.CharField(max_length=255, blank=True, null=True)
    referral_url = models.URLField(blank=True, null=True)
    name_servers = models.JSONField(blank=True, null=True)
    status = models.JSONField(blank=True, null=True)
    dnssec = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    org = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    registrant_postal_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.domain_name
