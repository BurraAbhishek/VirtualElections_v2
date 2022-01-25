from django.shortcuts import render
from bin.mongoinserts.add_admin_account import add_admin
from bin.mongoinserts.add_election_controls import add_access_controls
from bin.mongoinserts.add_vote_nota import add_nota
from modules.modzone.forms import ModLogin


def start_admin(request) -> render:
    try:
        add_admin()
    except:
        pass
    try:
        add_access_controls()
    except:
        pass
    try:
        add_nota()
    except:
        pass
    return render(
        request,
        "modzone/index.html",
        {
            "login": ModLogin
        }
    )
