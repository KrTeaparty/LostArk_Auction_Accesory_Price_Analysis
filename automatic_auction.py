import requests
import json
import urllib
import itertools
import time
from datetime import datetime
import pandas as pd
import os

# Base Class
class LostArk():
    def __init__(self):
        with open('/root/workspace/project/lostark/api_key.txt', 'r') as f:
            self.api_key = 'bearer ' + f.read()

    def create_url(self, key, option=''):
        base = 'https://developer-lostark.game.onstove.com'
        url_val = self.url_dict[key]
        base += url_val
        return base

    def request_url(self, url):
        headers = {
            'accept': 'application/json',
            'authorization': self.api_key
        }

        response = requests.get(url, headers=headers)
        jsonObject = response.json()
        return jsonObject

# Auction Class
class LostArkAuction(LostArk):
    def __init__(self):
        super().__init__()

        self.url_dict = {
            'auction_options': '/auctions/options',
            'auction_items': '/auctions/items'
        }

    def request_url_post(self, url, cond):
        headers = {
            'accept': 'application/json',
            'authorization': self.api_key
        }
        response = requests.post(url, headers=headers, json=cond)

        if response.status_code == 429:
            #print("=" * 40)
            #print(f"API Limit Exceeded Waiting for {int(response.headers['Retry-After'])} seconds")
            #print("=" * 40)
            time.sleep(int(response.headers["Retry-After"]))
            response = requests.post(url, headers=headers, json=cond)
        elif response.status_code != 200:
            for i in range(5):
                response = requests.post(url, headers=headers, json=cond)
                if response.status_code == 200:
                    break
        jsonObject = response.json()
        return jsonObject

    def get_auction_options(self):
        url = self.create_url('auction_options')
        response = self.request_url(url)
        return response

    def get_auction_items(self, cond):
        url = self.create_url('auction_items')
        response = self.request_url_post(url, cond)
        return response

# 장신구 코드, 치특신 코드
codes = {
    200010: [(15,16), (15,18), (16,18)],
    200020: [15, 16, 18],
    200030: [15, 16, 18]
}

