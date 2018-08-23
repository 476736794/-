import requests
import json
import pandas as pd

from settings import headers
# 创建格式化的url
url = "http://m.maoyan.com/mmdb/comments/movie/1217513.json?_v_=yes&offset={}&startTime=2018-08-{}%2015%3A10%3A31"
date = range(20,23)
def get_json(url,k_name):
    json_str = requests.get(url=url,headers=headers).content
    data = json.loads(json_str)
    data = data[str(k_name)]
    return data

def mao_yan():
    # 先创建列标题
    df = pd.DataFrame(columns=['city','content'])
    print("开始爬取...")
    cnt = 0
    for day in date:
        try:
            for page in range(0,100):
                url1 = url.format(page*15,str(day))
                # 最新短评
                data_cmts = get_json(url1,'cmts')
                # 最热短评
                data_hcmts = get_json(url1, 'hcmts')
                for data_cmt in data_cmts:
                    item = {}
                    if cnt == 0:
                        for data_hcmt in data_hcmts:
                            item['city'] = data_hcmt['cityName']
                            item['content'] = data_hcmt['content']
                            item['date'] = data_hcmt['startTime']
                            # print(data_hcmt['content'])
                            df = df.append(item, ignore_index=True)
                        cnt+=1
                    item['city'] = data_cmt['cityName']
                    item['content'] = data_cmt['content']
                    item['date'] = data_cmt['startTime']
                    df = df.append(item, ignore_index=True)
        except Exception as e:
            # print(e)
            df.to_csv('train_set.csv',encoding='utf_8_sig')
            continue

if __name__ == "__main__":
    mao_yan()
    print("爬取已结束。。。")