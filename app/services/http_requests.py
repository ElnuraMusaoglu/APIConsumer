import aiohttp
import json
from app.core import logging


async def exception_handler(func):
    async def inner_function(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception as e:
            logging.info('Http Error {}'.format(str(e)))

    return inner_function


#@exception_handler
async def get(url, id=0, client_timeout=300):
    async with aiohttp.ClientSession() as session:
        timeout = aiohttp.ClientTimeout(total=client_timeout)
        result, response_status = None, 500
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.text()
                    result = json.loads(data)
                response_status = response.status
        except Exception as e:
          logging.info('Client Error {}'.format(str(e)))
        finally:
            await session.close()
            return result, response_status


async def post(url, json_data, client_timeout=300):
    async with aiohttp.ClientSession() as session:
        timeout = aiohttp.ClientTimeout(total=client_timeout)
        result, response_status = None, 500
        try:
            async with session.post(url, json=json_data, timeout=timeout) as response:
                if response.status == 201:
                    logging.info("Status : {}".format(str(response.status)))
                    data = await response.text()
                    result = json.loads(data)
                response_status = response.status
        except Exception as e:
          logging.info('Client Error {}'.format(str(e)))
        finally:
            await session.close()
            return result, response_status


async def delete(url, id, client_timeout=300):
    async with aiohttp.ClientSession() as session:
        timeout = aiohttp.ClientTimeout(total=client_timeout)
        result, response_status = False, 500
        try:
            async with session.delete(url, timeout=timeout) as response:
                if response.status == 200:
                    result = True
                response_status = response.status
        except Exception as e:
          logging.info('Client Error {}'.format(str(e)))
        finally:
            await session.close()
            return result, response_status


async def put(url, json_data, client_timeout=300):
    async with aiohttp.ClientSession() as session:
        timeout = aiohttp.ClientTimeout(total=client_timeout)
        try:
            async with session.put(url, json=json_data, timeout=timeout) as response:
                if response.status == 200:
                    logging.info("Status : {}".format(str(response.status)))
        except Exception as e:
          logging.info('Client Error'.format(str(e)))
        finally:
            await session.close()
