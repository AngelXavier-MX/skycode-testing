from locust import HttpUser, task, between, TaskSet


class FormCoreTasks(TaskSet):
    @task
    def update_form(self):
        form_id = 1346  # Replace with the actual form ID
        updated_data = {
            "form_name": "course form updated",
            "form_description": "Updated Description",
            "organization": 55,
            "form_json_schema": [],
            "form_style_schema": [],
            "form_rule_schema": [],
            "permissions": [],
            "core_table": True
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = self.client.put(
                f"/create_form/organization/55/{form_id}/",
                json=updated_data,
                headers=headers,
                name=f"Update Form {form_id}"
            )

            print(f"\n🔁 Updating Form ID {form_id}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code in [200, 202]:
                print(f"✅ Successfully updated form {form_id}")
            elif response.status_code == 405:
                print(f"❌ Update method not allowed for Form ID {form_id} (405)")
            else:
                print(f"❌ Failed to update form {form_id}")

        except Exception as e:
            print(f"❗ Exception occurred while updating form: {e}")


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [FormCoreTasks]
