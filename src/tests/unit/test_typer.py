from tests import utils


@utils.async_methods_in_db_transaction
class TestTyper:
    async def test_create_tron(
        self, container_singletone, db_transaction
    ):
        from app import typer

        typer.create_tron("TGNUXxxhFHsfuPwBV8RndDnBUazSrH6sTW", 570, 64276, 0.001289)