# 각인 코드 사전
EtcSubs = [{'Value': 118, 'Text': '원한', 'Class': ''},
 {'Value': 247, 'Text': '저주받은 인형', 'Class': ''},
 {'Value': 255, 'Text': '각성', 'Class': ''},
 {'Value': 111, 'Text': '안정된 상태', 'Class': ''},
 {'Value': 140, 'Text': '위기 모면', 'Class': ''},
 {'Value': 238, 'Text': '달인의 저력', 'Class': ''},
 {'Value': 240, 'Text': '중갑 착용', 'Class': ''},
 {'Value': 249, 'Text': '기습의 대가', 'Class': ''},
 {'Value': 254, 'Text': '돌격대장', 'Class': ''},
 {'Value': 109, 'Text': '정기 흡수', 'Class': ''},
 {'Value': 110, 'Text': '에테르 포식자', 'Class': ''},
 {'Value': 121, 'Text': '슈퍼 차지', 'Class': ''},
 {'Value': 134, 'Text': '구슬동자', 'Class': ''},
 {'Value': 141, 'Text': '예리한 둔기', 'Class': ''},
 {'Value': 142, 'Text': '급소 타격', 'Class': ''},
 {'Value': 241, 'Text': '폭발물 전문가', 'Class': ''},
 {'Value': 253, 'Text': '바리케이드', 'Class': ''},
 {'Value': 167, 'Text': '최대 마나 증가', 'Class': ''},
 {'Value': 288, 'Text': '결투의 대가', 'Class': ''},
 {'Value': 295, 'Text': '질량 증가', 'Class': ''},
 {'Value': 297, 'Text': '타격의 대가', 'Class': ''},
 {'Value': 299, 'Text': '아드레날린', 'Class': ''},
 {'Value': 300, 'Text': '속전속결', 'Class': ''},
 {'Value': 301, 'Text': '전문의', 'Class': ''},
 {'Value': 303, 'Text': '정밀 단도', 'Class': ''},
 {'Value': 125, 'Text': '광기', 'Class': '버서커'},
 {'Value': 127, 'Text': '오의 강화', 'Class': '배틀마스터'},
 {'Value': 129, 'Text': '강화 무기', 'Class': '데빌헌터'},
 {'Value': 130, 'Text': '화력 강화', 'Class': '블래스터'},
 {'Value': 188, 'Text': '광전사의 비기', 'Class': '버서커'},
 {'Value': 189, 'Text': '초심', 'Class': '배틀마스터'},
 {'Value': 190, 'Text': '극의: 체술', 'Class': '인파이터'},
 {'Value': 191, 'Text': '충격 단련', 'Class': '인파이터'},
 {'Value': 192, 'Text': '핸드거너', 'Class': '데빌헌터'},
 {'Value': 193, 'Text': '포격 강화', 'Class': '블래스터'},
 {'Value': 194, 'Text': '진실된 용맹', 'Class': '바드'},
 {'Value': 195, 'Text': '절실한 구원', 'Class': '바드'},
 {'Value': 293, 'Text': '점화', 'Class': '소서리스'},
 {'Value': 294, 'Text': '환류', 'Class': '소서리스'},
 {'Value': 196, 'Text': '분노의 망치', 'Class': '디스트로이어'},
 {'Value': 197, 'Text': '중력 수련', 'Class': '디스트로이어'},
 {'Value': 198, 'Text': '상급 소환사', 'Class': '서머너'},
 {'Value': 199, 'Text': '넘치는 교감', 'Class': '서머너'},
 {'Value': 200, 'Text': '황후의 은총', 'Class': '아르카나'},
 {'Value': 201, 'Text': '황제의 칙령', 'Class': '아르카나'},
 {'Value': 224, 'Text': '전투 태세', 'Class': '워로드'},
 {'Value': 225, 'Text': '고독한 기사', 'Class': '워로드'},
 {'Value': 256, 'Text': '세맥타통', 'Class': '기공사'},
 {'Value': 257, 'Text': '역천지체', 'Class': '기공사'},
 {'Value': 258, 'Text': '두 번째 동료', 'Class': '호크아이'},
 {'Value': 259, 'Text': '죽음의 습격', 'Class': '호크아이'},
 {'Value': 276, 'Text': '절정', 'Class': '창술사'},
 {'Value': 277, 'Text': '절제', 'Class': '창술사'},
 {'Value': 278, 'Text': '잔재된 기운', 'Class': '블레이드'},
 {'Value': 279, 'Text': '버스트', 'Class': '블레이드'},
 {'Value': 280, 'Text': '완벽한 억제', 'Class': '데모닉'},
 {'Value': 281, 'Text': '멈출 수 없는 충동', 'Class': '데모닉'},
 {'Value': 282, 'Text': '심판자', 'Class': '홀리나이트'},
 {'Value': 283, 'Text': '축복의 오라', 'Class': '홀리나이트'},
 {'Value': 284, 'Text': '아르데타인의 기술', 'Class': '스카우터'},
 {'Value': 285, 'Text': '진화의 유산', 'Class': '스카우터'},
 {'Value': 286, 'Text': '갈증', 'Class': '리퍼'},
 {'Value': 287, 'Text': '달의 소리', 'Class': '리퍼'},
 {'Value': 289, 'Text': '피스메이커', 'Class': '건슬링어'},
 {'Value': 290, 'Text': '사냥의 시간', 'Class': '건슬링어'},
 {'Value': 291, 'Text': '일격필살', 'Class': '스트라이커'},
 {'Value': 292, 'Text': '오의난무', 'Class': '스트라이커'},
 {'Value': 305, 'Text': '회귀', 'Class': '도화가'},
 {'Value': 306, 'Text': '만개', 'Class': '도화가'},
 {'Value': 307, 'Text': '질풍노도', 'Class': '기상술사'},
 {'Value': 308, 'Text': '이슬비', 'Class': '기상술사'},
 {'Value': 309, 'Text': '포식자', 'Class': '슬레이어'},
 {'Value': 310, 'Text': '처단자', 'Class': '슬레이어'},
 {'Value': 311, 'Text': '만월의 집행자', 'Class': '소울이터'},
 {'Value': 312, 'Text': '그믐의 경계', 'Class': '소울이터'}]
engrave_val = dict()
for etc in EtcSubs:
    engrave_val[etc['Text']] = etc['Value']

