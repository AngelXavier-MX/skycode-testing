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

    #create rpa
    @task
    def create_rpa_bot(self):
            # Headers for the request
            headers = {
                "Content-Type": "application/json"
            }

            # Payload to create the RPA bot
            rpa_payload = {
                "name": "skycode test",
                "bot_name": "screen_scraping",
                "bot_description": "automate the process of skycode",
                "bot_uid": None,
                "bot_schema_json": {
                    "url": "http://skycode-studio-qa.s3-website.ap-south-1.amazonaws.com/auth/login",
                    "forms": [
                        {
                            "form_value": [
                                {
                                    "field_id": "username",
                                    "value": "infinitesys@gmail.com",
                                    "value_type": "value"
                                },
                                {
                                    "field_id": "password",
                                    "value": "Password@123",
                                    "value_type": "value"
                                }
                            ],
                            "form_element_details": [
                                {
                                    "efield_id": "username",
                                    "evalue": "//*[@id=\"root\"]/div/main/div/div[2]/div[3]/form/div/div[3]/div[1]/div[2]/input",
                                    "evalue_type": "XPATH",
                                    "eaction": "send_keys",
                                    "ewait": False,
                                    "eskip": False
                                },
                                {
                                    "efield_id": "password",
                                    "evalue": "//*[@id=\"root\"]/div/main/div/div[2]/div[3]/form/div/div[3]/div[2]/div[2]/input",
                                    "evalue_type": "XPATH",
                                    "eaction": "send_keys",
                                    "ewait": False,
                                    "eskip": False
                                },
                                {
                                    "efield_id": "login",
                                    "evalue": "//*[@id=\"root\"]/div/main/div/div[2]/div[3]/form/div/div[4]/button/div",
                                    "evalue_type": "XPATH",
                                    "eaction": "click",
                                    "ewait": False,
                                    "eskip": False
                                }
                            ]
                        },
                        {
                            "form_value": [],
                            "form_element_details": [
                                {
                                    "efield_id": "",
                                    "evalue": "//*[@id=\"root\"]/div/main/div/section/div[1]/div[2]/button",
                                    "evalue_type": "XPATH",
                                    "eaction": "click",
                                    "ewait": False,
                                    "eskip": False
                                }
                            ]
                        },
                        {
                            "form_value": [],
                            "form_element_details": [
                                {
                                    "efield_id": "",
                                    "evalue": "//*[@id=\"root\"]/div/main/div/div[2]/div[1]/button",
                                    "evalue_type": "XPATH",
                                    "eaction": "click",
                                    "ewait": False,
                                    "eskip": False
                                }
                            ]
                        },
                        {
                            "form_value": [
                                {
                                    "field_id": "Name",
                                    "value": "leave form",
                                    "value_type": "value"
                                },
                                {
                                    "field_id": "description",
                                    "value": "Attendance purpose",
                                    "value_type": "value"
                                }
                            ],
                            "form_element_details": [
                                {
                                    "efield_id": "Name",
                                    "evalue": "/html/body/div/div/main/div/div[3]/div[1]/div[1]/div[1]/input",
                                    "evalue_type": "XPATH",
                                    "eaction": "send_keys",
                                    "ewait": False,
                                    "eskip": False
                                },
                                {
                                    "efield_id": "description",
                                    "evalue": "/html/body/div/div/main/div/div[3]/div[1]/div[1]/div[2]/textarea",
                                    "evalue_type": "XPATH",
                                    "eaction": "send_keys",
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
            }

            # API call to create the RPA bot
            self.client.post(
                "/custom_components/bots/",  # Adjust endpoint if different in Skycode
                json=rpa_payload,
                headers=headers,
                name="Create RPA Bot"
            )

    @task
    # url not found error but get updated on skycode
    def update_rpa_bot(self):
        url = "/custom_components/bots/55/181/"

        payload = {
            "name": "skycode-updated",
            "bot_name": "screen_scraping",
            "bot_description": "updated new description: automating enhanced skycode process",
            "bot_uid": None,
            "bot_schema_json": {
                "url": "http://skycode-studio-qa.s3-website.ap-south-1.amazonaws.com/auth/login",
                "forms": [
                    {
                        "form_value": [
                            {"field_id": "username", "value": "infinitesys@gmail.com", "value_type": "value"},
                            {"field_id": "password", "value": "Password@123", "value_type": "value"}
                        ],
                        "form_element_details": [
                            {
                                "efield_id": "username",
                                "evalue": "//*[@id='root']/div/main/div/div[2]/div[3]/form/div/div[3]/div[1]/div[2]/input",
                                "evalue_type": "XPATH",
                                "eaction": "send_keys",
                                "ewait": False,
                                "eskip": False
                            },
                            {
                                "efield_id": "password",
                                "evalue": "//*[@id='root']/div/main/div/div[2]/div[3]/form/div/div[3]/div[2]/div[2]/input",
                                "evalue_type": "XPATH",
                                "eaction": "send_keys",
                                "ewait": False,
                                "eskip": False
                            },
                            {
                                "efield_id": "login",
                                "evalue": "//*[@id='root']/div/main/div/div[2]/div[3]/form/div/div[4]/button/div",
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
                        "initialized": "True",
                        "navigated": "True",
                        "updated": "True",
                        "closed": "False",
                        "error": "None",
                        "processed_forms_count": 1
                    }
                ]
            }
        }

        headers = {"Content-Type": "application/json"}

        self.client.put(
            f"/custom_components/bots/55/181/",
            json=payload,
            headers=headers,
            name="Update RPA Bot"
        )
    #rpa preview running
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


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [RpaTasks]
