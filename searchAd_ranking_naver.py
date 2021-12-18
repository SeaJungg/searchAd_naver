import datetime
import os
import ssl
import urllib.request
from urllib.parse import quote, quote_plus, unquote, urlencode

currentDT = datetime.datetime.now()
import pandas as pd
from bs4 import BeautifulSoup

context = ssl._create_unverified_context() 


# 0. 뭐찾을지 받아와
print("Give me business title : ")
business_title = input()
#business_title = '유데미'
print(business_title + " start")


# 1. 엑셀파일을 가져와
print("Give me csv file name(only csv) (ex : pc_keyword) : ")
file_name = input()
#file_name = 'D:\SomeProject\pc_keyword_with_ranking_유데미.csv'
#target_file = pd.read_csv(file_name)
target_file = pd.read_csv("./" + file_name + ".csv")
output = pd.DataFrame(columns=["키워드","노출순위","단독노출"])

# 2. 행에 순차접근
for i in target_file.index:
    # 3. 검색링크 만들기
    search_word = target_file._get_value(i, '키워드')
    url = 'https://ad.search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=' + quote(search_word)
    opend_html = urllib.request.urlopen(url,context=context).read() 
    soup = BeautifulSoup(opend_html,'html.parser')
    ad_titles_with_htmlTags = soup.find_all('a', attrs={'class': 'lnk_tit'})
    
    # 3-1. 광고가 하나뿐인지 확인
    is_only = False
    if(len(ad_titles_with_htmlTags) == 1):
        is_only = True
    
    # 4. 그 중에 있는지 확인
    found_index = -1
    for index, ad_title_with_htmlTag in enumerate(ad_titles_with_htmlTags):
        ad_title = ad_title_with_htmlTag.get_text()
        if business_title in ad_title:
            found_index = index + 1
            if(is_only == True):
                output._set_value(i, '단독노출', 1)
                print(search_word + " : 단독노출 키워드입니다.")
            break
        else:
            continue
    
    # 5. 그 순위를 새로운 파일에 기록 - 순위가 없으면 -1을 기록
    output._set_value(i, '키워드', search_word)
    output._set_value(i, '노출순위', found_index)
    print(search_word, found_index)

output_name = "./out_" + business_title + " " + currentDT.strftime("%Y-%m-%d %H%M%S") + ".csv"
output.to_csv(output_name, encoding='utf-8-sig')



  