# 사용 각인 정리
engraves = {
    '전태': ['원한', '바리케이드', '안정된 상태', '예리한 둔기', '아드레날린', '전투 태세'],
    '고기': ['원한', '슈퍼 차지', '고독한 기사', '결투의 대가', '저주받은 인형', '전투 태세'],   
    '비기': ['원한', '예리한 둔기', '돌격대장', '질량 증가', '광전사의 비기', '에테르 포식자'],   
    '광기': ['원한', '예리한 둔기', '돌격대장', '달인의 저력', '광기', '에테르 포식자'] ,      
    '중수': ['원한', '바리케이드', '중력 수련', '정기 흡수', '결투의 대가', '분노의 망치'],     
    '분망': ['원한', '슈퍼 차지', '바리케이드', '분노의 망치', '결투의 대가', '아드레날린'],     
    '포식': ['원한', '기습의 대가', '돌격대장', '질량 증가', '포식자', '아드레날린'],         
    '처단': ['원한', '기습의 대가', '돌격대장', '저주받은 인형', '처단자', '아드레날린'],       
    '상소': ['원한', '상급 소환사', '예리한 둔기', '타격의 대가', '저주받은 인형', '아드레날린'],  
    '교감': ['원한', '예리한 둔기', '아드레날린', '돌격대장', '넘치는 교감', '에테르 포식자'],    
    '황후': ['원한', '아드레날린', '저주받은 인형', '돌격대장', '타격의 대가', '황후의 은총'],    
    '황제': ['원한', '황제의 칙령', '돌격대장', '질량 증가', '타격의 대가', '아드레날린'],      
    '점화': ['원한', '점화', '속전속결', '타격의 대가', '아드레날린', '에테르 포식자'],        
    '환류': ['원한', '환류', '예리한 둔기', '타격의 대가', '저주받은 인형', '아드레날린'],      
    '초심': ['원한', '예리한 둔기', '돌격대장', '질량 증가', '초심', '각성'],             
    '오의': ['원한', '예리한 둔기', '돌격대장', '저주받은 인형', '아드레날린', '오의 강화'],     
    '체술': ['원한', '극의: 체술', '기습의 대가', '예리한 둔기', '돌격대장', '아드레날린'],     
    '충단': ['원한', '예리한 둔기', '기습의 대가', '저주받은 인형', '충격 단련', '아드레날린'],   
    '세맥': ['원한', '예리한 둔기', '돌격대장', '질량 증가', '아드레날린', '세맥타통'],        
    '역천': ['원한', '예리한 둔기', '저주받은 인형', '아드레날린', '역천지체', '각성'],        
    '절정': ['원한', '절정', '돌격대장', '기습의 대가', '저주받은 인형', '아드레날린'],        
    '절제': ['원한', '절제', '돌격대장', '기습의 대가', '저주받은 인형', '아드레날린'],        
    '일격': ['원한', '기습의 대가', '예리한 둔기', '저주받은 인형', '일격필살', '아드레날린'],    
    '난무': ['원한', '기습의 대가', '예리한 둔기', '오의난무', '저주받은 인형', '아드레날린'],    
    '강무': ['원한', '예리한 둔기', '저주받은 인형', '기습의 대가', '아드레날린', '강화 무기'],   
    '핸건': ['원한', '핸드거너', '저주받은 인형', '아드레날린', '정밀 단도', '에테르 포식자'],     
    '화강': ['원한', '예리한 둔기', '아드레날린', '화력 강화', '타격의 대가', '에테르 포식자'],   
    '포강': ['원한', '예리한 둔기', '포격 강화', '저주받은 인형', '속전속결', '아드레날린'],     
    '죽습': ['원한', '예리한 둔기', '저주받은 인형', '타격의 대가', '죽음의 습격', '아드레날린'],  
    '두동': ['원한', '예리한 둔기', '두 번째 동료', '돌격대장', '타격의 대가', '아드레날린'],    
    '유산': ['원한', '예리한 둔기', '바리케이드', '돌격대장', '아드레날린', '진화의 유산'],      
    '기술': ['원한', '예리한 둔기', '돌격대장', '아르데타인의 기술', '질량 증가', '아드레날린'],   
    '피메': ['원한', '예리한 둔기', '저주받은 인형', '타격의 대가', '아드레날린', '피스메이커'],   
    '사시': ['원한', '예리한 둔기', '타격의 대가', '저주받은 인형', '사냥의 시간', '피스메이커'],  
    '질풍': ['원한', '돌격대장', '타격의 대가', '아드레날린', '질풍노도', '에테르 포식자'],      
    '슬비': ['원한', '아드레날린', '이슬비', '예리한 둔기', '타격의 대가', '에테르 포식자'],     
    '충동': ['원한', '멈출 수 없는 충동', '예리한 둔기', '저주받은 인형', '돌격대장', '아드레날린'],
    '억제': ['원한', '돌격대장', '예리한 둔기', '저주받은 인형', '완벽한 억제', '아드레날린'],    
    '달소': ['원한', '달의 소리', '기습의 대가', '예리한 둔기', '저주받은 인형', '아드레날린',],  
    '갈증': ['원한', '돌격대장', '기습의 대가', '갈증', '저주받은 인형', '아드레날린'],        
    '버스트': ['원한', '예리한 둔기', '저주받은 인형', '기습의 대가', '버스트', '아드레날린'],    
    '잔재': ['원한', '슈퍼 차지', '잔재된 기운', '기습의 대가', '저주받은 인형', '아드레날린'],   
    '만월': ['원한', '만월의 집행자', '돌격대장', '예리한 둔기', '타격의 대가', '아드레날린'],    
    '그믐': ['원한', '그믐의 경계', '예리한 둔기', '돌격대장', '아드레날린', '에테르 포식자'],    
    '축오': ['전문의', '급소 타격', '각성', '축복의 오라', '구슬동자', '심판자'],           
    '심판자': ['원한', '기습의 대가', '돌격대장', '심판자', '저주받은 인형', '아드레날린'],      
    '절구': ['각성', '절실한 구원', '전문의', '중갑 착용', '급소 타격', '폭발물 전문가'],       
    '진용': ['원한', '아드레날린', '예리한 둔기', '질량 증가', '돌격대장', '진실된 용맹'],      
    '만개': ['만개', '전문의', '각성', '중갑 착용', '급소 타격', '위기 모면'],            
    '회귀': ['원한', '예리한 둔기', '돌격대장', '회귀', '저주받은 인형', '아드레날린'],      
}

