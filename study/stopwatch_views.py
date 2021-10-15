from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy


def sample(request):
    if request.method == "POST":
        if "start_button" in request.POST:
        # 以下にstart_buttonがクリックされた時の処理を書いていく
          print("スタートボタンを押した")
          return redirect('study:record_input')
        elif "finish_button" in request.POST:
        # 以下にfinish_buttonがクリックされた時の処理を書いてく
          print("ストップボタンを押した")
