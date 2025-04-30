from locust import HttpUser, task, between, SequentialTaskSet, TaskSet

class UserBehavior(SequentialTaskSet):
    @task
    def on_start(self):
        payload = {
            "mail_id": "divyasnpr02@gmail.com",
            "password": "Skylimit@123"
        }
        headers = {"Content-Type": "application/json"}

        response = self.client.post("/api/login/", json=payload, headers=headers, name="login")
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

    @task #no url like api/logout
    def on_stop(self):
        # Optional: Log out or perform cleanup when user stops
        try:
            response = self.client.post("/api/logout/")
            print("Logout response status:", response.status_code)
        except Exception as e:
            print("Error during logout:", e)

class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [UserBehavior]