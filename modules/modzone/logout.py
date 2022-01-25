from django.shortcuts import HttpResponseRedirect


def sign_out(request):
    if request.session.get("mod"):
        request.session.__delitem__("mod")
    return HttpResponseRedirect("/modzone/")
