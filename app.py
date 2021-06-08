from bokeh.util.dependencies import import_optional
from starlette.requests import Request
import uvicorn

from fastapi import FastAPI, Request, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

import numpy as np

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.embed import json_item

from make_plot2 import make_plot, get_contour_line
from optimize_line import make_data
from PES_from_file import make_graph_from_file

from utils import create_test_data, get_meshgrid_from_xyzArray


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
    judge: bool = False,
    step: float = 0.01,
    xmin: float = -2.5,
    xmax: float = 1.5,
    ymin: float = -1,
    ymax: float = 3,
    zmin: float = -147,
    zmax: float = 100,
    function_name: str = "mbp",
):
    print("colortone:", tone)
    print("interval:", interval)
    print("x=", x, "y=", y)
    print("step=", step)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    func = None
    import function_memo

    if function_name == "mbp":
        func = function_memo.muller_brown_potential
    elif function_name == "pes1":
        func = function_memo.pes1

    check_value = check
    print("check_value:", check_value)
    print("judge", judge)
    if judge:
        make_data(x, y, check_value, step, func)
    fig = make_plot(tone, interval, xmin, xmax, ymin, ymax, zmin, zmax, judge)
    # fig = make_graph_from_file(tone, zmax)
    print("fig finished!")

    script, div = components(fig, INLINE)

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
            "judge": judge,
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
            "zmin": zmin,
            "zmax": zmax,
        },
    )


@app.get("/post_version")
@app.post("/post_version")
async def post_test(
    request: Request,
    # file: UploadFile = File(...),
    interval: float = Form(0.1),
    x: float = Form(-0.75),
    y: float = Form(0.55),
    tone: int = Form(10),
    check: int = Form(0),
    judge: bool = Form(False),
    step: float = Form(0.01),
    xmin: float = Form(-2.5),
    xmax: float = Form(1.5),
    ymin: float = Form(-1),
    ymax: float = Form(3),
    zmin: float = Form(-147),
    zmax: float = Form(100),
):

    # file = request.files['file']
    # print("file: ", file)
    # print(file.file)
    # print(file.filename)
    # print(len(file))

    # グラフを作成する。
    print("colortone:", tone)
    print("interval:", interval)
    print("x=", x, "y=", y)
    print("step=", step)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    check_value = check
    print("check_value:", check_value)
    print("judge", judge)
    if judge:
        make_data(x, y, check_value, step)
    fig = make_plot(tone, interval, xmin, xmax, ymin, ymax, zmin, zmax, judge)
    # fig = make_graph_from_file(file.file, tone, zmax)

    script, div = components(fig, INLINE)
    # print(script)
    # print(div)

    return templates.TemplateResponse(
        "index_post.html",
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
            "judge": judge,
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
            "zmin": zmin,
            "zmax": zmax,
        },
    )


class Params(BaseModel):
    interval: float = 0.1
    x: Optional[float] = -0.75
    y: Optional[float] = 0.55


@app.post("/api/test")
async def post_api4(
    file: Optional[bytes] = File(None),
    resolution: float = Form(300),
    x: float = Form(-0.75),
    y: float = Form(0.55),
    tone: int = Form(40),
    check: int = Form(0),
    step: float = Form(0.01),
    xmin: float = Form(-2.5),
    xmax: float = Form(1.5),
    ymin: float = Form(-1),
    ymax: float = Form(3),
    zmin: float = Form(-147),
    zmax: float = Form(100),
):

    params = {
        "resolution": resolution,
        "x": x,
        "y": y,
        "tone": tone,
        "check": check,
        "step": step,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "zmin": zmin,
        "zmax": zmax,
    }

    print(params)

    # TODO: calculate values here!!!
    X_list, Y_list, Z_list = create_test_data(xmin, xmax, ymin, ymax, resolution)
    Z_list_meshed = get_meshgrid_from_xyzArray(X_list, Y_list, Z_list)
    # print("interval",interval)
    print("xrange: ", xmin, "~", xmax)
    print("yrange ", ymin, "~", ymax)
    X1_list, Y1_list, X2_list, Y2_list = make_data(x, y, check, step)
    contours = get_contour_line(Z_list_meshed, xmin, xmax, ymin, ymax, zmin, zmax, tone)
    return {
        "params": params,
        "data": {
            "energy": Z_list_meshed.tolist(),
            "contours": contours,
            "optimizeLine": {
                "x1_list": X1_list,
                "y1_list": Y1_list,
                "x2_list": X2_list,
                "y2_list": Y2_list,
            },
        },
    }


@app.post("/api/file")
async def post_api5(
    file: UploadFile = File(...), tone: int = Form(40), zmax: float = Form(100)
):

    params = {"tone": tone, "zmax": zmax}

    print(file)

    # print(file.name)
    print(file.filename)

    xmin, xmax, ymin, ymax, zmin, Z_list_meshed = make_graph_from_file(file.file, zmax)
    contours = get_contour_line(Z_list_meshed, xmin, xmax, ymin, ymax, zmin, zmax, tone)
    return {
        "params": params,
        "data": {
            "energy": Z_list_meshed.tolist(),
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
            "zmin": zmin,
            "contours": contours,
        },
    }


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
