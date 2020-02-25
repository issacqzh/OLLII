from django.shortcuts import render
from django.http import HttpResponse
from pymed import PubMed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

pubmed = PubMed(tool="MyTool", email="my@email.address")

def home(request):
	return render(request,'html_sites/home.html')

def about(request):
	return render(request,'html_sites/about.html')

# def help4mom(request):
# 	return render(request,'html_sites/help4mom.html')

def vocabulary(request):
	return render(request,'html_sites/vocabulary.html')

def later(request):
	return render(request,'html_sites/later.html')



def help4mom(request):
    if "stage1" in request.GET:
        print("antepartum")
        q = "antepartum prenatal"
        stage = "Antepartum"
    elif "stage2" in request.GET:
        print("intrapartum")
        q = "intrapartum labor and delivery management"
        stage = "Intrapartum"
    elif "stage3" in request.GET:
        print("postpartum")
        q = "postpartum"
        stage = "Postpartum"
    else:
        return render(request,'html_sites/help4mom.html',{})

    pubmed_results = pubmed.query(q, max_results=20)
    f_results = []

    for result in pubmed_results:
        dict_result = result.toDict()
        f_results.append(dict_result)

    paginator = Paginator(f_results, 20)
    page = request.GET.get('page',1)
    queryset_list = paginator.page(page)

    context = {
		"results": queryset_list,
		"title": "Pub Med Results",
        "stage": stage,
        "query": q,
	}

    print("Context:"+str(context))
    return render(request,'html_sites/help4mom.html',context)
