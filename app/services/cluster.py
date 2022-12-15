from typing import List
from app.db.repositories import grouprepository
from app.models.schemas.groups import GroupClusterSchema, GroupClusterDB


async def create(group: GroupClusterSchema) -> GroupClusterDB:
    group_id = await grouprepository.create(group)
    return GroupClusterDB(id=group_id, name=group.name,
                 description=group.description,
                 transaction_id=group.transaction_id)


async def get_by_id(id: int) -> GroupClusterDB:
    return await grouprepository.get(id)


async def get_all() -> List[GroupClusterDB]:
    groups = await grouprepository.get_all()
    return groups


async def delete(id: int) -> GroupClusterDB:
    return await grouprepository.delete(id)


async def delete_by_transaction(id: str) -> GroupClusterDB:
    return await grouprepository.delete_by_transaction_id(id)

async def get_by_transaction_id(id: str) -> GroupClusterDB:
    group =  await grouprepository.get_by_transaction_id(id)
    if group:
        return GroupClusterDB(**group)
    return None