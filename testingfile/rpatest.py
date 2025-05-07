from locust import HttpUser, task, between, TaskSet


class RpaTasks(TaskSet):

    # 1. Retrieve existing rpa forms
    @task
    def get_forms(self):
        response = self.client.get("/custom_components/bots/55/", name="rpa List")

        if response.status_code == 200:
            rpa = response.json()
            print("\n--- Existing Rpa's ---")
            for rpa in rpa:
                print(f"ID: {rpa.get('id')}")
                print(f"Name: {rpa.get('name')}")
                print(f"Description: {rpa.get('bot_description')}\n")
        else:
            print(f" Failed to fetch forms. Status Code: {response.status_code}")

    #2.check if exist
    # check if group exist
    @task
    def check_user_group_exists(self):
        # Replace this with your actual endpoint
        response = self.client.get("/custom_components/bots/55/", name="Check User Groups")

        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            rpa_names = [rpa["name"] for rpa in data]
            target_rpa = "skycode"

            if target_rpa in rpa_names:
                print(f" Group '{target_rpa}' exists.")
            else:
                print(f" Group '{target_rpa}' not found.")
        else:
            print(f" Failed to fetch user groups. Status code: {response.status_code}")


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [RpaTasks]
