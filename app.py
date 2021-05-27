from starlette.requests import Request
import uvicorn

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from bokeh.embed import components
from bokeh.resources import INLINE

from make_plot2 import make_plot
from graph2 import make_data


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

@app.get("/")
async def read_item(request:Request,
                    #intervalのデフォルトは0.05
                    interval: float = 0.05,
                    x: float = -0.75, y: float = 0.55,
                    tone: int = 20, check: int = 0,
                    step: float = 0.01):
    # グラフを作成する。
    print("colortone:", tone)
    print("interval:",interval)
    print("x=",x,"y=",y)
    print("step=",step)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    check_value = check
    print("check_value:",check_value)
    make_data(x,y,check_value,step)
    fig = make_plot(tone,interval)

    script, div = components(fig, INLINE)
    # print(script)
    # print(div)


    return templates.TemplateResponse("index.html", {"request":request,
                                                      "js_resources":js_resources,
                                                      "css_resources": css_resources,
                                                      "plot_div": div, "plot_script": script,
                                                      "step": step, "x":x, "y":y,"tone":tone, "check":check})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)