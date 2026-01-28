from django.db import models


class Requesting(models.Model):
    """A models representation of a <Requesting> instance."""
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_lenght=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of a <Requesting> instance."""
        return f"Request by IP: {self.ip_address}"
