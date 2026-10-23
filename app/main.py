from fastapi import FastAPI

app = FastAPI(title="Учебный проект FastAPI")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Привет, FastAPI!"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
