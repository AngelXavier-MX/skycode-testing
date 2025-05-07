from locust import HttpUser, between, SequentialTaskSet, task


class UserBehavior(SequentialTaskSet):

    def on_start(self):
        """Login at the start of the test_files."""
        payload = {
            "mail_id": "divyasnpr02@gmail.com",
            "password": "Skylimit@123"
        }
        headers = {"Content-Type": "application/json"}

        response = self.client.post("/api/login/", json=payload, headers=headers, name="Login")
        print("Login Response Text:", response.text)
        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Cookies:", response.cookies)

        if response.status_code == 200:
            try:
                token = response.json().get("token")
                if token:
                    self.client.headers.update({
                        "Authorization": f"Bearer {token}"
                    })
                    print(" Token set successfully in headers.")
                else:
                    print(" No token found in login response.")
            except Exception as e:
                print(" Error parsing token:", e)
        else:
            print(" Login failed. Check credentials or server status.")

    @task
    def get_organizations(self):
        """Fetch list of organizations after login."""
        response = self.client.get("/custom_components/organizations/", name="Get Organizations")
        if response.status_code == 200:
            orgs = response.json()
            print("\nOrganizations List:")
            for org in orgs:
                print(f"- ID: {org['id']} | Name: {org['org_name']}")
        else:
            print(f" Failed to fetch organizations. Status: {response.status_code}")

    def on_stop(self):
        """Logout or cleanup (optional)."""
        print(" Test stopped for user. No /api/logout/ endpoint found.")
        # If your backend has a logout endpoint, use it here:
        # response = self.client.post("/api/logout/")
        # print("Logout Response:", response.status_code)


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [UserBehavior]
