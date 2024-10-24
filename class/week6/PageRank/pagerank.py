import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages



def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N=len(corpus)
    transition=dict()

    for p in corpus.keys():
        transition[p]=round((1-damping_factor)/N,5)

    toPage=corpus[page]
    num_links=len(toPage)
    if num_links>0:
        for i in toPage:
            transition[i]=round(damping_factor*1/num_links,5)+transition[i]
    else:
        for p in corpus.keys():
            transition[p] = round(1 / N, 5)

    return transition



def sample_pagerank(corpus, damping_factor, T):
    """
    Return PageRank values for each page by sampling `T` times.
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank=dict()

    for p in corpus.keys():
        pageRank[p]=0

    sample=random.choice(list(corpus.keys()))
    pageRank[sample]=pageRank[sample]+1

    for i in range(1,T):
        pr_next=transition_model(corpus,sample,damping_factor)
        sample=random.choices(list(pr_next.keys()),weights=list(pr_next.values()),k=1)[0]
        pageRank[sample]=pageRank[sample]+1

    for p in corpus.keys():
        pageRank[p]=pageRank[p]/T

    return pageRank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N=len(corpus)
    pageRank=dict()

    for p in corpus.keys():
        pageRank[p]=round(1/N,5)

    while True:
        d=0
        for p in corpus.keys():
            old = pageRank[p]
            X=0
            for p0 in corpus.keys():
                if p in corpus[p0]:
                    X=X + (1/len(corpus[p0])) * pageRank[p0]
                if len(corpus[p0])==0:
                    X=X + (1/N) * pageRank[p0]

            new=round((1-damping_factor)/N+damping_factor*X,5)
            d=d+abs(new-old)
            pageRank[p]=new

        if d<0.001:
            break
    return pageRank


if __name__ == "__main__":
    # command line argument format
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    # Retrive the links between pages
    corpus = crawl(sys.argv[1])

    # Generate PageRank Score using Random Suffer Model
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)

    # Print out the result in the terminal
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    # Generate PageRank Score using Iterative Algorithm
    ranks = iterate_pagerank(corpus, DAMPING)

    # Print out the result in the terminal
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
