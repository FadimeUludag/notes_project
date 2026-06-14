from django.urls import path
from .views import (
    login_view,
    register_view,
    home_view,
    add_note,
    edit_note,
    delete_note,
    note_detail_api,
    logout_view,
    toggle_task
)

urlpatterns = [
    # AUTH
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

    # MAIN PAGE
    path("", home_view, name="home"),

    # NOTES PAGES (form sayfaları)
    path("api/add/", add_note, name="add_note"),
    path("api/edit/<int:note_id>/", edit_note, name="edit_note"),
    path("api/delete/<int:note_id>/", delete_note, name="delete_note"),

    # API
    path("api/notes/<int:note_id>/", note_detail_api),
    path("api/toggle-task/<int:item_id>/", toggle_task, name="toggle_task"),
]
