# myapp/tasks.py
from celery import shared_task
import requests
from .models import threads, CompanySell
from openai import OpenAI
import json
import time
client = OpenAI(api_key="")

@shared_task
def add_company(data):
    pass

@shared_task(bind = True, max_retries = 0, default_retry_delay = 40)
def check_for_new_messages(*args, **kwargs):
    url_base = "https://b24-jhixft.bitrix24.kz/rest/1/qsbme0fps6axl6c7/"
    dialogs = requests.get(url_base+"im.recent.list").json()["result"]["items"]
    
    unique_user_ids = threads.objects.values_list('user_id', flat=True).distinct()
    unique_user_ids_list = list(unique_user_ids)

    for dialog in dialogs:
        if dialog["id"] in unique_user_ids_list and dialog["id"] != "chat10" and dialog["id"] != "chat8" and dialog["id"] != 1 and dialog["id"] != 0:
            print("First")
            thread_id = threads.objects.get(user_id = dialog["id"]).thread_id
            messages = requests.get(url_base+f"im.dialog.messages.get?DIALOG_ID={dialog['id']}").json()
            unread_messages = ""
            for message in messages["result"]["messages"]:
                if message["id"] > threads.objects.get(thread_id = thread_id).last_message_id and message["author_id"] != 0 and message["author_id"] != 1 :
                    unread_messages = unread_messages + message["text"] +"\n"
                    th_object = threads.objects.get(thread_id = thread_id)
                    th_object.last_message_id = message["id"]
                    th_object.save()

                    client.beta.threads.messages.create(
                        thread_id,
                        role = "user",
                        content = unread_messages
                    )
                    run = client.beta.threads.runs.create(
                        thread_id = thread_id,
                        assistant_id = "asst_Ibu9BqhtcfMBMVNki4dx9OI8"
                    )
                    time.sleep(4)
                    status = False
                    while status == False:
                        run_steps = client.beta.threads.runs.steps.list(
                            thread_id = thread_id,
                            run_id = run.id    
                        )
                        print(run_steps)
                        if run_steps.data[0].status == "completed":
                            status = True

                    response = client.beta.threads.messages.list(
                        thread_id = thread_id
                    )
                    response_message = response.data[0].content[0].text.value
                    if "***БИН***" in response_message:
                        bin = response_message.split("***БИН***:")[1].split("\n")[0]
                        name = response_message.split("***Название***:")[1].split("\n")[0]
                        description = response_message.split("***Описание***:")[1].split("\n")[0]
                        telephone = response_message.split("***Телефон***:")[1].split("\n")[0]
                        data = {
                            "c_bin": bin,
                            "c_name": name,
                            "c_description": description,
                            "c_telephone": telephone,
                        }
                        print(data)

                    requests.get(url_base+f"im.message.add?DIALOG_ID={dialog['id']}&MESSAGE={response_message}")
                    
        if dialog["id"] not in unique_user_ids_list and dialog["id"] != "chat10" and dialog["id"] != "chat8" and dialog["id"] != 1 and dialog["id"] != 0:
            print("Second")
            messages = requests.get(url_base+f"im.dialog.messages.get?DIALOG_ID={dialog['id']}").json()
            unread_messages = ""
            last_message_id = 0
            for message in messages["result"]["messages"]:
                if message["author_id"] != 0 and message["author_id"] != 1:
                    unread_messages = unread_messages + message["text"] +"\n"
                    last_message_id = message["id"]
                    thread_id = client.beta.threads.create().id
                    threads.objects.create(user_id = dialog["id"], thread_id = thread_id, last_message_id = last_message_id)
                    client.beta.threads.messages.create(
                        thread_id,
                        role = "user",
                        content = unread_messages
                    )
                    run = client.beta.threads.runs.create(
                        thread_id = thread_id,
                        assistant_id = "asst_Ibu9BqhtcfMBMVNki4dx9OI8"
                    )
                    time.sleep(6)
                    status = False
                    while status == False:
                        run_steps = client.beta.threads.runs.steps.list(
                            thread_id = thread_id,
                            run_id = run.id    
                        )
                        if run_steps.data[0].status == "completed":
                            status = True

                    response = client.beta.threads.messages.list(
                        thread_id = thread_id
                    )
                    print(response)
                    response_message = response.data[0].content[0].text.value
                    chat_id = dialog['id'].replace("chat", "")
                    requests.get(url_base+f"imopenlines.session.join?CHAT_ID={chat_id}")
                    requests.get(url_base+f"im.message.add?DIALOG_ID={dialog['id']}&MESSAGE={response_message}")


    print("End")



