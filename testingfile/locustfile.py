from locust import HttpUser, task, between,SequentialTaskSet

class UserBehavior(SequentialTaskSet):
    @task
    def login(self):
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
            try:
                # Try to extract a token if present
                token = response.json().get("token")
                if token:
                    # If token exists, set it in Authorization header
                    self.client.headers.update({
                        "Authorization": f"Bearer {token}"
                    })
                    print("Token set successfully in headers.")
                else:
                    print("No token found in login response.")
            except Exception as e:
                print("Error parsing token:", e)


    @task
    def organization(self):
        self.client.get("/custom_components/organizations/", name="organizations")

    @task
    def form_data(self):
        self.client.get("/core-data/55/", name="form_coredata")

    @task
    def user_groups(self):
        self.client.get("/custom_components/organizations/55/usergroups/", name="user_groups")
    @task
    def submit_form(self):
        form_data ={
                "form_json_schema": [],
                "form_name": "Leave form",
                "form_description": "Attendance Process",
                "organization": 55,
                "permissions": [],
                "form_style_schema": [],
                "form_rule_schema": [],
                "core_table": False
            }
            # Example, depends on API
            # Add other fields based on what your backend expects
        headers = {
            "Content-Type": "application/json",
        }
        self.client.post(
            "http://13.235.34.196/create_form/",
            json=form_data,
            headers=headers,
            name="Submit Core Data Form"
        )

# Define user class and host (backend API URL)
class MyUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between user actions
    host = "http://13.235.34.196"  # Backend API base URL
    tasks = [UserBehavior]