from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from routers import design, ai, storage
from ai import OpenAI, AzureOpenAI
from ai.Azure import Gpt4omini, Gpt4o

app = FastAPI()

# Router 등록
app.include_router(design.router)
app.include_router(ai.router)
app.include_router(storage.router)

# 정적파일 등록
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/api-test", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name="App/ai/00-api-test.html", 
                                      context={
                                          "request": request, 
                                          "category": "AI", 
                                          "submenu":"api test",
                                          "title": "AI", 
                                          "subtitle" : "API TEST"
                                          })

@app.get("/open-ai", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name="App/ai/01-open-ai.html", 
                                      context={
                                          "request": request, 
                                          "category": "AI", 
                                          "submenu":"open ai",
                                          "title": "AI", 
                                          "subtitle" : "Open AI"
                                          })

@app.get("/azure-open-ai", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name="App/ai/02-azure-open-ai.html", 
                                      context={
                                          "request": request, 
                                          "category": "AI", 
                                          "submenu":"azure open ai",
                                          "title": "AI", 
                                          "subtitle" : "Azure Open AI"
                                          })

@app.get("/azure-ai-search", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name="App/ai/03-azure-ai-search.html", 
                                      context={
                                          "request": request, 
                                          "category": "AI", 
                                          "submenu":"azure ai search",
                                          "title": "AI", 
                                          "subtitle" : "Azure AI Search"
                                          })

# --------------------------------------------- #

@app.get("/base", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name="App/base.html", context={"request": request, "title": "test"})

@app.get("/index", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name="App/index.html", context={"request": request, "title": "Dashboard", "subtitle" : "Control panel"})

@app.get("/index2", response_class=HTMLResponse)
def index2(request: Request):
    return templates.TemplateResponse(name="App/index2.html", context={"request": request, "title": "Dashboard2", "subtitle" : "Control panel"})


# Layout Option
@app.get("/pages/layout/top-nav", response_class=HTMLResponse)
def topnav(request: Request):
    return templates.TemplateResponse(name="App/pages/layout/top-nav.html", context={"request": request, "title": "Top Navigation","subtitle" : "Example 2.0"})

@app.get("/pages/layout/boxed", response_class=HTMLResponse)
def boxed(request: Request):
    return templates.TemplateResponse(name="App/pages/layout/boxed.html", context={"request": request, "title": "Boxed Layout","subtitle" : "Blank example to the boxed layout"})

@app.get("/pages/layout/fixed", response_class=HTMLResponse)
def fixed(request: Request):
    return templates.TemplateResponse(name="App/pages/layout/fixed.html", context={"request": request, "title": "Fixed Layout","subtitle" : "Blank example to the fixed layout"})

@app.get("/pages/layout/collapsed-sidebar", response_class=HTMLResponse)
def collapsedsidebar(request: Request):
    return templates.TemplateResponse(name="App/pages/layout/collapsed-sidebar.html", context={"request": request, "title": "Sidebar Collapsed","subtitle" : "Layout with collapsed sidebar on load"})


# Widgets
@app.get("/pages/widgets", response_class=HTMLResponse)
def widgets(request: Request):
    return templates.TemplateResponse(name="App/pages/widgets.html", context={"request": request, "title": "Widgets","subtitle" : "Preview page"})


# Charts
@app.get("/pages/charts/chartjs", response_class=HTMLResponse)
def widgets(request: Request):
    return templates.TemplateResponse(name="App/pages/charts/chartjs.html", context={"request": request, "title": "ChartJS","subtitle" : "Preview sample"})
@app.get("/pages/charts/morris", response_class=HTMLResponse)
def morris(request: Request):
    return templates.TemplateResponse(name="App/pages/charts/morris.html", context={"request": request, "title": "Morris Charts","subtitle" : "Preview sample"})
@app.get("/pages/charts/flot", response_class=HTMLResponse)
def flot(request: Request):
    return templates.TemplateResponse(name="App/pages/charts/flot.html", context={"request": request, "title": "Flot Charts","subtitle" : "Preview sample"})
@app.get("/pages/charts/inline", response_class=HTMLResponse)
def inline(request: Request):
    return templates.TemplateResponse(name="App/pages/charts/inline.html", context={"request": request, "title": "Inline Charts","subtitle" : "multiple types of charts"})


# UI Elements
@app.get("/pages/UI/general", response_class=HTMLResponse)
def general(request: Request):
    return templates.TemplateResponse(name="App/pages/UI/general.html", context={"request": request, "title": "General UI","subtitle" : "Preview of UI elements"})

@app.get("/pages/UI/icons", response_class=HTMLResponse)
def icons(request: Request):
    return templates.TemplateResponse(name="App/pages/UI/icons.html", context={"request": request, "title": "Icons","subtitle" : "a set of beautiful icons"})

@app.get("/pages/UI/buttons", response_class=HTMLResponse)
def buttons(request: Request):
    return templates.TemplateResponse(name="App/pages/UI/buttons.html", context={"request": request, "title": "Buttons","subtitle" : "Control panel"})

