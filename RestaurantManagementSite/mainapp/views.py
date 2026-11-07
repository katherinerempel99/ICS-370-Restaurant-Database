from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    # Request object taken as a parameter will allow us to access things like query parameters and the body of different requests that are
    # being sent to this function 
    # return HttpResponse("hello world!")

    return render(request, "home.html") # render the template, only works if templates are inside directory