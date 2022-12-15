from typing import List
from app.models.schemas.groups import GroupDeleteSchema, GroupDeleteDB, ListOfGroupDeleteDB
from app.db.db import database, groupdelete


async def create(group_delete: GroupDeleteSchema):
    query = groupdelete.insert().values(
        transaction_id=group_delete.transaction_id
    )
    return await database.execute(query=query)


async def get(id: int):
    query = groupdelete.select().where(id == groupdelete.c.id)
    result = await database.fetch_one(query=query)
    return GroupDeleteDB(result)


async def get_all()->List[GroupDeleteDB]:
    query = groupdelete.select()
    result = await database.fetch_all(query=query)
    return ListOfGroupDeleteDB(groups=result)


async def delete(id: int):
    query = groupdelete.delete().where(id == groupdelete.c.id)
    return await database.execute(query=query)


async def delete_by_transaction(transaction_id: str):
    query = groupdelete.delete().where(transaction_id == groupdelete.c.transaction_id)
    return await database.execute(query=query)
