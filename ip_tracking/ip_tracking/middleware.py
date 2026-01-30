from django.http import HttpResponseForbidden
from django.core.cache import cache
from django_ip_geolocation.utils import get_geolocation

from .models import RequestLog, BlockIP


class IPLoggingMiddleware:
    """
    Logs request IP, path, timestamp, geolocation
    and blocks blacklisted IPs.
    """
    GEO_CACHE_TIMEOUT = 60 * 60 * 24
    BLOCK_CACHE_TIMEOUT = 60 * 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        if not ip_address:
            return self.get_response(request)

        block_cache_key = f"blocked:{ip_address}"
        is_blocked = cache.get(block_cache_key)

        if is_blocked is None:
            is_blocked = BlockIP.objects.filter(ip_address=ip_address).exists()
            cache.set(block_cache_key, is_blocked, self.BLOCK_CACHE_TIMEOUT)

        if is_blocked:
            return HttpResponseForbidden("Access denied.")

        geo_cache_key = f"geo:{ip_address}"
        geo_data = cache.get(geo_cache_key)

        if geo_data is None:
            geo_info = get_location(request)
            geo_data = {
                "country": geo_info.get("country"),
                "city": geo_info.get("city")
            }
            cache.set(geo_cache_key, geo_data, self.GEO_CACHE_TIMEOUT)

        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
            country=geo_data.get("country"),
            city=geo_data.get("city")
        )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
