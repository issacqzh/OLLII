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
	if 'term' in request.GET:
		print('search')
	else:
		return render(request,'html_sites/implementor.html',{})
	address='http://spring-boot-engine:8080/implementorsearch'
	response = requests.get(address+request.GET.get('term'))
	params  = {"query": request.GET.get('term')}
	response = requests.get(address,params=params)
	print(response)
	response.raise_for_status()
	search_results = response.json()
	print(search_results)
	
	queryset_list = search_results
	paginator = Paginator(queryset_list, 10)
	page = request.GET.get('page',1)
	queryset_list = paginator.page(page)
	context = {
		"results": queryset_list,
		"title": "implementor results",
	}
	print(context)
	print("----hellloooo-------")
	return render(request,'html_sites/implementor.html',context)

def definition(request):
	if 'term' in request.GET:
		print('search')
	else:
		return render(request,'html_sites/definition.html',{})
	address='http://localhost:8080/meshterms'
	medplus_address='https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term='
	response = requests.get(address+request.GET.get('term'))
	params  = {"query": request.GET.get('term')}
	response = requests.get(address,params=params)
	
	response.raise_for_status()
	search_results = response.json()
	
	queryset_list = search_results
	

	
		

	for i in range(len(queryset_list)):
	
		rel_terms_string = queryset_list[i]['related_terms'][1:-1]

		rel_terms=rel_terms_string.split(",")
	
		for j in range(len(rel_terms)):
			rel_terms[j] = rel_terms[j][1:-1]
		queryset_list[i]['related_terms'] = rel_terms
		medplus_response = requests.get(medplus_address+queryset_list[i]['term']+'&retmax=1')
		tree = ElementTree.fromstring(medplus_response.content)
		try:
		    medplus_result = tree.find('list')[0]

		    link=medplus_result.attrib['url']
		    for row in medplus_result:
		        if row.attrib['name'] == 'title':
		            title=row.text
		            continue
		        if row.attrib['name'] == 'FullSummary':
		       		summary=row.text
		       		val = -1
		       		val = summary.find('</p>',val+1)
		       		overview=summary[:val+4]
		       		summary = summary[val+4:]
		       		continue
		    queryset_list[i]['medplus']={'url':link,'title':title,'overview':overview,'summary':summary}
		    # ['medplus'] = {'url':link,'title':title,'overview':overview,'summary':summary}
		   
		    
		except:
			print('no medlineplus articles')
	print(queryset_list)
	paginator = Paginator(queryset_list, 10)
	page = request.GET.get('page',1)
	queryset_list = paginator.page(page)

	context = {
		"results": queryset_list,
		"title": "implementor results",
	}

	print(context)
	print("----hellloooo-------")
	return render(request,'html_sites/definition.html',context)


# def definition(request):
# 	# if 'term' in request.GET:
# 	# 	print('search:'+str(request.GET.get('term')))
# 	# else:
# 	# 	return render(request,'html_sites/definition.html',{})
# 	# address='https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term='
# 	# response = requests.get(address+request.GET.get('term')+'&retmax=15')
# 	# tree = ElementTree.fromstring(response.content)
# 	# f_results=[]
# 	# for result in tree.find('list'):
# 	# 	link = result.attrib['url']
# 	# 	for row in result:
# 	# 		if row.attrib['name'] == 'title':
# 	# 			title = row.text
# 	# 			continue
# 	# 		if row.attrib['name'] == 'FullSummary':
# 	# 			summary = row.text
# 	# 			continue
# 	# 	f_results.append({'url':link,'title':title,'summary':summary})
# 	# paginator = Paginator(f_results,5)
# 	# page=request.GET.get('page',1)
# 	# queryset_list = paginator.page(page)
# 	# context = {
# 	# 	'results': queryset_list,
# 	# 	'term': request.GET.get('term'),
# 	# 	'pages': paginator.page_range
# 	# }
# 	# print(f_results)
# 	# print(context)
# 	# return render(request,'html_sites/definition.html',context)

	
# 	# if 'term' in request.GET:
# 	#     print('s')
# 	# else:
# 	#     return render(request,'html_sites/search.html',{})


# 	if 'term' in request.GET:
# 		print('search:'+str(request.GET.get('term')))
# 	else:
# 		return render(request,'html_sites/definition.html',{})

# 	basic_address='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
# 	search_address='esearch.fcgi?db=mesh&retmax=100&term='
# 	summary_address='esummary.fcgi?db=mesh&retmax=100&id='
# 	id_results=[]
# 	with requests.Session() as s:
# 	    response = s.get(basic_address+search_address+request.GET.get('term'))
# 	    tree = ElementTree.fromstring(response.content)
# 	    for result in tree.find('IdList'):
# 	        id_results.append(result.text)
# 	    s.close()

# 	final_id=None
# 	final_term=None
# 	with requests.Session() as s:
# 	    for i in range(len(id_results)):

# 	        response=s.get(basic_address+summary_address+id_results[i])
# 	        print(len(id_results))
# 	        print(id_results[i])
# 	        print(response.content)
# 	        tree=ElementTree.fromstring(response.content)
# 	        for item in tree[0].findall('Item'):
# 	            if item.attrib['Name']=="DS_MeshTerms":
# 	                for mesh in item:
# 	                    if mesh.text.lower() == request.GET.get('term').lower():
# 	                        final_id=id_results[i]
# 	                        final_term = mesh.text
# 	                        break

# 	        time.sleep(1)
# 	        if i >2: break
# 	    s.close()
# 	if final_id is None:
# 	    print("None")
# 	else:
# 	    with requests.Session() as s:
# 	        result_response=s.get(basic_address+summary_address+final_id)
# 	        tree = ElementTree.fromstring(result_response.content)
# 	        related=[]
# 	        for item in tree[0].findall('Item'):
# 	            if item.attrib['Name'] == "DS_ScopeNote":
# 	                definition= item.text
# 	            elif item.attrib['Name']=="DS_SeeRelated":
# 	                for row in item:
# 	                    related.append(row.text)
# 	            elif item.attrib['Name']=="DS_IdxLinks":
# 	                for linked_tree in item:
# 	                    for tree_item in linked_tree:
# 	                        if tree_item.attrib['Name'] == "Parent":
# 	                            related.append(tree_item.text)
# 	                        elif tree_item.attrib['Name'] == "Children":
# 	                            for child in tree_item:
# 	                                related.append(child.text)
# 	                        else:
# 	                            continue
# 	        context={'term':final_term,'definition':definition, 'related':related}
# 	        s.close()
# 	return render(request,'html_sites/definition.html',context)
