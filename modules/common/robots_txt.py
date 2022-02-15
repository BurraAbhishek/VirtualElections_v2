from django.http import FileResponse, HttpResponseRedirect

# Since STATICFILES_DIRS is static/


def show_robots(request) -> FileResponse:
    _ = request
    return FileResponse(
        open(
            "static/robots.txt",
            "rb"
        )
    )


def route_to_correct_robots(request) -> HttpResponseRedirect:
    _ = request
    return HttpResponseRedirect("/robots.txt")
