from locust import HttpUser, task, between, TaskSet

class DashboardTasks(TaskSet):
    organization_id = 55

    @task
    def create_dashboard(self):
        dashboard_data = {

                "name": "Finance Dashboard",
                "usergroup": "182",
                "dashboard_type": "client_dashboard_1",
                "organization": 55,
                "dashboard_config": {
                    "cardOne": {
                        "label": "Finance",
                        "count": 10,
                        "value": "Approved",
                        "process_name": "finance_approval"
                    }
                }


        }

        headers = {
            "Content-Type": "application/json"
        }

        response = self.client.post(
            "/custom_components/dashboards/55/",
            json=dashboard_data,
            headers=headers,
            name="Create Dashboard"
        )
        print(f" Create Dashboard Status: {response.status_code}")
        print(f"Response: {response.text}")


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [DashboardTasks]
