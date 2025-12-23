class SecurityHeadersMiddleware:
    """
    Middleware to remove or modify headers that leak server information.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Remove or clear server-related headers
        if 'Server' in response:
            del response['Server']
        if 'X-Powered-By' in response:
            del response['X-Powered-By']
        # Optionally add security headers if not already present
        if 'X-Content-Type-Options' not in response:
            response['X-Content-Type-Options'] = 'nosniff'
        if 'X-Frame-Options' not in response:
            response['X-Frame-Options'] = 'DENY'
        return response
