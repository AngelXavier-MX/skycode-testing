from locust import HttpUser, task, between, TaskSet


class DashboardTasks(TaskSet):

    organization_id = 55

    # 1. Retrieve existing dashboards
    @task
    def get_dashboards(self):
        response = self.client.get(f"/custom_components/dashboards/55/", name="Dashboard List")

        if response.status_code == 200:
            dashboards = response.json()
            print("\n--- Existing Dashboards ---")
            for dash in dashboards:
                print(f"id: {dash.get('id')}")
                print(f"Name: {dash.get('name')}")
                print(f"Group: {dash.get('usergroup')}")
                print(f"Type: {dash.get('dashboard_types')}\n")

        else:
            print(f" Failed to fetch dashboards. Status Code: {response.status_code}")
    # 2. Create a new dashboard configuration
    @task
    def create_dashboard(self):
        dashboard_data = {
            "name": "Finance Dashboard",
            "usergroup": "182",
            "dashboard_type": "client_dashboard_1",
            "organization": self.organization_id
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

    # 3. Check if a specific dashboard exists
    @task
    def check_dashboard_exists(self):
        response = self.client.get(f"/custom_components/dashboards/55/", name="Check Dashboard Exists")

        if response.status_code == 200:
            dashboards = response.json()
            target_dashboard = "vendors"
            dash_names = [dash.get("name") for dash in dashboards]

            if target_dashboard in dash_names:
                print(f" Dashboard '{target_dashboard}' exists.")
            else:
                print(f" Dashboard '{target_dashboard}' not found.")
        else:
            print(f" Failed to check dashboards. Status Code: {response.status_code}")
    #4. update existing dashboard
    @task
    def update_dashboard(self):
        dashboard_id = 26  # The ID you want to update

        updated_data = {
            "name": "Updated Vendor Dashboard",
            "group_name": "Vendor / Supplier",
            "dashboard_types": "client_dashboard_1",
            "organization": self.organization_id,
            "usergroup": 173,  # Replace with valid group ID if needed
            "dashboard_config": {
                "cardOne": {
                    "label": "Vendors",
                    "count": "12",
                    "value": "Approved",
                    "process_name": "vendor_approval"
                }
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = self.client.put(
                f"/custom_components/dashboards/{self.organization_id}/{dashboard_id}/",
                json=updated_data,
                headers=headers,
                name=f"Update Dashboard {dashboard_id}"
            )

            print(f"\n Updating Dashboard ID {dashboard_id}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

        except Exception as e:
            print(f" Exception while updating dashboard: {e}")


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [DashboardTasks]
