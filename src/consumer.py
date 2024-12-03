import requests
from flask import Flask, jsonify, render_template, abort


class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class UserConsumer:

    def __init__(self, base_uri: str):
        self.base_uri = base_uri

    def list_users(self):
        url = f"{self.base_uri}/users"
        response = requests.get(url)
        response.raise_for_status()
        users_data = response.json()
        return [User(user_id=u["id"], name=u["name"], email=u["email"]) for u in users_data]

    def user_detail(self, user_id):
        url = f"{self.base_uri}/users/{user_id}"
        response = requests.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        user_data = response.json()
        return User(user_id=user_data["id"], name=user_data["name"], email=user_data["email"])


class WebApp:
    def __init__(self):
        BASE_URL = "http://127.0.0.1:5000"

        self.app = Flask(__name__)
        self.consumer = UserConsumer(BASE_URL)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/")
        def home():
            try:
                users = self.consumer.list_users()
                return render_template("users.html", users=users)
            except Exception as e:
                return f"Error al cargar usuarios: {e}", 500

        @self.app.route("/users/<int:user_id>")
        def user_detail(user_id):
            user = self.consumer.user_detail(user_id)
            if user:
                return jsonify(user.to_dict())
            else:
                return abort(404, description="Usuario no encontrado")

    def run(self, **kwargs):
        self.app.run(**kwargs)


if __name__ == "__main__":
    web_app = WebApp()
    web_app.run(debug=True, port=5001)
