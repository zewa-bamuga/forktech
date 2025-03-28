import logging

from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import UnitOfWork
from a8t_tools.logging.utils import setup_logging
from a8t_tools.storage.local_storage import LocalStorageBackend
from dependency_injector import containers, providers

from app.config import Settings
from app.domain.tron.containers import TronContainer


class Container(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()
    config.from_dict(
        options=Settings(_env_file=".env", _env_file_encoding="utf-8").model_dump(),  # type: ignore [call-arg]
    )

    logging = providers.Resource(
        setup_logging,
        logger_level=logging.INFO,
        sentry_dsn=config.sentry.dsn,
        sentry_environment=config.sentry.env_name,
        sentry_traces_sample_rate=config.sentry.traces_sample_rate,
        json_logs=False,
    )

    transaction = providers.Singleton(AsyncDbTransaction, dsn=config.db.dsn)

    unit_of_work = providers.Factory(UnitOfWork, transaction=transaction)

    local_storage_backend = providers.Factory(
        LocalStorageBackend,
        base_path=config.storage.local_storage.base_path,
        base_uri=config.storage.local_storage.base_uri,
    )

    tron = providers.Container(
        TronContainer,
        transaction=transaction,
    )
