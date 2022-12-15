import os
import uuid
from typing import List
from app.models.schemas.groups import GroupSchema, GroupSchemaTransaction, GroupDB
from app.services import http_requests
from app.services import rollback_service

CLUSTER_URL = os.getenv('CLUSTER_URL')


async def send_create(group: GroupSchema) -> GroupDB:
    group_send = GroupSchemaTransaction(
        name=group.name, description=group.description, transaction_id=str(uuid.uuid4()))
    response, _ = await http_requests.post(CLUSTER_URL, group_send.__dict__)
    if response:
        return GroupDB(id=response["id"],
                       name=response["name"],
                       description=response["description"],
                       transaction_id=response["transaction_id"])
    else:
        await rollback_service.add_delete_group(group_send.transaction_id)
        return None


async def get_by_id(id: int) -> GroupDB:
    response, _ = await http_requests.get('{}/{}'.format(CLUSTER_URL, id), id)
    if response:
        return GroupDB(id=response["id"],
                       name=response["name"],
                       description=response["description"],
                       transaction_id=response["transaction_id"])
    else:
        return None


async def get_all() -> List[GroupDB]:
    groups, _ = await http_requests.get(CLUSTER_URL)
    return groups


async def send_delete(id: int):
    get_response, _ = await http_requests.get('{}/{}'.format(CLUSTER_URL, id), id)
    if get_response:
        response, _ = await http_requests.delete('{}/{}'.format(CLUSTER_URL, id), id)
        if not response:
            await rollback_service.add_delete_group(response["transaction_id"])
        return response
    return False
