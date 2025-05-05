from locust import HttpUser, task, between, TaskSet

class UserGroupTasks(TaskSet):
    # retrieve groups existing
    @task
    def user_group(self):
        # Send a GET request using Locust's client
        response = self.client.get("/custom_components/organizations/55/usergroups/", name="User Group List")

        if response.status_code == 200:
            groups = response.json()
            print("User Groups:\n")
            for group in groups:
                print(f"ID: {group['id']}")
                print(f"Name: {group['group_name']}")
                print(f"Description: {group['group_description']}\n")
        else:
            print(f" Failed to fetch groups. Status Code: {response.status_code}")
    #create new group
    @task
    def user_form(self):
        form_data = {
            "group_name": "advertising",
            "group_description": "monitoring all the worker and works",
            "status": True,
            "organization": "55"
        }

        headers = {
            "Content-Type": "application/json"
        }

        self.client.post(
            "/custom_components/user-groups/",
            json=form_data,
            headers=headers,
            name="Create User Group"
        )
    #check if group exist
    @task
    def check_user_group_exists(self):
        # Replace this with your actual endpoint
        response = self.client.get("/custom_components/organizations/55/usergroups/", name="Check User Groups")

        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            group_names = [group["group_name"] for group in data]
            target_group = "manager"

            if target_group in group_names:
                print(f" Group '{target_group}' exists.")
            else:
                print(f" Group '{target_group}' not found.")
        else:
            print(f" Failed to fetch user groups. Status code: {response.status_code}")
    #update user group
    @task
    def update_user_group(self):
        group_id = 217  # Change this to the ID of the group you want to update
        updated_data = {
            "group_name": "monitor-updated",
            "group_description": "Updated description for monitor group",
            "status": True,
            "organization": "55"
        }

        headers = {
            "Content-Type": "application/json",
            # "Authorization": "Bearer <your_token>"  # Uncomment and update if auth is required
        }

        response = self.client.patch(
            f"/custom_components/organizations/55/usergroups/226/",
            json=updated_data,
            headers=headers,
            name=f"Update Group {group_id}"
        )

        print(f" Updating Group ID {group_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code in [200, 202]:
            print(f" Successfully updated group {group_id}")
        else:
            print(f" Failed to update group {group_id}")


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [UserGroupTasks]
