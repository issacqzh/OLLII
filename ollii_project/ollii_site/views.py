from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib.request
import requests
from xml.etree import ElementTree
import time
# Create your views here.
# 


def vocabulary(request):
	return render(request,'html_sites/vocabulary.html')
def about(request):
    return render(request,'html_sites/about.html')

def home(request):
    return render(request,'html_sites/home.html')



def help4mom(request):

    if 'term' in request.GET:
        print('search')
    else:
        return render(request,'html_sites/help4mom.html',{})

    address='https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term='

    response = requests.get(address+request.GET.get('term')+'&retmax=35')
    tree = ElementTree.fromstring(response.content)
    f_results=[]
    for result in tree.find('list'):
        # url
        link=result.attrib['url']
        for row in result:
            if row.attrib['name'] == 'title':
                title=row.text
                continue
            if row.attrib['name'] == 'FullSummary':
                
                summary=row.text
                continue
        f_results.append({'url':link,'title':title,'summary':summary})

    paginator=Paginator(f_results,5)
    page=request.GET.get('page',1)
    queryset_list=paginator.page(page)

    context = {
        'results': queryset_list,
        'term': request.GET.get('term'),
        'pages': paginator.page_range
    }

    return render(request,'html_sites/help4mom.html',context)


def implementor(request):
    return render(request,'html_sites/implementor.html',{})





def definition(request):
    # return render(request,'html_sites/definition.html',{})
    if 'term' in request.GET:
        print('s')
    else:
        return render(request,'html_sites/definition.html',{})

    basic_address='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    search_address='esearch.fcgi?db=mesh&retmax=1000&term='
    summary_address='esummary.fcgi?db=mesh&retmax=1000&id='
    id_results=[]
    with requests.Session() as s:

        response = s.get(basic_address+search_address+request.GET.get('term'))
        tree = ElementTree.fromstring(response.content)
        id_list=tree.find('IdList')
        for id_ in id_list:
            id_results.append(id_.text)

    
    final_id=None
    final_term=None
    final_def=None
    with requests.Session() as s:
        for i in range(len(id_results)):
     
            response=s.get(basic_address+summary_address+id_results[i])
        
            tree=ElementTree.fromstring(response.content)
            temp_def=None
            for item in tree[0].findall('Item'):
                if item.attrib['Name']=="DS_ScopeNote":
                    temp_def= item.text
                if item.attrib['Name']=="DS_MeshTerms":
                    for mesh in item:
                        if mesh.text.lower() == request.GET.get('term').lower():
                            final_id=id_results[i]
                            final_term = mesh.text
                            final_def=temp_def
                            break
            time.sleep(0.4)
    if final_id is None:
        context={}
    else:
        related=[]
        related_terms=[]
        with requests.Session() as s:
            result_response=s.get(basic_address+summary_address+final_id)
            tree = ElementTree.fromstring(result_response.content)
            for item in tree[0].findall('Item'):
                if item.attrib['Name']=="DS_SeeRelated":
                    for row in item:
                        related.append(row.text)
                elif item.attrib['Name']=="DS_IdxLinks":
                    for linked_tree in item:
                        for tree_item in linked_tree:
                            if tree_item.attrib['Name'] == "Parent":
                                related.append(tree_item.text)
                            elif tree_item.attrib['Name'] == "Children":
                                for child in tree_item:
                                    related.append(child.text)
                            else:
                                continue
            time.sleep(0.4)   
            for related_id in related:
                related_response = s.get(basic_address+summary_address+related_id)
                related_tree = ElementTree.fromstring(related_response.content) 
                for item in related_tree[0].findall('Item'):
                    if item.attrib['Name'] == 'DS_MeshTerms':
                        related_terms.append(item[0].text)
                        break
                time.sleep(0.4)
        context={'term':final_term,'definition':final_def, 'related':related_terms}

    return render(request,'html_sites/definition.html',context)   

        