# 검색을 위한 각인 조합 생성
combs = set()

for key, value in engraves.items():
    comb = list(itertools.combinations(value[:-1], 2))
    combs.update(comb)

combs = list(combs)

# 반드시 1만 쓰는 각인들 정리
only_one = ['위기 모면', '황후의 은총', '진실된 용맹', '세맥타통', '에테르 포식자',
            '폭발물 전문가', '피스메이커', '진화의 유산', '강화 무기', '오의 강화',
            '전투 태세']

# 데이터 가져오기
result = []
start = datetime.today().strftime("%Y-%m-%d %H:%M")
df = pd.DataFrame()
la = LostArkAuction()
for comb in combs:
    comb = list(comb)
    if comb[0] in only_one:
        min_val_0 = 6
    else:
        min_val_0 = 3

    
    if comb[1] in only_one:
        min_val_1 = 6
    else:
        min_val_1 = 3
        
    for equip_code, stats in codes.items():
        for stat in stats:
            if equip_code == 200010: # 목걸이
                cond = {
                    "ItemLevelMin": 1540,
                    "ItemGradeQuality": 85,
                    "EtcOptions": [
                        {
                            "FirstOption": 2,
                            "SecondOption": stat[0],
                        },
                        {
                            "FirstOption": 2,
                            "SecondOption": stat[1],
                        },
                        {
                            "FirstOption": 3,
                            "SecondOption": engrave_val[comb[0]],
                            "MinValue": min_val_0,
                        },
                        {
                            "FirstOption": 3,
                            "SecondOption": engrave_val[comb[1]],
                            "MinValue": min_val_1,
                        }
                    ],
                    "Sort": "BIDSTART_PRICE",
                    "CategoryCode": equip_code,
                    "PageNo": 0,
                    "ItemGrade": "고대",
                    "SortCondition": "ASC"
                }
            else:
                cond = {
                    "ItemLevelMin": 1540,
                    "ItemGradeQuality": 85,
                    "EtcOptions": [
                        {
                            "FirstOption": 2,
                            "SecondOption": stat,
                        },
                        {
                            "FirstOption": 3,
                            "SecondOption": engrave_val[comb[0]],
                            "MinValue": min_val_0,
                        },
                        {
                            "FirstOption": 3,
                            "SecondOption": engrave_val[comb[1]],
                            "MinValue": min_val_1,
                        }
                    ],
                    "Sort": "BIDSTART_PRICE",
                    "CategoryCode": equip_code,
                    "PageNo": 0,
                    "ItemGrade": "고대",
                    "SortCondition": "ASC"
                }
            res = la.get_auction_items(cond)
            try:
                result.extend(res['Items'])
            except:
                pass

# 저장하기
file_cnt = len(os.listdir('/root/workspace/project/lostark/auction_data/')) - 1
day = int(start.split(' ')[0].split('-')[2])
with open('/root/workspace/project/lostark/cur_date.txt', 'r') as f:
    cur_date = int(f.read())

if day != cur_date:
    with open('/root/workspace/project/lostark/cur_date.txt', 'w') as f:
        f.write(str(day))
        file_cnt += 1

filename = f"/root/workspace/project/lostark/auction_data/lostark_auction_data{file_cnt}.csv"
df['Date'] = [start for i in range(len(result))]
df['Result'] = result

if os.path.exists(filename):
    df_origin = pd.read_csv(filename)
    df_result = pd.concat([df_origin, df], ignore_index=True)
    df_result.to_csv(filename, index=False)
else:
    df.to_csv(filename, index=False)
