"""TheFROGtask streamlit app

That's a one-page task management app that shows the tasks from the API_URL. 
Functionality:
1. Creates, updates (minimally), deletes, and shows tasks
2. Validates the input data (task title, description)
3. Has display options for tasks: (not completed tasks only or all) (what is the limit of shown tasks)

Version: 1.0.0
Author: Abdulrahman Wael
Date: 6 Jan 2026
"""

from os import getenv
from dotenv import load_dotenv
import streamlit as st
import requests as rq

load_dotenv()

st.set_page_config(page_icon="👌", page_title="theFROGtask")

with st.sidebar:
    """Page sidebar (input data)

    this sidebar accepts data in order to create one task: (title, description) .. after this ID is automatically created (of the last created ID +1) and completed is set to False.
    """
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
                f"{getenv('API_URL')}/tasks/",
                json={"title": title_input, "description": description_area},
            )
            if request.status_code == 200:
                st.success(
                    f"Task with ID {request.json()['id']} is successfully created"
                )

st.title("Eat that frog!")
col1, col2 = st.columns([2, 1])
with col1:
    """ Limit slider

    This limits the shown tasks to a specific number and it can be changed easily with the slider.
    """
    limit = st.slider("displyed tasks limit", min_value=5, max_value=100, value=20)
with col2:
    """ show completed tasks Checkbox

    Checked = show all tasks including completed ones ... and the opposite is true.
    """
    show_completed = st.checkbox("show completed tasks", value=False)

all_tasks = rq.get(f"{getenv('API_URL')}/tasks/").json()
for task in all_tasks:
    """ main page logic

    for each task in the database check if it's completed or not to know if it will be displayed or not ... 
    then display the attributes or the task using an expander which shows the ID, completion_status, title outside 
    and have description text, toggle_completed button, and delete button inside.
    """
    if task["completed"] and not show_completed:
        continue
    with st.expander(
        f"[ {task['id']} ] {task['title']}",
        icon=f"{'👌' if task['completed'] else '❄️'}",
    ):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            description_area = st.write(
                f"{task['description'] if task['description'] else 'nothing special.'}"
            )
        with col2:
            task_checkbox = st.button(
                f"{'Done!' if not task['completed'] else 'Not done yet!'}",
                key=f"toggle_task_{task['id']}",
            )
            if task_checkbox:
                update_request = rq.patch(
                    url=f"{getenv('API_URL')}/tasks/{task['id']}",
                    json={"completed": not task["completed"]},
                )
                print(update_request.json()["id"])
                if update_request.status_code == 200:
                    st.rerun()
        with col3:
            delete_button = st.button("delete", key=f"delete_task_{task['id']}")
            if delete_button:
                delete_request = rq.delete(f"{getenv('API_URL')}/tasks/{task['id']}")
                if delete_request.status_code == 200:
                    st.rerun()
