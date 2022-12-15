import os
from app.db.repositories import groupdelete_repository
from app.models.schemas.groups import GroupDeleteSchema
from app.services import http_requests
from app.core import logging

CLUSTER_URL = os.getenv('CLUSTER_URL')


async def add_delete_group(transaction_id: str):
    """Record DB groupdelete table with transaction id and timestamp

    Args:
        transaction_id (str): transaction_id of group
    """
    await groupdelete_repository.create(GroupDeleteSchema(transaction_id=transaction_id))
    # Create Group - Delete Group couldn't be sent to Cluster API.
    # Transaction ID added to delete group table to be processed by Background Repeated Task.
    # If the API is unstable  when sending create group http request - > 
    # Add to be table, and to rollback the process delete the data anyway
    # If the API is unstable  when sending delete group http request - > 
    # Add to be table, and delete the data anyway
    # The Background repeated job will be working repeatedly all provide the consistency between this API and Cluster API
    logging.info("Create Group - Delete Group couldn't be sent to Cluster API.")
    logging.info("Transaction ID : {}".format(str(transaction_id)))


async def check_and_send_delete_group_task() -> None:
    """Checks db table deletegroup and if any data exists, sends http request to the cluster,
    If it can delete group, then remove data from deletegroup table, 
    Otherwise do the job repeatedly
    """
    try:
        groups_to_delete = await groupdelete_repository.get_all()
        for group_to_delete in groups_to_delete.groups:
            logging.info("Transaction to be deleted : {}".format(str(group_to_delete.transaction_id)))
            url = "{}/transaction/{}/".format(CLUSTER_URL,
                                              group_to_delete.transaction_id)
            response, status_code = await http_requests.delete(url, group_to_delete.transaction_id)
            if response or status_code == 204:  # 200 or 204 -> No such data or deleted, remove from group delete table
                await groupdelete_repository.delete_by_transaction(str(group_to_delete.transaction_id))
                logging.info("No such group in cluster so deleted from groupdelete table")
    except Exception as ex:
        logging.info(str(ex))
