from locust import HttpUser, task, between, TaskSet


class FormCoreTasks(TaskSet):

    # 1. Retrieve existing forms
    @task
    def get_forms(self):
        response = self.client.get("/core-data/55/", name="Form List")

        if response.status_code == 200:
            forms = response.json()
            print("\n--- Existing Forms ---")
            for form in forms:
                print(f"ID: {form.get('id')}")
                print(f"Name: {form.get('form_name')}")
                print(f"Description: {form.get('form_description')}\n")
        else:
            print(f" Failed to fetch forms. Status Code: {response.status_code}")

    # 2. Create a new form
    @task
    def create_form(self):
        form_data = {
            "form_name": "employee info form",
            "form_description": "employee personal details",
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

        response = self.client.post(
            "/create_form/",
            json=form_data,
            headers=headers,
            name="Create Core Form"
        )
        print(f" Create Form Status: {response.status_code}")
        print(f"Response: {response.text}")

    # 3. Check if a specific form exists
    @task
    def check_form_exists(self):
        response = self.client.get("/core-data/55/", name="Check Form Exists")

        if response.status_code == 200:
            forms = response.json()
            target_form = "leave form"
            form_names = [form.get("form_name") for form in forms]

            if target_form in form_names:
                print(f" Form '{target_form}' exists.")
            else:
                print(f" Form '{target_form}' not found.")
        else:
            print(f" Failed to check forms. Status Code: {response.status_code}")

    # 4. Update a form (optional, ID must be known)
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

            print(f"\n Updating Form ID {form_id}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code in [200, 202]:
                print(f" Successfully updated form {form_id}")
            elif response.status_code == 405:
                print(f" Update method not allowed for Form ID {form_id} (405)")
            else:
                print(f" Failed to update form {form_id}")

        except Exception as e:
            print(f" Exception occurred while updating form: {e}")


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [FormCoreTasks]
