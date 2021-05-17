import base64
from io import BytesIO
from starlette.requests import Request

import uvicorn

import numpy as np
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
# from flask import Flask, render_template
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from graph import make_plot


app = FastAPI()

def fig_to_base64(fig):
    """Figure を base64 文字列に変換する。
    """
    # Bytes IO に対して、エンコード結果を書き込む。
    ofs = BytesIO()
    fig.savefig(ofs, format="png")
    png_data = ofs.getvalue()

    # バイト列を base64 文字列に変換する。
    base64_data = base64.b64encode(png_data).decode()

    return base64_data


def create_graph():
    """matplotlib のグラフを作成する。
    """
    x = np.linspace(-10, 10, 100)
    y = x ** 2

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Title", c="darkred", size="large")

    return fig

templates = Jinja2Templates(directory='templates')

@app.get("/")
async def read_item(request:Request, nbins: int = 20):
    # グラフを作成する。
    fig, ax = plt.subplots()
    ax.pie([100, 200, 300, 400, 500])

    print("nbins:", nbins)
    fig2 = make_plot(nbins)

    # グラフを base64 文字列に変換する。
    img = fig_to_base64(fig2)



    return templates.TemplateResponse("index.html", {"request":request,"img":img})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)