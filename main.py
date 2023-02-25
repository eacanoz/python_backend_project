from fastapi import FastAPI

app = FastAPI()

# First line code.
@app.get("/")
def root():
    return "Main page"