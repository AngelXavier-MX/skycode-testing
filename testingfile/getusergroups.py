from locust import HttpUser, task, between, TaskSet


class RpaTasks(TaskSet):

    # update user group
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
    tasks = [RpaTasks]
