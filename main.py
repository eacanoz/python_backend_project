from fastapi import FastAPI
from routers import myProfile

app = FastAPI()

# Add routers
app.include_router(myProfile.router)


# First line code.
@app.get("/")
def root():
    return "Main page"