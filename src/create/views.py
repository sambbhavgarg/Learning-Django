from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm, RawProductForm
from .models import Banner

# Create your views here.
def Feed(request, *args, **kwargs):
	queryset = Banner.objects.order_by('-id')
	feed_input = RawProductForm()
	context = {"form" : feed_input, "object_list": queryset}
	if request.method == "POST":
		feed_input = RawProductForm(request.POST)
		if feed_input.is_valid():
			Banner.objects.create(**feed_input.cleaned_data)
			# print(time)
			return render(request, "Feed.html", context)
	return render(request, "Feed.html", context)


def Profile(request, *args, **kwargs):
    return render(request, "Profile.html")