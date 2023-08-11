from locust import HttpUser, between, task


class APIUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def test(self):
        json = {"message": "poliza de seguros que incluya proteccion contra covid 19"}
        self.client.post(
            "/test/",
            json=json,
        )
