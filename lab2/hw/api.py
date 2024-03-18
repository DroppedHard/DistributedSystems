from fastapi import FastAPI, status, Request
from typing import Union
from services.FOaaS import FOaaS
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from urllib.parse import unquote
from services.profanityFilter import ProfanityFilterAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

origins = ["http://localhost:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def isUrlGood(url: str) -> bool:
    temp = url.split("/")
    for i in temp:
        if not i:
            return False
    return True


@app.get("/foaas", response_class=HTMLResponse)
async def get_foass(
    url: str,
    filterProfanity: bool,
    req: Request,
    APIKey: Union[str, None] = None,
):
    try:
        url = unquote(url)
        if not isUrlGood(url):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content="Please provide data in input fields",
            )
        if filterProfanity:
            if APIKey:
                json_content = FOaaS.getFOaaSEndpoint(url)
                message = ProfanityFilterAPI.getFilteredMessage(
                    json_content.get("message"), APIKey
                )
                return templates.TemplateResponse(
                    "out.html",
                    {
                        "request": req,
                        "message": message,
                        "subtitle": json_content.get("subtitle"),
                    },
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content="Ninja API key not provided, which is required to filter profanity",
                )
        else:
            json_content = FOaaS.getFOaaSEndpoint(url)
            return templates.TemplateResponse(
                "out.html",
                {
                    "request": req,
                    "message": json_content.get("message"),
                    "subtitle": json_content.get("subtitle"),
                },
            )
            # return html_content
    except Exception as e:
        print(f"An error occured: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=f"An error occurred while processing the request: {e}",
        )


@app.get("/foaas/endpoints")
async def get_foass_endpoints():
    return FOaaS.getOperations()