@app.get("/pages/UI/sliders", response_class=HTMLResponse)
def sliders(request: Request):
    return templates.TemplateResponse(name="App/pages/UI/sliders.html", context={"request": request, "title": "Sliders","subtitle" : "range sliders"})

@app.get("/pages/UI/timeline", response_class=HTMLResponse)
def timeline(request: Request):
    return templates.TemplateResponse(name="App/pages/UI/timeline.html", context={"request": request, "title": "Timeline","subtitle" : "example"})

@app.get("/pages/UI/modals", response_class=HTMLResponse)
def modals(request: Request):
    return templates.TemplateResponse(name="App/pages/UI/modals.html", context={"request": request, "title": "Modals","subtitle" : "new"})

# Forms
@app.get("/pages/forms/general", response_class=HTMLResponse)
def general2(request: Request):
    return templates.TemplateResponse(name="App/pages/forms/general.html", context={"request": request, "title": "General Form Elements","subtitle" : "Preview"})

@app.get("/pages/forms/advanced", response_class=HTMLResponse)
def advanced(request: Request):
    return templates.TemplateResponse(name="App/pages/forms/advanced.html", context={"request": request, "title": "Advanced Form Elements","subtitle" : "Preview"})

@app.get("/pages/forms/editors", response_class=HTMLResponse)
def editors(request: Request):
    return templates.TemplateResponse(name="App/pages/forms/editors.html", context={"request": request, "title": "Text Editors","subtitle" : "Advanced form element"})


# Tables
@app.get("/pages/tables/simple", response_class=HTMLResponse)
def simple(request: Request):
    return templates.TemplateResponse(name="App/pages/tables/simple.html", context={"request": request, "title": "Simple Tables","subtitle" : "preview of simple tables"})

@app.get("/pages/tables/data", response_class=HTMLResponse)
def editors(request: Request):
    return templates.TemplateResponse(name="App/pages/tables/data.html", context={"request": request, "title": "Data Tables","subtitle" : "advanced tables"})


# Calandar
@app.get("/pages/calendar", response_class=HTMLResponse)
def calendar(request: Request):
    return templates.TemplateResponse(name="App/pages/calendar.html", context={"request": request, "title": "Calendar","subtitle" : "Control panel"})

# Mailbox
@app.get("/pages/mailbox/mailbox", response_class=HTMLResponse)
def mailbox(request: Request):
    return templates.TemplateResponse(name="App/pages/mailbox/mailbox.html", context={"request": request, "title": "Mailbox","subtitle" : "13 new messages"})
@app.get("/pages/mailbox/read-mail", response_class=HTMLResponse)
def read_mail(request: Request):
    return templates.TemplateResponse(name="App/pages/mailbox/read-mail.html", context={"request": request, "title": "Read Mail","subtitle" : ""})
@app.get("/pages/mailbox/compose", response_class=HTMLResponse)
def compose(request: Request):
    return templates.TemplateResponse(name="App/pages/mailbox/compose.html", context={"request": request, "title": "Compose Mail","subtitle" : "13 new messages"})

# Examples
@app.get("/pages/examples/invoice", response_class=HTMLResponse)
def invoice(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/invoice.html", context={"request": request, "title": "Invoice","subtitle" : "#007612"})

@app.get("/pages/examples/invoice-print", response_class=HTMLResponse)
def invoice_print(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/invoice-print.html", context={"request": request, "title": "","subtitle" : ""})

@app.get("/pages/examples/profile", response_class=HTMLResponse)
def profile(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/profile.html", context={"request": request, "title": "User Profile","subtitle" : ""})

@app.get("/pages/examples/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/login.html", context={"request": request, "title": "login","subtitle" : ""})

@app.get("/pages/examples/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/register.html", context={"request": request, "title": "register","subtitle" : ""})

@app.get("/pages/examples/lockscreen", response_class=HTMLResponse)
def lockscreen(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/lockscreen.html", context={"request": request, "title": "lockscreen","subtitle" : ""})

@app.get("/pages/examples/404", response_class=HTMLResponse)
def error404(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/404.html", context={"request": request, "title": "404 Error Page","subtitle" : ""})

@app.get("/pages/examples/500", response_class=HTMLResponse)
def error500(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/500.html", context={"request": request, "title": "500 Error Page","subtitle" : ""})

@app.get("/pages/examples/blank", response_class=HTMLResponse)
def blank(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/blank.html", context={"request": request, "title": "Blank page","subtitle" : "it all starts here"})

@app.get("/pages/examples/pace", response_class=HTMLResponse)
def pace(request: Request):
    return templates.TemplateResponse(name="App/pages/examples/pace.html", context={"request": request, "title": "Pace page","subtitle" : "Loading example"})


# Multilevel


# Documentation
@app.get("/documentation/index", response_class=HTMLResponse)
def documantation(request: Request):
    return templates.TemplateResponse(name="App/documentation/index.html", context={"request": request, "title": "AdminLTE Documentation","subtitle" : "Version 2.3"})