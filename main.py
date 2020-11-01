from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import twint

# Increments of 20
LIMIT = 20


def searchTweets(username, search, city, since, until):
    c = twint.Config()

    tweets = []

    if username != "":
        c.Username = username
    if search != "":
        c.Search = search
    if city != "":
        c.Near = city
    if since != "":
        c.Since = since
    if until != until:
        c.Until = until

    if LIMIT > 0:
        c.Limit = LIMIT
    c.Store_object = True
    c.Hide_output = True
    c.Store_object_tweets_list = tweets
    twint.run.Search(c)
    return(tweets)


app = FastAPI()

origins = [
    "https://twinvestigo.com",
    "http://twinvestigo.com",
    "*"
]

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


class SearchParameters(BaseModel):
    username: Optional[str] = ""
    searchText: Optional[str] = ""
    city: Optional[str] = ""
    since: Optional[str] = ""
    until: Optional[str] = ""


@app.get("/")
def root():
    return "It's working"


@app.post("/api/search")
def search(search: SearchParameters):
    response = []
    username = search.username
    searchText = search.searchText
    city = search.city
    since = search.since
    until = search.until
    response = searchTweets(username, searchText, city, since, until)
    return response
