from __future__ import absolute_import

import codecs
import csv
import json

import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from .models import ProductFile, ProductInfo, ProductWebHook


def stream_file_update(file_id, current_row, total_rows):
    channel_layer = get_channel_layer()
    # web socket clients will open and listen to this channel to get the event update
    room = "file_stream"
    async_to_sync(channel_layer.group_send)(
        room,
        {
            "type": "chat.message",
            "room_id": room,
            "message": {
                "total_rows": total_rows,
                "current_row": current_row,
                "file_id": file_id,
            },
        },
    )


@shared_task
def process_file_to_db(file_id):
    try:
        file_obj = ProductFile.objects.get(id=file_id)
        csvfile = csv.reader(codecs.iterdecode(file_obj.file, "utf-8"))
        next(csvfile)
        total_rows = 123  # hard coded -needs to remove
        inserted_rows = 0
        for row in csvfile:
            ProductInfo.objects.update_or_create(
                sku=row[1].lower(), defaults={"name": row[0], "description": row[2]}
            )
            inserted_rows = inserted_rows + 1
            # stream_file_update(file_id, inserted_rows, total_rows)
    except Exception as e:
        print(e)
        raise


@shared_task
def webhook_event(prod_data):
    try:
        web_hooks = ProductWebHook.objects.all()
        for web_hook_obj in web_hooks:
            web_hook_url = web_hook_obj.url
            requests.post(
                web_hook_url,
                data=json.dumps(prod_data),
                headers={"Content-Type": "application/json"},
            )
    except Exception as e:
        print(e)
