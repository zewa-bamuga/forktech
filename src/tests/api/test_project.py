import pytest

from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestTron:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    async def test_add_address(self):
        response = await self.client.post(
            "/api/tron/v1/create",
            json=dict(
                address="TZHF6a17t1wWYBvzunaatrq1WbdR9sixaj",
            ),
        )
        assert response.status_code == 200, response.json()

    async def test_get_tron_list(self):
        factories.TronFactory.create_batch(10)
        response = await self.client.get("/api/tron/v1/get/list")
        assert response.status_code == 200, response.json()
        assert response.json()["count"] == 10
        assert len(response.json()["items"]) == 10
