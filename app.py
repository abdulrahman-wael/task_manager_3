from os import getenv
from dotenv import load_dotenv
import streamlit as st
import requests as rq

load_dotenv()

st.set_page_config(page_icon="👌", page_title="theFROGtask")

with st.sidebar:
    title_input = st.text_input(
        label="Title", max_chars=200, placeholder="what do you want?"
    )
    description_area = st.text_area(
        label="Description", placeholder="write any details ..."
    )
    submit = st.button(type="primary", label="create")
    if submit:
        if not title_input.strip():
            st.error("Title cannot be empty")
        else:
            request = rq.post(
                getenv("API_URL"),
                json={"title": title_input, "description": description_area},
            )
            if request.status_code == 200:
                st.success(
                    f"Task with ID {request.json()["id"]} is successfully created"
                )

st.title("FROGGY MORNING!")
col1, col2 = st.columns([2, 1])
with col1:
    limit = st.slider("displyed tasks limit", min_value=5, max_value=100, value=20)
with col2:
    show_completed = st.checkbox("show completed tasks", value=False)

all_tasks = rq.get(getenv("API_URL")).json()
for task in all_tasks:
    if task["completed"] and not show_completed:
        continue
    with st.expander(
        f"[ {task["id"]} ] {task['title']}",
        icon=f"{'👌' if task['completed'] else '❄️'}",
    ):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            description_area = st.write(
                f"{task['description'] if task['description'] else "nothing special."}"
            )
        with col2:
            task_checkbox = st.button(
                f"{"Done!" if not task["completed"] else "Not done yet!"}",
                key=f"toggle_task_{task['id']}",
            )
            if task_checkbox:
                update_request = rq.patch(
                    url=f"{getenv('API_URL')}{task['id']}",
                    json={"completed": not task["completed"]},
                )
                print(update_request.json()["id"])
                if update_request.status_code == 200:
                    st.rerun()
        with col3:
            delete_button = st.button("delete", key=f"delete_task_{task['id']}")
            if delete_button:
                delete_request = rq.delete(f"{getenv('API_URL')}{task['id']}")
                if delete_request.status_code == 200:
                    st.rerun()
