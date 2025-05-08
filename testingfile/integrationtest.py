from locust import HttpUser, task, between, TaskSet


class RpaTasks(TaskSet):
    # 3. List APIs
    @task
    def list_apis(self):
        response = self.client.get(
            "/custom_components/integrations/55/",
            headers={"Content-Type": "application/json"},
            name="List APIs"
        )

        print(" List APIs Status:", response.status_code)
        print(" Response:", response.text)

        # Check if a specific integration exists
    @task
    def check_integration_exists(self):
            response = self.client.get("/custom_components/integrations/55/", name="Check Integrations")

            if response.status_code == 200:
                try:
                    data = response.json()  # Parse JSON list of integrations
                    integration_names = [item["integration_name"] for item in data]
                    target_integration = "loginAPI"  # Change to your target

                    if target_integration in integration_names:
                        print(f" Integration '{target_integration}' exists.")
                    else:
                        print(f" Integration '{target_integration}' not found.")
                except Exception as e:
                    print(" Error parsing integration response:", str(e))
            else:
                print(f" Failed to fetch integrations. Status code: {response.status_code}")

    @task
    def create_new_integration(self):
        integration_data = {
            "integration_name": "skycode new login",
            "description": "login new",
            "integration_type": "api",
            "organization": "55",
            "integration_schema": {
                "base_url": {
                    "base": "http://13.235.34.196",
                    "endpoint": "/custom_components/execute-api/"
                },
                "method": "POST",
                "headers": [
                    {
                        "header_key": "",
                        "header_value": "",
                        "header_type": "static",
                        "header_source": ""
                    }
                ],
                "auth": {
                    "type": "none",
                    "basic": {
                        "username": "",
                        "password": ""
                    },
                    "bearer": {
                        "token": ""
                    },
                    "api_key": {
                        "key": "",
                        "value": "",
                        "add_to": ""
                    }
                },
                "body": {
                    "contentType": "json",
                    "payload": [
                        {
                            "key": "username",
                            "value": "test_user",
                            "type": "static"
                        },
                        {
                            "key": "password",
                            "value": "test_pass",
                            "type": "static"
                        }
                    ]
                },
                "api_response": [
                    {
                        "access_path": "",
                        "response_key": ""
                    }
                ]
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = self.client.post(
            "/custom_components/integrations/55/",
            json=integration_data,
            headers=headers,
            name="Create Integration"
        )

        print("🚀 Create Integration Status:", response.status_code)
        print("🚀 Response:", response.text)

    @task
    def update_integration(self):
        integration_id = 71  # Replace with the actual integration ID to update

        updated_data = {
            "integration_name": "skycode login - updated",
            "description": "login flow updated",
            "integration_type": "api",
            "organization": "55",
            "integration_schema": {
                "base_url": {
                    "base": "http://13.235.34.196",
                    "endpoint": "/custom_components/execute-api/"
                },
                "method": "POST",
                "headers": [
                    {
                        "header_key": "Content-Type",
                        "header_value": "application/json",
                        "header_type": "static",
                        "header_source": ""
                    }
                ],
                "auth": {
                    "type": "none",
                    "basic": {
                        "username": "",
                        "password": ""
                    },
                    "bearer": {
                        "token": ""
                    },
                    "api_key": {
                        "key": "",
                        "value": "",
                        "add_to": ""
                    }
                },
                "body": {
                    "contentType": "json",
                    "payload": [
                        {
                            "key": "username",
                            "value": "updated_user",
                            "type": "static"
                        },
                        {
                            "key": "password",
                            "value": "updated_pass",
                            "type": "static"
                        }
                    ]
                },
                "api_response": [
                    {
                        "access_path": "",
                        "response_key": ""
                    }
                ]
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = self.client.put(
            f"/custom_components/integrations/55/{integration_id}/",
            json=updated_data,
            headers=headers,
            name=f"Update Integration {integration_id}"
        )

        print(f"🔄 Update Integration ID {integration_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"  # Update if needed
    tasks = [RpaTasks]