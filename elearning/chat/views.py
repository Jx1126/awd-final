from django.shortcuts import render


def search_room(request):
    return render(request, "chat/search_room.html")


def chat_room(request, room_name):
    return render(request, "chat/chat_room.html", {"room_name": room_name})
