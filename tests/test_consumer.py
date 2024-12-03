from pact import Pact, Like

from src.consumer import UserConsumer, User


def test_get_existing_user(pact: Pact, user_consumer: UserConsumer) -> None:
    expected: dict[str, str] = {
        "id": 1,
        "name": "Alice",
        "email": "alice@mail.com",
    }
    (
        pact.given("user_1_exists")
        .upon_receiving("a request for user 1")
        .with_request("GET", "/users/1")
        .will_respond_with(status=200, body=Like(expected), headers={"Content-Type": "application/json"})
    )

    with pact:
        user = user_consumer.user_detail(1)

        assert isinstance(user, User)
        assert user.name == expected["name"]
        assert user.email == expected["email"]

        pact.verify()
