from typing import List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette import status

from app.models.schemas.groups import (
    GroupSchema,
    GroupDB
)
from app.services import groups as groupservice

router = APIRouter()


@router.get("", response_model=List[GroupDB])
async def get_groups() -> List[GroupDB]:
    response = await groupservice.get_all()
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Groups not found')
    return response


@router.get("/{group_id}/", response_model=GroupDB)
async def get(group_id: int):
    group = await groupservice.get_by_id(group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Group not found')
    return group


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GroupDB)
async def create_group(group_create: GroupSchema) -> GroupDB:
    group = await groupservice.send_create(group_create)
    if not group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Bad request. Perhaps the group exists.')
    return group


@router.delete('/{group_id}/', status_code=status.HTTP_200_OK)
async def delete_group(group_id: int) -> GroupDB:
    group = await groupservice.send_delete(group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail='Group not found')
    return group


@router.get('/ping')
async def pong():
    return {'ping': 'pong'}
