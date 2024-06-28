from django.shortcuts import render

# Create your views here.
def champ_info(request):
    return render(request, 'champInfos/champInfos.html')