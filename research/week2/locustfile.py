from locust import HttpUser, TaskSet, task, between, events

class UserBehavior(TaskSet):
    @task(1)
    def get_random(self):
        response = self.client.get("/random", timeout = 3600)
        print(f"Response from backend: {response.status_code}, {response.text}")
        if response.status_code != 200:
            print('Error: {}'.format(response.text))
        else:
            print(response.json())

class WebsiteUser(HttpUser):
    tasks = {UserBehavior: 1}
    wait_time = between(1, 3)

@events.request.add_listener
def record_response_time(request_type, name, response_time, response_length, **kwargs):
    print(f"Request Type: {request_type}, Name: {name}, Response Time: {response_time} ms, Response Length: {response_length} bytes")

