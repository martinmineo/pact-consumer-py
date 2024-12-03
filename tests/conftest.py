import os
from pathlib import Path
from typing import Generator, Any

import pytest
from flask.cli import load_dotenv
from pact import Pact, Consumer, Provider
from yarl import URL

from src.consumer import UserConsumer

MOCK_URL = URL("http://localhost:8080")


@pytest.fixture(scope="module")
def pact(broker: URL, pact_dir: Path) -> Generator[Pact, Any, None]:
    consumer = Consumer(name="pact-consumer-py", version="0.0.1", auto_detect_version_properties=True)
    pact = consumer.has_pact_with(
        Provider("pact-provider-py"),
        pact_dir=str(pact_dir),
        publish_to_broker=True,
        # Mock service configuration
        host_name=MOCK_URL.host,
        port=MOCK_URL.port,
        # Broker configuration
        broker_base_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
    )

    pact.start_service()
    yield pact
    pact.stop_service()


@pytest.fixture(scope="session")
def broker(request: pytest.FixtureRequest) -> Generator[URL, Any, None]:
    load_dotenv()
    broker_url: str = os.getenv("BROKER_URL")
    yield URL(broker_url)
    return


@pytest.fixture(scope="session")
def pact_dir() -> Path:
    return Path(__file__).parent.parent.resolve() / "pacts"


@pytest.fixture
def user_consumer() -> UserConsumer:
    return UserConsumer(str(MOCK_URL))