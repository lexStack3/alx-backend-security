from django.db import models


class RequestLog(models.Model):
    """Model representation of a <RequestLog> instance."""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)

    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        """String representation of a <RequestLog> instance."""
        return f"IP: {self.ip_address}"


class BlockIP(models.Model):
    """Model representation of a <BlockIP> instance."""
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of a <BlockIP> instance"""
        return f"Bocked IP: {self.ip_address}"
