import requests 


url = "http://127.0.0.1:8000/tasks"

#GET requests 
resp = requests.get(url)
print(resp.status_code)
print(resp.json())

#POST requests 

task = {"id": 1, "name": "Buy milk"}
        #"id": 2, "name": "Walk dog"}
resp = requests.post(url, json=task)
print(resp.json())


# PUT and delete 
#update 
requests.put(
    url, 
    json = {"id": 1, "name": "Buy milk","done": True}
    )

#GET requests 
resp = requests.get(url)
print(resp.status_code)
print(resp.json())

for task in requests.get("http://127.0.0.1:8000/tasks").json():
    print(f"{task['id']}: {task['name']} ({'done' if task['done'] else'pending'})")
