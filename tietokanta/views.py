from django.shortcuts import render
from .models import Triathlon_Record

def record_list(request): #Ohjelman laajentuessa voi olla tarpeen miettiä funktioiden nimeämislogiikkaa.
    records = Triathlon_Record.objects.all()
    return render(request, 'tietokanta/triathlon_record_list.html', {'records': records})

def test_page(request):
    return render(request, 'tietokanta/test_page.html')



