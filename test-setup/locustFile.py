from locust import HttpUser, TaskSet, task, between

class CustomerTasks(TaskSet):
    @task(1)
    def add_customer(self):
        self.client.post(
            "/customer/form.html",
            data={
                "name": "Test",
                "firstname": "User",
                "email": "testuser@example.com",
                "street": "123 Main St",
                "city": "Sample City",
            },
        )

    @task(1)
    def list_customers(self):
        self.client.get("/customer/list.html")

    @task(1)
    def update_customer(self):
        self.client.put(
            "/customer/1.html",
            data={
                "name": "Updated Name",
                "firstname": "Updated Firstname",
                "email": "updateduser@example.com",
                "street": "456 Updated St",
                "city": "Updated City",
            },
        )

class CatalogTasks(TaskSet):
    @task(1)
    def list_catalog(self):
        self.client.get("/catalog/list.html")

    @task(1)
    def add_product(self):
        self.client.post(
            "/catalog/form.html",
            data={"name": "New Product", "price": 9.99},
        )

    @task(1)
    def search_product(self):
        self.client.get("/catalog/searchByName.html", params={"query": "i", "submit": ""})

class OrderTasks(TaskSet):
    @task(1)
    def add_order(self):
        self.client.post(
            "/order/",
            data={
                "customerId": 2,
                "orderLine[0].count": 10,
                "orderLine[0].itemId": 1,
                "orderLine[1].count": 20,
                "orderLine[1].itemId": 2,
                "orderLine[2].count": 30,
                "orderLine[2].itemId": 3,
            },
        )

    @task(1)
    def list_orders(self):
        self.client.get("/order/")

class MicroserviceUser(HttpUser):
    tasks = {
        CustomerTasks: 3,
        CatalogTasks: 3,
        OrderTasks: 2
    }
    wait_time = between(1, 3)


# kata
# locust -f locustFile.py --host=http://64.226.93.187:30292/ --users=100 --spawn-rate=1 --run-time=5m --headless --csv=kata --html=kata.html
# runc
# locust -f locustFile.py --host=http://64.226.93.187:30278/ --users=100 --spawn-rate=1 --run-time=5m --headless --csv=runc --html=runc.html
# gvisor 
# locust -f locustFile.py --host=http://64.226.93.187:30573/ --users=100 --spawn-rate=1 --run-time=5m --headless --csv=gvisor --html=gvisor.html


# kata 50 user
# locust -f locustFile.py --host=http://64.226.93.187:30292/ --users=50 --spawn-rate=1 --run-time=5m --headless --csv=kata50 --html=kata50.html
# runc 50 user
# locust -f locustFile.py --host=http://64.226.93.187:30278/ --users=50 --spawn-rate=1 --run-time=5m --headless --csv=runc50 --html=runc50.html
# gvisor 50 user
# locust -f locustFile.py --host=http://64.226.93.187:30573/ --users=50 --spawn-rate=1 --run-time=5m --headless --csv=gvisor50 --html=gvisor50.html


# kata low user
# locust -f locustFile.py --host=http://64.226.93.187:30292/ --users=120 --spawn-rate=5 --run-time=5m --headless --csv=kata_low --html=kata_low.html
# runc low user
# locust -f locustFile.py --host=http://64.226.93.187:30278/ --users=120 --spawn-rate=5 --run-time=5m --headless --csv=runc_low --html=runc_low.html
# gvisor low user
# locust -f locustFile.py --host=http://64.226.93.187:30573/ --users=120 --spawn-rate=5 --run-time=5m --headless --csv=gvisor_low --html=gvisor_low.html