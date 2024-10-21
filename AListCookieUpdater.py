# 批量更新AList的微云cookie by suzh@20241021

import requests
import json

def main():
    # Login
    payload = json.dumps({
        "username": "admin",
        "password": "31536u2@mike"
        })
    api_url = "http://192.168.0.188:5244/api/auth/login"
    headers = {'Content-Type': 'application/json'}
    result = requests.post(api_url, headers = headers, data = payload)
    # print(result.text)
    result_data = json.loads(result.text)
    if result_data['code'] != 200:
        print("Login failed")
        return
    token = result_data['data']['token']
    print(token)

    # Get store list
    api_url = "http://192.168.0.188:5244/api/admin/storage/list"
    headers = {'Authorization': f'{token}'}
    result = requests.get(api_url, headers = headers)
    # print(result.text)
    result_data = json.loads(result.text)
    if result_data['code'] != 200:
        print("Get store list failed")
        return
    store_list = result_data['data']['content']

    # Batch update weiyun cookie
    api_url = "http://192.168.0.188:5244/api/admin/storage/update"
    new_cookie = "{{new_cookie}}"
    headers = {'Authorization': f'{token}', 'Content-Type': 'application/json'}

    for store in store_list:
        if store['driver'] == 'WeiYun':
            print(store['mount_path'])
            addition = store['addition']
            addition_data = json.loads(addition)
            # print(addition_data['root_folder_id'])
            addition_data['cookies'] = new_cookie
            store['addition'] = json.dumps(addition_data)
            payload = json.dumps(store)
            result = requests.post(api_url, headers = headers, data = payload)
            # print(result.text)
            if result_data['code'] != 200:
                print("Update weiyun cookie failed")
            else:
                print("Update weiyun cookie success")

if __name__ == "__main__":
    main()
