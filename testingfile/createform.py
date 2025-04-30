from locust import HttpUser, task, between, SequentialTaskSet, TaskSet

# Define a TaskSet for form and organization tasks
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

# Main UserBehavior class for login only
class UserBehavior(SequentialTaskSet):
    def on_start(self):
        payload = {
            "mail_id": "divyasnpr02@gmail.com",
            "password": "Skylimit@123"
        }
        headers = {"Content-Type": "application/json"}

        response = self.client.post("/api/login/", json=payload, headers=headers)
        print(response.text)
        print(response.status_code)
        print(response.headers)
        print(response.cookies)

        if response.status_code == 200:
            self.client.get("/custom_components/organizations/", name="organizations")
            try:
                token = response.json().get("token")
                if token:
                    self.client.headers.update({
                        "Authorization": f"Bearer {token}"
                    })
                    print("Token set successfully in headers.")
                else:
                    print("No token found in login response.")
            except Exception as e:
                print("Error parsing token:", e)
        else:
            print("Login failed. Check credentials or server status.")

    @task
    def form_core_data_flow(self):
        # Run the form and organization tasks
        self.schedule_task(FormCoreDataTasks)
    @task
    def on_stop(self):
        # Optional: Log out or perform cleanup when user stops
        try:
            response = self.client.post("/api/logout/")
            print("Logout response status:", response.status_code)
        except Exception as e:
            print("Error during logout:", e)

# Define the User
class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [UserBehavior]
