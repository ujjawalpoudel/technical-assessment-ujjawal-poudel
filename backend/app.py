from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from models import Article
from data import ARTICLES

app = FastAPI()

# Allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/articles", response_model=List[Article])
def list_articles(featured: Optional[bool] = Query(None)):
    articles = ARTICLES

    if featured:
        # return only featured when featured == "true",
        articles = [a for a in articles if a.is_featured]

    else:
        # only non-featured when featured == "false".
        articles = [a for a in articles if not a.is_featured]

    return articles


@app.get("/api/articles/{article_id}", response_model=Article)
def get_article(article_id: int):
    try:
        # it takes too much operation, first check each and every articles from ARTICLES data
        # and check with the input id with articles id, if it found it will return the given value
        # other wise raise expection as Article not found

        # TODO:- More optimization need for large dataset.
        
        for a in ARTICLES:
            if a.id == article_id:
                return a
        
        raise HTTPException(status_code=404, detail="Article not found")
        # return ARTICLES[article_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Article not found")


@app.post("/api/articles", response_model=Article, status_code=201)
def create_article(article: Article):
    for idx, existing in enumerate(ARTICLES):
        if existing.id == article.id:
            ARTICLES[idx] = article
            return article

    ARTICLES.append(article)
    return article
