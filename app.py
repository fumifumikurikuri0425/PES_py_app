from utils import create_test_data
from fastapi.params import File
from starlette.requests import Request
import uvicorn

from fastapi import FastAPI, Request, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.embed import json_item

from make_plot2 import make_plot
from graph2 import make_data


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_item_1(
    request: Request,
    # intervalのデフォルトは0.05
    interval: float = 0.01,
    x: float = -0.75,
    y: float = 0.55,
    tone: int = 20,
    check: int = 0,
    step: float = 0.01,
    xmin: float = -2.5,
    xmax: float = 1.5,
    ymin: float = -1,
    ymax: float = 3,
    zmin: float = -147,
    zmax: float = 100,
):
    # グラフを作成する。
    print("colortone:", tone)
    print("interval:", interval)
    print("x=", x, "y=", y)
    print("step=", step)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    check_value = check
    print("check_value:", check_value)
    make_data(x, y, check_value, step)
    fig = make_plot(tone, interval, xmin, xmax, ymin, ymax, zmin, zmax)

    script, div = components(fig, INLINE)
    # print(script)
    # print(div)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "js_resources": js_resources,
            "css_resources": css_resources,
            "plot_div": div,
            "plot_script": script,
            "step": step,
            "x": x,
            "y": y,
            "tone": tone,
            "check": check,
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
            "zmin": zmin,
            "zmax": zmax,
        },
    )


@app.get("/api2")
async def read_item_2(
    request: Request,
    # intervalのデフォルトは0.05
    interval: float = 0.1,
    x: float = -0.75,
    y: float = 0.55,
    tone: int = 5,
    check: int = 0,
    step: float = 0.01,
    xmin: float = -2.5,
    xmax: float = 1.5,
    ymin: float = -1,
    ymax: float = 3,
):
    # グラフを作成する。
    print("colortone:", tone)
    print("interval:", interval)
    print("x=", x, "y=", y)
    print("step=", step)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    check_value = check
    print("check_value:", check_value)
    make_data(x, y, check_value, step)
    fig = make_plot(tone, interval, xmin, xmax, ymin, ymax)

    script, div = components(fig, INLINE)
    # print(script)
    # print(div)

    retval = {
        "js_resources": js_resources,
        "css_resources": css_resources,
        "plot_div": div,
        "plot_script": script,
        "step": step,
        "x": x,
        "y": y,
        "tone": tone,
        "check": check,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
    }

    return retval


@app.get("/api3")
async def read_item_3(
    request: Request,
    # intervalのデフォルトは0.05
    interval: float = 0.1,
    x: float = -0.75,
    y: float = 0.55,
    tone: int = 5,
    check: int = 0,
    step: float = 0.01,
    xmin: float = -2.5,
    xmax: float = 1.5,
    ymin: float = -1,
    ymax: float = 3,
):
    # グラフを作成する。
    print("colortone:", tone)
    print("interval:", interval)
    print("x=", x, "y=", y)
    print("step=", step)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    check_value = check
    print("check_value:", check_value)
    make_data(x, y, check_value, step)
    fig = make_plot(tone, interval, xmin, xmax, ymin, ymax)

    script, div = components(fig, INLINE)
    # print(script)
    # print(div)

    retval = {
        "js_resources": js_resources,
        "css_resources": css_resources,
        "plot_div": div,
        "plot_script": script,
        "step": step,
        "x": x,
        "y": y,
        "tone": tone,
        "check": check,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
    }

    return json_item(fig, "myplot")


class Params(BaseModel):
    interval: float = 0.1
    x: Optional[float] = -0.75
    y: Optional[float] = 0.55


@app.post("/api/test")
async def post_api4(
    file: Optional[bytes] = File(None),
    interval: float = Form(0.05),
    x: float = Form(-0.75),
    y: float = Form(0.55),
    tone: int = Form(20),
    check: int = Form(0),
    step: float = Form(0.01),
    xmin: float = Form(-2.5),
    xmax: float = Form(1.5),
    ymin: float = Form(-1),
    ymax: float = Form(3),
):

    params = {
        "interval": interval,
        "x": x,
        "y": y,
        "tone": tone,
        "check": check,
        "step": step,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
    }

    # TODO: calculate values here!!!
    X_list, Y_list, Z_list = create_test_data(xmin, xmax, ymin, ymax, interval)

    return {"params": params, "data": [X_list, Y_list, Z_list]}


origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000", "ssss"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
