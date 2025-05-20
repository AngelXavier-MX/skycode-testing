from locust import HttpUser, task, between

class SkycodeRpaPreview(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"  # Change to your server IP if needed

    @task
    def trigger_preview(self):
        payload = {
            "config": {
                "input_data": [{}],
                "schema_config": [
                    {
                        "url": "https://www.flipkart.com/",
                        "forms": [
                            {
                                "form_value": [],
                                "form_element_details": [
                                    {
                                        "efield_id": "login",
                                        "evalue": "//*[@id=\"container\"]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div/header/div[2]/div[2]/div/div/div/div/a",
                                        "evalue_type": "XPATH",
                                        "eaction": "click",
                                        "ewait": False,
                                        "eskip": False
                                    }
                                ]
                            }
                        ],
                        "form_status": [
                            {
                                "initialized": "False",
                                "navigated": "False",
                                "updated": "False",
                                "closed": "False",
                                "error": "None",
                                "processed_forms_count": 0
                            }
                        ]
                    }
                ]
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = self.client.post("/start-rpa", json=payload, headers=headers, name="Skycode RPA Preview")
        print("Status:", response.status_code)
        print("Response:", response.text)
