from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Note, TodoItem


# -----------------------
# AUTH
# -----------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")

        return render(request, "notes/login.html", {"error": "Hatalı giriş"})

    return render(request, "notes/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 1. şifre kontrolü
        if password1 != password2:
            return render(request, "notes/register.html", {
                "error": "Şifreler aynı değil"
            })

        # 2. kullanıcı var mı kontrolü
        if User.objects.filter(username=username).exists():
            return render(request, "notes/register.html", {
                "error": "Bu kullanıcı adı zaten alınmış"
            })

        User.objects.create_user(
            username=username,
            password=password1
        )

        return redirect("login")

    return render(request, "notes/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# -----------------------
# HOME
# -----------------------

def home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    notes = Note.objects.filter(user=request.user)\
        .prefetch_related("items")\
        .order_by("-updated_at")

    return render(request, "notes/home.html", {"notes": notes})


# -----------------------
# ADD NOTE
# -----------------------

def add_note(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        title = request.POST.get("title")
        note_type = request.POST.get("type", "note")

        if not title:
            return render(request, "notes/add_note.html", {
                "error": "Başlık boş olamaz"
            })

        content = request.POST.get("content")

        note = Note.objects.create(
            user=request.user,
            title=title,
            content=content,
            type=note_type
        )

        # checklist items (frontend’den gelir)
        items = request.POST.getlist("items[]")

        for item in items:
            if item.strip():
                TodoItem.objects.create(
                    note=note,
                    text=item
                )

        return redirect("home")

    return render(request, "notes/add_note.html")


# -----------------------
# EDIT NOTE
# -----------------------

def edit_note(request, note_id):

    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    if request.method == "POST":

        note.title = request.POST.get("title")

        note_type = request.POST.get("type", "note")

        note.type = note_type

        # NORMAL NOTE
        if note_type == "note":

            note.content = request.POST.get("content", "")

            note.items.all().delete()

        # TODO NOTE
        else:

            note.content = ""

            note.items.all().delete()

            items = request.POST.getlist("items[]")

            for item in items:

                if item.strip():

                    TodoItem.objects.create(
                        note=note,
                        text=item
                    )

        note.save()

        return redirect("home")

    return render(request, "notes/edit_note.html", {
        "note": note
    })


# -----------------------
# DELETE NOTE
# -----------------------

def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect("home")


# -----------------------
# NOTE DETAIL API
# -----------------------

def note_detail_api(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    return JsonResponse({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "type": note.type,
        "created_at": str(note.created_at)
    })


# -----------------------
# TOGGLE TASK (ŞU AN GERÇEK DEĞİL - PLACEHOLDER)
# -----------------------

def toggle_task(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)

    item.is_done = not item.is_done
    item.save()

    return JsonResponse({
        "id": item.id,
        "is_done": item.is_done
    })
