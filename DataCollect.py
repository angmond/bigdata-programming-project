import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime

# 이 코드는 api로부터 필요한 데이터를 수집 및 전처리하는 코드이다.

# 선거id와 선거코드 정보 받아오기
pageNo = 1
CommerceInfor = {}

sgIdlist = []
sgTypecodelist = []

while pageNo <= 5:
    url = 'http://apis.data.go.kr/9760000/CommonCodeService/getCommonSgCodeList'
    params ={'serviceKey' : '서비스키',
             'pageNo' : pageNo, 'numOfRows' : '10' }
    
    response = requests.get(url, params=params)
    html = response.text
    soup = bs(html, 'html.parser')

    sgIds = soup.find_all('sgid')
    sgTypecodes = soup.find_all('sgtypecode')

    for sgId in sgIds:
        sgIdlist.append(sgId.text)
    for sgTypecode in sgTypecodes:
        sgTypecodelist.append(sgTypecode.text)
        
    pageNo+=1

CommerceInfor['sgId'] = sgIdlist
CommerceInfor['sgTypecode'] = sgTypecodelist

df = pd.DataFrame(CommerceInfor)

now = datetime.now()
current_date = now.strftime("%Y%m%d")

# 선거공약 정보 조회 서비스가 2020-01-20 이후의 데이터만 제공하므로
df1 = df[(df['sgId'] >= '20200120') & (df['sgId'] < current_date)]
# 1, 3, 4, 11 이외 코드는 선거공약서를 제출하지 않으므로
df2 = df1[(df1['sgTypecode'] == '1') | (df1['sgTypecode'] == '3') |
          (df1['sgTypecode'] == '4') | (df1['sgTypecode'] == '11') ]


# 당선인 정보(선거id, 선거코드, 후보자id) 받아오기
CommerceInfor2 = {}

sgIdlist2 = []
sgTypecodelist2 = []
huboidlist = []

for i in range(len(df2)):
    sgId = df2.iloc[i]['sgId']
    sgTypecode = df2.iloc[i]['sgTypecode']

    url = 'http://apis.data.go.kr/9760000/WinnerInfoInqireService2/getWinnerInfoInqire'
    params ={'serviceKey' : '서비스키',
             'pageNo' : '1', 'numOfRows' : '10', 'sgId' : sgId, 'sgTypecode' : sgTypecode}
    
    response = requests.get(url, params=params)
    html = response.text
    soup = bs(html, 'html.parser')
    
    sgIds2 = soup.find_all('sgid')
    sgTypecodes2 = soup.find_all('sgtypecode')
    huboids2 = soup.find_all('huboid')
    
    for sgId in sgIds2:
        sgIdlist2.append(sgId.text)
    for sgTypecode in sgTypecodes2:
        sgTypecodelist2.append(sgTypecode.text)
    for huboid in huboids2:
        huboidlist.append(huboid.text)

CommerceInfor2['sgId'] = sgIdlist2
CommerceInfor2['sgTypecode'] = sgTypecodelist2
CommerceInfor2['huboid'] = huboidlist

df3 = pd.DataFrame(CommerceInfor2)

# 선거공약 정보 받아오기ㅇ
CommerceInfor3 = {}

# sgIdlist3 = []
# sgTypecodelist3 = []
# cnddtIdlist = []
prmsTitle_list = []
# prmmCont_list = []

for i in range(len(df3)):
    sgId2 = df3.iloc[i]['sgId']
    sgTypecode2 = df3.iloc[i]['sgTypecode']
    huboid = df3.iloc[i]['huboid']
    
    url = 'http://apis.data.go.kr/9760000/ElecPrmsInfoInqireService/getCnddtElecPrmsInfoInqire'
    params ={'serviceKey' : '서비스키',
             'pageNo' : '1', 'numOfRows' : '10', 'sgId' : sgId2, 'sgTypecode' : sgTypecode2, 'cnddtId' : huboid }
    
    response = requests.get(url, params=params)
    html = response.text
    soup = bs(html, 'html.parser')

    prmstitles1 = soup.find_all('prmstitle1')
    prmstitles2 = soup.find_all('prmstitle2')
    prmstitles3 = soup.find_all('prmstitle3')
    prmstitles4 = soup.find_all('prmstitle4')
    prmstitles5 = soup.find_all('prmstitle5')

    for prmstitle1 in prmstitles1:
        prmsTitle_list.append(prmstitle1.text)
    for prmstitle2 in prmstitles2:
        prmsTitle_list.append(prmstitle2.text)
    for prmstitle3 in prmstitles3:
        prmsTitle_list.append(prmstitle3.text)
    for prmstitle4 in prmstitles4:
        prmsTitle_list.append(prmstitle4.text)
    for prmstitle5 in prmstitles5:
        prmsTitle_list.append(prmstitle5.text)

CommerceInfor3['prmsTitle'] = prmsTitle_list

df4 = pd.DataFrame(CommerceInfor3)

df4.to_csv('data.csv', encoding = 'utf-8', index = False)
