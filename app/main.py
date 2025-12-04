from fastapi import FastAPI

# Create an instance of the FastAPI application
app = FastAPI()

# create api test
@app.get("/")
def read_root():
  return {"Hello": "World"}
