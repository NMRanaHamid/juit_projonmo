class BlockAdminFromFrontendMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Just warn in console, but don't logout
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            if not request.path.startswith('/admin/'):
                print("⚠️ Warning: Admin user accessing frontend")

        response = self.get_response(request)
        return response
