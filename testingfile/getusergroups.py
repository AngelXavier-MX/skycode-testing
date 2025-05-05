from locust import HttpUser, task, between, TaskSet

class UserGroupTasks(TaskSet):


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://13.235.34.196"
    tasks = [UserGroupTasks]
