from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
	# User.objects.all().delete()
	return render(request, "quotable_app/index.html")


def register(request):
	response = User.objects.register(
	request.POST["first"],
	request.POST["last"],
	request.POST["alias"],
	request.POST["email"],
	request.POST["dob"],
	request.POST["password"],
	request.POST["confirm"]
	)
	print response
	if response["valid"]:
		request.session["user_id"] = response["user"].id
		return redirect("/dashboard")
	else:
		for error_message in response["errors"]:
			messages.add_message(request, messages.ERROR, error_message)
		return redirect("/")

def login(request):
	response = User.objects.login(
		request.POST["email"],
		request.POST["password"]
	)
	if response["valid"]:
		request.session["user_id"] = response["user"].id
		return redirect("/dashboard")
	else:
		for error_message in response["errors"]:
			messages.add_message(request, messages.ERROR, error_message)
		return redirect("/")

def logout(request):
	request.session.clear()
	return redirect("/")

def quote(request):
	if "user_id" not in request.session:
		return redirect("/")
	loggedin_user = User.objects.get(id=request.session['user_id'])
	favorite_quotes =Quote.objects.filter(quotes_participant=loggedin_user)

	print "loggedin_user", loggedin_user 
	print "favorite_quotes", favorite_quotes

	context = {
		"user": User.objects.get(id=request.session["user_id"]), 
		"all_users": User.objects.all().exclude(id=request.session["user_id"]),
		"quotable_quotes": Quote.objects.exclude(quotes_participant=loggedin_user),
		"Favs" : favorite_quotes
	}
	return render(request, "quotable_app/dashboard.html", context)

def add_quote(request):
	loggedin_user = User.objects.get(id=request.session["user_id"])

	new_quote = Quote.objects.create(quoted_by=request.POST["quoted_by"],content=request.POST["content"], posted_by=loggedin_user)

	return redirect("/dashboard")
def add_favs(request, quote_id):
	print "quote id is:...", quote_id

	favorited_quote = Quote.objects.get(id=quote_id)
	loggedin_user = User.objects.get(id=request.session["user_id"])
	favorited_quote.quotes_participant.add(loggedin_user)

	print "loggedin_user", loggedin_user

	return redirect("/dashboard")

def remove_fav(request, quote_id):
	
	favorited_quote = Quote.objects.get(id=quote_id)
	loggedin_user = User.objects.get(id=request.session["user_id"])
	favorited_quote.quotes_participant.remove(loggedin_user)

	return redirect("/dashboard")
	
def user(request, user_id):

	user = User.objects.get(id=user_id)
	quote = Quote.objects.filter(posted_by=user_id)
	count = Quote.objects.filter(posted_by=user_id).count()

	context = {
	"user": User.objects.get(id=user_id),
	"my_quotes": quote,
	"count" : count
	}
	
	return render(request, "quotable_app/details.html", context)

