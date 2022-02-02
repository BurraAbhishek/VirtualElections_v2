from django.http import FileResponse

# Since STATICFILES_DIRS is static/


def show_robots(request):
    _ = request
    return FileResponse(
        open(
            "static/robots.txt",
            "rb"
        )
    )
