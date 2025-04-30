from locust import HttpUser, task, between, SequentialTaskSet, TaskSet

class FormCoreDataTasks(TaskSet):
    @task
    def form_data(self):
        self.client.get("/create_form/organization/55/", name="create_form")
        self.client.get("/core-data/55/", name="forms_list")

    @task
    def submit_form(self):
        form_data = {
            "form_json_schema": [],
            "form_name": "Leave form",
            "form_description": "Attendance Process",
            "organization": 55,
            "permissions": [],
            "form_style_schema": [],
            "form_rule_schema": [],
            "core_table": False
        }
        headers = {
            "Content-Type": "application/json",
        }
        self.client.post(
            "/create_form/",
            json=form_data,
            headers=headers,
            name="Submit Core Data Form"
        )

class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [FormCoreDataTasks]