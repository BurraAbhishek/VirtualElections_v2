from django.shortcuts import render


def serve_docs(request) -> render:
    return render(
        request,
        "site_navigation/documentation.html",
    )


def open_sourcepage(request) -> render:
    return render(
        request,
        "docs/source.html",
    )


def show_changelog(request) -> render:
    return render(
        request,
        "docs/changelog.html",
    )


def privacy_policy(request) -> render:
    return render(
        request,
        "docs/privacy.html",
    )


def show_tos(request) -> render:
    return render(
        request,
        "docs/tos.html",
    )


def show_faq(request) -> render:
    return render(
        request,
        "docs/faq.html",
    )


def redirect_oldhomepage(request) -> render:
    return render(
        request,
        "docs/oldhomepage.html",
    )
