from django.db import models
from apps.core.models import TimeStampedModel

class UserProfile(TimeStampedModel):
    """
    Representa um usuário do sistema, vinculado ao número de telefone (WAHA ID).
    Armazena credenciais da UTFPR (criptografadas idealmente, aqui simplificado para MVP).
    """
    phone_number = models.CharField(max_length=50, unique=True, help_text="ID do usuário no WhatsApp (ex: 554199999999@c.us)")
    ra = models.CharField(max_length=20, blank=True, null=True, help_text="Registro Acadêmico")
    utfpr_password = models.CharField(max_length=255, blank=True, null=True, help_text="Senha do Portal (Cuidado: Armazenamento sensível)")
    is_authenticated_utfpr = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} ({self.ra if self.ra else 'Sem RA'})"
