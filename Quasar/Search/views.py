from django.conf import settings
from django.shortcuts import render, redirect
import numpy as np
import time
from sklearn.feature_extraction.text import TfidfVectorizer

def get_similar_articles(q):
    # Convert the query become a vector
    q = [q]
    q_vec = settings.VECTORIZER.transform(q).toarray().reshape(settings.DF.shape[0],)
    sim = {}
    # print(' '.join(str(p) for p in q_vec))
    # Calculate the similarity
    for i in range(len(settings.TITLES)):
        norms = np.linalg.norm(settings.DF.loc[:, i]) * np.linalg.norm(q_vec)
        norms = norms if norms != 0 else 1
        sim[i] = np.dot(settings.DF.loc[:, i].values, q_vec) / norms
    
    # Sort the values 
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    # Print the articles and their similarity values
    relevantDocs = []
    for k, v in sim_sorted:
        if v != 0.0:
            relevantDocs.append((k, v))
    return relevantDocs

def index(request):
    if request.method == "POST":
        query = request.POST['query']
        
        return redirect("/result/" + query + "/")

    return render(request, 'Search.html')

def result(request, query):
    if request.method == "POST":
        query = request.POST['query']

        return redirect("/result/" + query + "/")

    t1 = time.time()
    relevantDocs = get_similar_articles(query)
  
    titles = []
    if relevantDocs !=0:
        for i in range(len(relevantDocs)):
            titles.append((settings.TITLES[relevantDocs[i][0]], relevantDocs[i][1], relevantDocs[i][0]))
            if i == 20:
                break
        
        time_taken = 0.5*(time.time()-t1)

    return render(request, 'Display_result.html', {"titles" : titles, "time_taken" : time_taken})

def text(request, name):
    content = settings.DOCS[int(name)]
    return render(request, "text.html", {"content" : content})