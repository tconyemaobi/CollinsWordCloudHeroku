# uvicorn main:app --reload

# from cgitb import handler
from fastapi import FastAPI
from fastapi.responses import HTMLResponse,StreamingResponse
# from typing import Optional
# from fastapi import APIRouter, Depends,Query

# from pyparsing import Optional

# matplotlib.use("TKAgg")
# matplotlib.use("agg") 
# matplotlib.use("macOSX")

from matplotlib import pyplot as plt # import matplotlib.pyplot as plt

import numpy as np
from PIL import Image
from wordcloud import STOPWORDS, WordCloud
import io
import urllib, base64
# from mangum import Mangum

tags_metadata = [
    {
        "name": "",
        "description": "",
        "externalDocs": {
            "description": "Contact me tc.onyemaobi@gmail.com ",
            "url": "https://camlds.com",
        },
    },
]

app = FastAPI(
    title="Collins Word Cloud",
    description="High Perfomance Endpoints ",
    version="1.0",
    openapi_tags=tags_metadata,
    docs_url="/docs", redoc_url="/re",
    openapi_url="/cwc/api/v1/coreapi.json",
    log_config=None
)
# handler = Mangum(app=app)

# app.add_middleware(
# CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
# )


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


def word_cloud(text):
    whale_mask = np.array(Image.open("static/img/cloud.png"))
    # stopwords ={'은','입니다'}
    stopwords = set(STOPWORDS)
    # plt.figure(figsize = (20,5))
    # font_path = 'C:/Users/Jeong Suji/NanumBarunGothic.ttf'
    wc = WordCloud(background_color = 'white', max_words=1000, mask = whale_mask, stopwords = stopwords,
                   prefer_horizontal=0.5, mode="RGBA")
    wc= wc.generate(text)
    plt.figure(figsize=[20,10])
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    image = io.BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)  # rewind the data
    string = base64.b64encode(image.read())

    image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
    return image_64


# def read_img(wordcloud):
#     with open(wordcloud, "rb") as image_file:
#         return base64.b64encode(image_file.read())
    
# None = Query(None, min_length=50, max_length=3000),
@app.get("/",response_class=HTMLResponse)
async def root(word: str = None):
    print(word)
    if word:
        text = ''
        for i in word:
            text += i
        wordcloud = word_cloud(text)
    if not word:
        wordcloud =''
    
    html_content = """
        <!doctype html>
        <html lang="en">
        <head>

            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

            <title>tc.onyemaobi@gmail.com</title>
        </head>
        <body class="container container-sm">
            <h1 class="display-6">Welcome to Collins Word Cloud</h1>
                   <form class="form-floating" action="">
                    <fieldset>
                        <legend class="lead">Word Cloud Example</legend>
                        <div class="mb-3">
                        <label class="form-label">Past your word</label>
                        <textarea type="text" name="word" min="50" max="3000" class="form-control" style="max-width: 70vw; min-height: 25vh;" required></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </fieldset>
                    </form>

             
             <p class="d-inline-block text-truncate" style="max-width: 40vw;">
                <abbr title="attribute"> {0}<abbr>     
             </p>
             <span class="fw-lighter">Integrate with your app with request/response method 
                        <a href="/docs" class="text-reset">Code Documentations</a>.
                    </span>
            <div class="mb-0">
                    <img src="{0}" class="img-fluid" style="max-height: 25rem;">  
                </div>
            <div class="justify-content-md-center justify-content-center justify-content-between">
            <p class="d-inline-block justify-content-md-center justify-content-center justify-content-between">
                <abbr title="attribute"> Opensource CWCv1 - By Collins Onyemaobi<abbr>     
             
             <span class="fw-lighter"> - 
                        <a href="#" class="text-reset">tc.onyemaobi@gmail.com</a>.
                    </span>
                    </p>
            </div>
        </body>
        </html>

    """
    html_content =  html_content.format(wordcloud)

    return HTMLResponse(content=html_content, status_code=200)



