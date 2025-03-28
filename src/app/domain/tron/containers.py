from dependency_injector import containers, providers
from passlib.context import CryptContext

from a8t_tools.bus.producer import TaskProducer
from a8t_tools.db.transactions import AsyncDbTransaction

from app.domain.tron.core.commands import TronCreateCommand
from app.domain.tron.core.query import TronCredentialsQuery, TronManagementListQuery, TronListQuery
from app.domain.tron.core.repositories import TronRepository


class TronContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    task_producer = providers.Dependency(instance_of=TaskProducer)

    secret_key = providers.Dependency(instance_of=str)

    private_key = providers.Dependency(instance_of=str)

    public_key = providers.Dependency(instance_of=str)

    pwd_context = providers.Dependency(instance_of=CryptContext)

    repository = providers.Factory(
        TronRepository,
        transaction=transaction,
    )

    create_command = providers.Factory(
        TronCreateCommand,
        repository=repository,
    )

    tron_credentials_query = providers.Factory(
        TronCredentialsQuery,
    )

    tron_list_query = providers.Factory(
        TronListQuery,
        repository=repository,
    )

    management_list_query = providers.Factory(
        TronManagementListQuery,
        query=tron_list_query,
    )
