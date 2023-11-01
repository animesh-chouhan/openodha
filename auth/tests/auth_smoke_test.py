import json
import secrets
import requests

url = "http://localhost:9000"
# url = "https://openodha.animeshchouhan.com/auth"

username = secrets.token_urlsafe(12)
password = secrets.token_urlsafe(12)

print(username)
print(password)


class AuthSmokeTest:
    def test_health(self):
        response = requests.request("GET", f"{url}/health")
        assert response.status_code == 200
        print(response.text)

    def test_user_creation(self):
        payload = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "POST", f"{url}/users", headers=headers, data=payload
        )
        assert response.status_code == 200
        print(response.text)

        res = response.json()
        self.user_id = res["user_id"]
        assert res["username"] == username
        assert res["api_key"] == None

    def test_user_recreation(self):
        payload = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "POST", f"{url}/users", headers=headers, data=payload
        )
        assert response.status_code == 400
        print(response.text)

        assert response.json()["detail"] == "Username already registered"

    def test_login(self):
        payload = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "POST", f"{url}/login", headers=headers, data=payload
        )
        assert response.status_code == 200
        print(response.text)
        self.cookie_jar = response.cookies
        self.cookies = {}
        for c in response.cookies:
            print(f"{c.name}: {c.value}")
            self.cookies[c.name] = c.value

        res = response.json()
        assert res["username"] == username
        assert res["user_id"] == self.user_id
        assert res["api_key"] == None

    def test_list_users_without_cookie(self):
        response = requests.request("GET", f"{url}/users")
        assert response.status_code == 401
        print(response.text)

    def test_list_users_with_cookie(self):
        response = requests.request("GET", f"{url}/users", cookies=self.cookie_jar)
        assert response.status_code == 200
        print(response.text)

    def test_get_user_by_username(self):
        response = requests.request(
            "GET", f"{url}/users/{username}", cookies=self.cookie_jar
        )
        assert response.status_code == 200
        print(response.text)

    def test_get_api_key_wo_set(self):
        response = requests.request("GET", f"{url}/api-key", cookies=self.cookie_jar)
        assert response.status_code == 404
        print(response.text)

    def test_set_api_key(self):
        response = requests.request("POST", f"{url}/api-key", cookies=self.cookie_jar)
        assert response.status_code == 200
        print(response.text)

        res = response.json()
        self.api_key = res["api_key"]

    def test_get_api_key_with_set(self):
        response = requests.request("GET", f"{url}/api-key", cookies=self.cookie_jar)
        assert response.status_code == 200
        print(response.text)

        res = response.json()
        assert res["api_key"] == self.api_key

    def test_logout(self):
        response = requests.request("POST", f"{url}/logout", cookies=self.cookie_jar)
        assert response.status_code == 200
        print(response.text)

        res = response.json()
        assert res["status"] == "User successfully logged out"


if __name__ == "__main__":
    smoke_test = AuthSmokeTest()
    smoke_test.test_health()
    smoke_test.test_user_creation()
    smoke_test.test_user_recreation()
    smoke_test.test_login()
    smoke_test.test_list_users_without_cookie()
    smoke_test.test_list_users_with_cookie()
    smoke_test.test_get_user_by_username()
    smoke_test.test_get_api_key_wo_set()
    smoke_test.test_set_api_key()
    smoke_test.test_get_api_key_with_set()
    smoke_test.test_logout()
