from os import getenv
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel, Field, create_engine, Session, select

load_dotenv()

if getenv("DATABASE_URL") is None:
    raise ValueError("DATABASE_URL env var cannot be None")


class BaseTask(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

    @field_validator("title")
    def title_notna_formatted(cls, v: str):
        if not v:
            raise ValueError("Title cannot be None")
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip().capitalize()


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)


class CreateTask(BaseTask):
    pass


class UpdateTask(BaseTask):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


engine = create_engine(getenv("DATABASE_URL"))


def get_one_session():
    with Session(engine) as session:
        yield session


sessionDep = Annotated[Session, Depends(get_one_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(debug=True, lifespan=lifespan)


@app.post("/tasks/")
async def create_one_task(session: sessionDep, input_task: CreateTask) -> Task:
    task = Task.model_validate(input_task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/")
async def read_all_tasks(
    session: sessionDep, limit=Query(default=100, le=100), offset: int = 0
) -> list[Task]:
    tasks = session.exec(select(Task).limit(limit).offset(offset))
    return tasks


@app.get("/tasks/{id}")
async def read_one_task(session: sessionDep, id: int) -> Task:
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task id {id} is not available")
    return task


@app.patch("/tasks/{id}")
async def update_one_task(
    session: sessionDep, id: int, changed_fields: UpdateTask
) -> Task:
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task id {id} is not available")
    dump = changed_fields.model_dump(
        exclude_unset=True
    )  # didn't add "exclude_unset" from the beginning
    task.sqlmodel_update(dump)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{id}")
async def delete_one_task(session: sessionDep, id: int) -> dict:
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task id {id} is not available")
    session.delete(task)
    session.commit()
    return {"status": "ok"}
