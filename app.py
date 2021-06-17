import uvicorn
from fastapi import FastAPI, File, Form, UploadFile

from fastapi.middleware.cors import CORSMiddleware

from optimize_from_code import make_data_from_code
from optimize_line import make_data
from PES_from_file import make_graph_from_file
from utils import (
    create_pes_data,
    create_pes_data_from_code,
    get_meshgrid_from_xyzArray,
    get_contour_line,
)


app = FastAPI()


@app.post("/")
async def post_api4(
    # file: Optional[bytes] = File(None),
    function_name: str = Form("mbp"),
    resolution: float = Form(300),
    x: float = Form(-0.75),
    y: float = Form(0.55),
    tone: int = Form(20),
    check: int = Form(0),
    step: float = Form(0.01),
    xmin: float = Form(-2.5),
    xmax: float = Form(1.5),
    ymin: float = Form(-1),
    ymax: float = Form(3),
    zmin: float = Form(-147),
    zmax: float = Form(100),
    contour_on: bool = Form(False),
    optimize_on: bool = Form(False),
):

    params = {
        "function_name": function_name,
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
        "contour_on": contour_on,
        "optimize_on": optimize_on,
    }
    print("start")
    # ** make arrays for drawing pes
    X_list, Y_list, Z_list = create_pes_data(
        function_name, xmin, xmax, ymin, ymax, resolution
    )
    print("finish make arrays for pes")
    # ** convert arrays to mesh data array
    Z_list_meshed = get_meshgrid_from_xyzArray(X_list, Y_list, Z_list)
    print("finish convert arrays")
    result = {
        "params": params,
        "data": {
            "energy": Z_list_meshed.tolist(),
        },
    }
    # ** make data for contour line
    if contour_on:
        contours = get_contour_line(
            Z_list_meshed, xmin, xmax, ymin, ymax, zmin, zmax, tone
        )
        result["data"]["contours"] = {
            "contours": contours,
        }
        print("finish make contour")

    # ** make arrays for draw optimize line
    if optimize_on:
        (
            X1_list,
            Y1_list,
            X2_list,
            Y2_list,
            TS,
            EQ,
            count,
            Distance_list,
            Energy_list,
            TS_point,
        ) = make_data(function_name, x, y, check, step)
        result["data"]["optimizeLine"] = {
            "x1_list": X1_list,
            "y1_list": Y1_list,
            "x2_list": X2_list,
            "y2_list": Y2_list,
            "TS": TS,
            "EQ": EQ,
            "count": count,
            "Distance_list": Distance_list,
            "Energy_list": Energy_list,
            "TS_point": TS_point,
        }
        print("finish make arrays for draw optimize line")
    # print(result)

    return result


@app.post("/api/file")
async def post_api5(
    file: UploadFile = File(...),
    tone: int = Form(40),
    zmax: float = Form(100),
    contour_on: bool = Form(False),
):
    params = {"tone": tone, "zmax": zmax}
    # ** make data and array for pes
    xmin, xmax, ymin, ymax, zmin, Z_list_meshed = make_graph_from_file(file.file)
    # ** make array for contour line
    contours = get_contour_line(Z_list_meshed, xmin, xmax, ymin, ymax, zmin, zmax, tone)
    result = {
        "params": params,
        "data": {
            "energy": Z_list_meshed.tolist(),
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
            "zmin": zmin,
        },
    }
    # ** make data for contour line
    if contour_on:
        contours = get_contour_line(
            Z_list_meshed, xmin, xmax, ymin, ymax, zmin, zmax, tone
        )
        result["data"]["contours"] = {
            "contours": contours,
        }
    return result


@app.post("/api/write")
async def post_write(
    # file: Optional[bytes] = File(None),
    code: str = Form(...),
    resolution: float = Form(300),
    x: float = Form(-0.75),
    y: float = Form(0.55),
    tone: int = Form(20),
    check: int = Form(0),
    step: float = Form(0.01),
    xmin: float = Form(-2.5),
    xmax: float = Form(1.5),
    ymin: float = Form(-1),
    ymax: float = Form(3),
    zmin: float = Form(-147),
    zmax: float = Form(100),
    contour_on: bool = Form(False),
    optimize_on: bool = Form(False),
):
    print(code)

    params = {
        "code": code,
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
        "contour_on": contour_on,
        "optimize_on": optimize_on,
    }
    print("start")
    # ** make arrays for drawing pes
    X_list, Y_list, Z_list = create_pes_data_from_code(
        code, xmin, xmax, ymin, ymax, resolution
    )
    print("finish make arrays for pes")
    # ** convert arrays to mesh data array
    Z_list_meshed = get_meshgrid_from_xyzArray(X_list, Y_list, Z_list)
    print("finish convert arrays")
    result = {
        "params": params,
        "data": {
            "energy": Z_list_meshed.tolist(),
        },
    }
    # ** make data for contour line
    if contour_on:
        contours = get_contour_line(
            Z_list_meshed, xmin, xmax, ymin, ymax, zmin, zmax, tone
        )
        result["data"]["contours"] = {
            "contours": contours,
        }
        print("finish make contour")

    # ** make arrays for draw optimize line
    if optimize_on:
        (
            X1_list,
            Y1_list,
            X2_list,
            Y2_list,
            TS,
            EQ,
            count,
            Distance_list,
            Energy_list,
            TS_point,
        ) = make_data_from_code(code, x, y, check, step)
        result["data"]["optimizeLine"] = {
            "x1_list": X1_list,
            "y1_list": Y1_list,
            "x2_list": X2_list,
            "y2_list": Y2_list,
            "TS": TS,
            "EQ": EQ,
            "count": count,
            "Distance_list": Distance_list,
            "Energy_list": Energy_list,
            "TS_point": TS_point,
        }
        print("finish make arrays for draw optimize line")
    # print(result)

    return result


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
