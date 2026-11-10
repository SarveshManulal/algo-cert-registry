import logging

import algokit_utils

logger = logging.getLogger(__name__)


def deploy() -> None:
    """Deploy the registry and seed its app account for box storage."""
    from smart_contracts.artifacts.cert_registry.cert_registry_client import (
        CertRegistryFactory,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        CertRegistryFactory, default_sender=deployer.address
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    if result.operation_performed in {
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    }:
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer.address,
                receiver=app_client.app_address,
            )
        )

    logger.info(
        "Certificate registry deployed: app_id=%s app_address=%s",
        app_client.app_id,
        app_client.app_address,
    )
