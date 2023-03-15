from typing import Optional
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel


###################################################
# How to add a pydantic model and field validation?
###################################################
class Blog(BaseModel):
    title: str
    author: str


class LanguageName(Enum):
    python = "Python"
    java = "Java"
    golang = "Golang"


app = FastAPI()

BLOGS = {
    "blog_1": {"title": "random title 1", "auther": "random auther 1"},
    "blog_2": {"title": "random title 2", "auther": "random auther 2"},
    "blog_3": {"title": "random title 3", "auther": "random auther 3"},
    "blog_4": {"title": "random title 4", "auther": "random auther 4"},
    "blog_5": {"title": "random title 5", "auther": "random auther 5"},
}
###################################################
# How to enumeration class to get drop down?
###################################################


@app.get("/languages/{language_name}")
def get_language(language_name: LanguageName):
    if language_name == LanguageName.python:
        return {"language": language_name, "feature": "easy"}
    elif language_name == LanguageName.java:
        return {"language": language_name, "feature": "tough syntax"}
    elif language_name == LanguageName.golang:
        return {"language": language_name, "feature": "language for google"}


###################################################
# How to pass query parameter in FastAPI?
###################################################


@app.get("/")
def get_all_blogs(skip_blog: Optional[str] = None):
    if skip_blog:
        new_copy = BLOGS.copy()
        del new_copy[skip_blog]
        return new_copy
    return BLOGS


###################################################
# How to add path in FastAPI endpoint?
###################################################


@app.get("/{blog_name}")
def get_blog(blog_name: str):
    return BLOGS.get(blog_name)


###################################################
# How to delete in FastAPI endpoint?
###################################################


@app.delete("/{blog_name}")
def delete_blog(blog_name):
    del BLOGS[blog_name]
    return f"Blog `{blog_name}` has been deleted"


###################################################
# How to write a POST request in FastAPI?
###################################################


@app.post("/")
def create_blog(blog_title, blog_author):
    current_blog_id = 0

    if len(BLOGS) > 0:
        for blog in BLOGS:
            x = blog.split("_")[-1]
            x = int(x)
            if x > current_blog_id:
                current_blog_id = x

    new_index = "blog_" + str(current_blog_id + 1)
    BLOGS[new_index] = {"title": blog_title, "auther": blog_author}
    return BLOGS


###################################################
# How to write a PUT request in FastAPI?
###################################################


@app.put("/{blog.name}")
def update_blog(blog_name: str, blog_title: str, blog_author: str):
    blog_info = {"title": blog_title, "author": blog_author}
    BLOGS[blog_name] = blog_info
    return BLOGS


# V2 endpoints

###################################################
# How to write a POST request with JSON request body?
###################################################


@app.post("/v2/createblog")
def create_blog(blog: Blog):
    BLOGS.append(blog)
    return BLOGS
