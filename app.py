import base64
from io import BytesIO
from starlette.requests import Request

import uvicorn

#import numpy as np
import matplotlib
#import pandas as pd

matplotlib.use("Agg")
#from matplotlib import pyplot as plt
from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from MBPgraph import make_plot
from graph2 import make_data


app = FastAPI()

def fig_to_base64(fig):
    # Figure を base64 文字列に変換する。
    # Bytes IO に対して、エンコード結果を書き込む。
    ofs = BytesIO()
    fig.savefig(ofs, format="png")
    gif_data = ofs.getvalue()

    # バイト列を base64 文字列に変換する。
    base64_data = base64.b64encode(gif_data).decode()

    return base64_data

templates = Jinja2Templates(directory='templates')

@app.get("/")
async def read_item(request:Request,
                    nbins: int = 30, interval: float = 0.1,
                    x: float = -0.75, y: float = 0.55,
                    check: str = '', step: float = 0.01):
    # グラフを作成する。
    print("nbins:", nbins)
    print("interval:",interval)
    print("x=",x,"y=",y)
    print("step=",step)

    check_value = 0 if check == "on" else 1
    print("check_value:",check_value)
    make_data(x,y,check_value,step)
    fig = make_plot(nbins,interval)

    # グラフを base64 文字列に変換する。
    img = fig_to_base64(fig)

    return templates.TemplateResponse("index.html", {"request":request,"gif":img, "step": step, "x":x, "y":y,})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
gitのテスト わーい
"""