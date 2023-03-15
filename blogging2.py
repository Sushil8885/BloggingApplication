from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Form, Header
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


###################################################
# How to add a pydantic model and field validation?
###################################################
class Blog(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(max_length=100, min_length=1)
    description: str = Field(
        title="description of blog",
        max_length=250,
        min_length=1
    )
    rating: int = Field(gt=1, lt=101)

    class Config:
        schema_extra = {
            "example":
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "title": "Random title",
                    "author": "Sushil",
                    "description": "This is a very interesting blog",
                    "rating": 75
                }
        }


class BlogResponseWoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None,
        title="description of blog",
        max_length=250,
        min_length=1
    )


app = FastAPI()

BLOGS = []

###################################################
# How to write custom exception in fastapi?
###################################################


class NegativeNumberException(Exception):
    def __init__(self, blogs_to_return):
        self.blogs_to_return = blogs_to_return


@app.exception_handler(NegativeNumberException)
def negative_number_exception_handler(request: Request,
                                      exception: NegativeNumberException):
    return JSONResponse(status_code=400,
                        content={"message":f"too less blogs - {exception.blogs_to_return}"})


# V2 endpoints


def raise_item_cannot_found_exception():
    raise HTTPException(status_code=404,
                        detail="Blog not found")


def create_blogs_without_api():
    blog_1 = Blog(id="64d9e434-0113-4ba6-92a6-05c6ceb9c384",
                  title="Title 1",
                  author="Sushil1",
                  description="description 1",
                  rating=75)
    blog_2 = Blog(id="64d9e437-0113-4ba6-92a6-05c6ceb9c384",
                  title="Title 2",
                  author="Sushil2",
                  description="description 2",
                  rating=75)
    blog_3 = Blog(id="64d9e438-0113-4ba6-92a6-05c6ceb9c384",
                  title="Title 3",
                  author="Sushil3",
                  description="description 3",
                  rating=75)
    blog_4 = Blog(id="64d9e439-0113-4ba6-92a6-05c6ceb9c384",
                  title="Title 4",
                  author="Sushil4",
                  description="description 4",
                  rating=75)
    BLOGS.append(blog_1)
    BLOGS.append(blog_2)
    BLOGS.append(blog_3)
    BLOGS.append(blog_4)

###################################################
# How to write a POST request with JSON request body?
###################################################


@app.post("/v2/create_blog", status_code=201)
def create_blog(blog: Blog):
    BLOGS.append(blog)
    return BLOGS

###################################################
# How to add a response validation in FastAPI?
###################################################


@app.get("/blog/rating/{_id}", response_model=BlogResponseWoRating)
def read_blog_no_rating(blog_id: UUID):
    for x in BLOGS:
        if x.id == blog_id:
            return x

    return raise_item_cannot_found_exception()


@app.get("/v2/")
def rear_all_blogs(blogs_to_return: Optional[int] = None):

    if blogs_to_return and blogs_to_return < 0:
        raise NegativeNumberException(blogs_to_return=blogs_to_return)

    if len(BLOGS) < 1:
        create_blogs_without_api()

    if blogs_to_return and blogs_to_return <= len(BLOGS):
        i = 1
        new_blogs = []
        while i <= blogs_to_return:
            new_blogs.append(BLOGS[i-1])
            i += 1

        return new_blogs
    return BLOGS


@app.get("/v2/{blog_id}")
def read_blog(blog_id: UUID):
    for x in BLOGS:
        if x.id == blog_id:
            return x
    return raise_item_cannot_found_exception()


@app.put("/v2/{blog_id}")
def update_blog(blog_id: UUID, blog: Blog):
    counter = 0
    for x in BLOGS:
        counter += 1
        if x.id == blog_id:
            BLOGS[counter-1] = blog
            return BLOGS[counter-1]

    return raise_item_cannot_found_exception()


@app.delete("/v2/{blog_id}")
def update_blog(blog_id: UUID):
    counter = 0
    for x in BLOGS:
        counter += 1
        if x.id == blog_id:
            del BLOGS[counter-1]
            return f"ID - {blog_id} has been deleted"

    return raise_item_cannot_found_exception()


###################################################
# How to send a form data in request?
###################################################

@app.post("/blogs/login")
def blog_login(username: str = Form(), password: str = Form()):
    return {"username": username, "password": password}

###################################################
# How can we pass header in each request?
###################################################


@app.get("/header")
def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


