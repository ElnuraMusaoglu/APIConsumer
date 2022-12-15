from app.models.schemas.groups import GroupClusterSchema
from app.db.db import database, groups


async def create(group: GroupClusterSchema):
    query = groups.insert().values(
        name=group.name,
        description=group.description,
        transaction_id=group.transaction_id
    )
    return await database.execute(query=query)


async def get(id: int):
    query = groups.select().where(id == groups.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = groups.select()
    return await database.fetch_all(query=query)


async def put(id: int, group: GroupClusterSchema):
    query = (
        groups
        .update()
        .where(id == groups.c.id)
        .values(name=group.name, description=group.description, transaction_id=group.transaction_id)
        .returning(groups.c.id)
    )

    return await database.execute(query=query)


async def delete(id: int):
    query = groups.delete().where(id == groups.c.id)
    return await database.execute(query=query)


async def delete_by_transaction_id(transaction_id: str):
    query = groups.delete().where(transaction_id == groups.c.transaction_id)
    return await database.execute(query=query)


async def get_by_transaction_id(transaction_id: str):
    query = groups.select().where(transaction_id == groups.c.transaction_id)
    return await database.fetch_one(query=query)
