"""virtualelections_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from modules.modzone import adder, startmod, accesscontrols
from modules.modzone import logout, ban, regulation, mod_doc
from modules.common import customize, index, documentation, robots_txt
from modules.voter import voter_views
from modules.election import election_view, cast
from modules.party import party_views, show_profile
from modules.results import result_view

urlpatterns = [
    # Django default admin page - unused
    path('admin/', admin.site.urls),
    # Index pages
    path('', index.serve),
    path('menu/', index.serve_menu),
    # Documentation
    path('docs/', documentation.serve_docs),
    path('source/', documentation.open_sourcepage),
    path('changelog/', documentation.show_changelog),
    path('privacy/', documentation.privacy_policy),
    path('terms-of-service/', documentation.show_tos),
    path('faq/', documentation.show_faq),
    path('oldhomepage/', documentation.redirect_oldhomepage),
    # Voters
    path('voter/', voter_views.serve),
    path('voter/registration/', voter_views.voter_view),
    path('voter/edit/', voter_views.voter_edit_login),
    path('voter/edit/save/', voter_views.voter_edit),
    # Contestants
    path('contestant/', party_views.serve),
    path('contestant/registration/', party_views.party_view),
    path('contestant/edit/', party_views.voter_edit_login),
    path('contestant/edit/save/', party_views.voter_edit),
    path('contestant/profile/<slug:id>', show_profile.show_contestant),
    # Super Admins, Admins and Moderators only
    path('modzone/', adder.start_admin),
    path('modzone/authenticate/', startmod.authenticate_mod),
    path('modzone/logout/', logout.sign_out),
    path('modzone/access/', accesscontrols.control_access),
    path('modzone/mod/', ban.render_modzone),
    path('modzone/ban/', ban.ban),
    path('modzone/regulation/', regulation.mod_control_election),
    path('modzone/getstarted/', mod_doc.show_moderator_helppages),
    path('modzone/recompute/', result_view.reset_result),
    # Casting votes
    path('polls/', election_view.voter_screening),
    path('polls/cast/', cast.cast_vote),
    # Results and Exit Polls
    path('results/', result_view.result_view),
    path('results/turnout/gender/', result_view.voter_turnout_gender),
    # Personalization
    path('customize/', customize.personalization),
    # Robots (robots.txt)
    path('robots.txt', robots_txt.show_robots),
    path('robots.txt/', robots_txt.route_to_correct_robots)
]
