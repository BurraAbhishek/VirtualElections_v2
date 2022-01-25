from django.shortcuts import render


def serve(request) -> render:
    return render(
        request,
        "index.html",
    )


def serve_menu(request) -> render:
    return render(
        request,
        "mainmenu.html",
    )
