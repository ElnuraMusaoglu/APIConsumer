from typing import List
from fastapi import APIRouter, HTTPException
from starlette import status
from app.core import logging

from app.models.schemas.groups import (
    GroupClusterSchema,
    GroupClusterDB
)
from app.services.cluster import get_by_id, get_all, delete, create, get_by_transaction_id

router = APIRouter()


@router.get("", response_model=List[GroupClusterDB])
async def get_groups() -> List[GroupClusterDB]:
    groups = await get_all()
    if not groups:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Groups not found')
    return groups


@router.get("/{group_id}/", response_model=GroupClusterDB)
async def get(group_id: int):
    group = await get_by_id(group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Group not found')
    return group


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GroupClusterDB)
async def create_group(group_create: GroupClusterSchema) -> GroupClusterDB:
    group = await create(group_create)
    if not group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Bad request. Perhaps the group exists.')
    return group


@router.delete('/{group_id}/', status_code=status.HTTP_200_OK)
async def delete_group(group_id: int) -> GroupClusterDB:
    group = await get_by_id(group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail='Group not found')
    await delete(group_id)
    return group


@router.delete('/transaction/{transaction_id}/', status_code=status.HTTP_200_OK)
async def delete_group(transaction_id: str) -> GroupClusterDB:
    group = await get_by_transaction_id(transaction_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail='Group not found')
    await delete(group.id)
    return group


@router.get('/ping')
async def pong():
    logging.info("PING")
    return {'ping': 'pong'}
