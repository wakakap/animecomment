import requests

# API 基础 URL
BASE_URL = "https://api.bgm.tv"

# API Key (如果需要)
API_KEY = ""  # 替换为你的 API Key

# 自定义 User-Agent
HEADERS = {
    "User-Agent": "wakakap/my-private-project",
    "Authorization": f"Bearer {API_KEY}"  # 根据文档要求添加 API Key
}

# 调用搜索接口
def search_subjects(keyword):
    url = f"{BASE_URL}/v0/search/subjects"
    payload = {"keyword": keyword, "type": 2}  # 例如，type: 动画=2
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print("搜索结果：")
            return data
        else:
            print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
    except requests.RequestException as e:
        print(f"请求时发生错误: {e}")

# 调用收藏接口
def get_collections(username, subject_type=2, type=2, limit=50, offset=0):
    url = f"{BASE_URL}/v0/users/{username}/collections"
    print(f"请求URL: {url}")
    print(f"请求参数: subject_type={subject_type}, type={type}, limit={limit}, offset={offset}")
    
    params = {
        "subject_type": subject_type,
        "type": type,
        "limit": limit,
        "offset": offset
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        print(f"响应状态码: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
    except requests.RequestException as e:
        print(f"请求时发生错误: {e}")

def get_all_collections(username, subject_type=2, type=2, limit=50, offsetmax=50):
    all_data = []
    for offset in range(0, offsetmax, 50):
        print(f"当前偏移量: {offset}")
        print(f"使用的用户名: {username}")
        data = get_collections(username, subject_type, type, limit, offset)
        if data:
            print(f"获取到的数据量: {len(data)}")
            if isinstance(data, dict) and 'data' in data:
                print(f"实际数据量: {len(data['data'])}")
                all_data.extend(data['data'])
            else:
                print("数据格式不正确或缺少 'data' 键")
        else:
            print("未获取到数据")
    print(f"总数据量: {len(all_data)}")
    return all_data