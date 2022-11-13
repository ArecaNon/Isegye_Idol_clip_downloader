from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
import os
import os.path
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from urllib.request import urlretrieve
from datetime import date
import datetime
import warnings 
warnings.filterwarnings('ignore')
total_clip = 0

new_clip_link = []
new_clip_title = []
new_clip_count = 0

class CLIP:
    
    COMPLETED_PATH = ''
    Select_member = []
    user_id = '' 
    user_pw = ''
    start_point = 0
    end_point = 0
    date_start = ''
    date_end = ''

    driver_path = ''

    var  = {0: COMPLETED_PATH,1: Select_member,2: user_id,3: user_pw,4:start_point,5:end_point,6:date_start,7:date_start } #  Select_member / COMPLETED_PATH / user_id / user_pw
    try:
        with open('.\Setting.txt', mode = 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
            total_len = len(lines)
            for index,line in enumerate(lines):
                temp = line.split('\n')
                if index == 1:
                    mems = temp[0].split(',')
                    for m in mems:
                        var[index].append(m)
                else:
                    var[index] = temp[0]
            COMPLETED_PATH = var[0]       
            Select_member = var[1].copy() 
            user_id = var[2]  
            user_pw = var[3] 
            start_point = 0
            end_point = -1
            date_start = ''
            date_end = ''
            if(total_len > 4):   
                start_point = int(var[4])
            if(total_len > 5):    
                end_point = int(var[5])  
            if(total_len > 6):    
                date_start = var[6]  
            if(total_len > 7):    
                date_end = var[7]      
        f.close()
    except:
        print("Setting에 문제가 있습니다. 양식을 다시 확인해주세요")

    options = webdriver.ChromeOptions()

    total_list = ['title','link']
    total_index = []
    index_check_heads = ['아이네','징버거','릴파','주르르','고세구','비챤','2인이상']
    heads = ['[아이네]','[징버거]','[릴파]','[주르르]','[고세구]','[비챤]','[2인이상]']

    member_file = list()
    member_file_download = list()
    member_clip = list()
    member_clip_download = list()
    member_clip_Fail = list()

    origin_PlayList_df = [0 for i in range(7)]
    origin_PlayList_download_df = [0 for i in range(7)]
    origin_ClipList_df = [0 for i in range(7)]
    origin_ClipList_download_df = [0 for i in range(7)]
    origin_ClipList_Fail_df = [0 for i in range(7)]

    def __init__(self):
        self.chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        self.driver_path = f'./{self.chrome_ver}/chromedriver.exe'
        if os.path.exists(self.driver_path):
            print(f"chrom driver is insatlled: {self.driver_path}")
        else:
            print(f"install the chrome driver(ver: {self.chrome_ver})")
            chromedriver_autoinstaller.install(True)
        #self.options.binary_location = os.environ.get("E://창작 활동//discord bot//bot-env//chromedriver.exe")
        self.options.binary_location = os.environ.get(self.driver_path)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.add_argument("headless")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        self.get_clip()

    def get_clip(self):
        total_clip = 0

        new_clip_link = [[],[],[],[],[],[]]
        new_clip_title = [[],[],[],[],[],[]]
        new_clip_count = list()
        counting = 0#임시

        search_end = False

        for temp in self.Select_member:
            self.total_index.append(self.index_check_heads.index(temp))

        for i in range(0,7):
            my_list = list(self.heads[i][1:len(self.heads[i])-1])
            self.member_file.append(os.getcwd()+'/Data/{}/{}ArticleList.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list))) 
            self.member_file_download.append(os.getcwd()+'/Data/{}/{}ArticleList_Finish.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)))
            self.member_clip.append(os.getcwd()+'/Data/{}/{}ClipList.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list))) 
            self.member_clip_download.append(os.getcwd()+'/Data/{}/{}ClipList_Finish.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)))
            self.member_clip_Fail.append(os.getcwd()+'/Data/{}/{}ClipList_Fail.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)))

            if(not os.path.isfile(self.member_file[i])):
                os.mkdir(os.getcwd()+'/Data/{}'.format(''.join(s for s in my_list)))
                f = open(self.member_file[i],'w',encoding='utf-8-sig',newline='')
                wr = csv.writer(f)
                wr.writerow([self.total_list[0], self.total_list[1]])
                f.close()

            if(not os.path.isfile(self.member_file_download[i])):
                f = open(self.member_file_download[i],'w',encoding='utf-8-sig',newline='')
                wr = csv.writer(f)
                wr.writerow([self.total_list[0], self.total_list[1]])
                f.close()

            if(not os.path.isfile(self.member_clip[i])):
                f = open(self.member_clip[i],'w',encoding='utf-8-sig',newline='')
                wr = csv.writer(f)
                wr.writerow([self.total_list[0], self.total_list[1]])
                f.close()

            if(not os.path.isfile(self.member_clip_download[i])):
                f = open(self.member_clip_download[i],'w',encoding='utf-8-sig',newline='')
                wr = csv.writer(f)
                wr.writerow([self.total_list[0], self.total_list[1]])
                f.close()

            if(not os.path.isfile(self.member_clip_Fail[i])):
                f = open(self.member_clip_Fail[i],'w',encoding='utf-8-sig',newline='')
                wr = csv.writer(f)
                wr.writerow([self.total_list[0], self.total_list[1]])
                f.close()

        driver = webdriver.Chrome(self.driver_path,options=self.options)
        #driver = webdriver.Chrome('E://창작 활동//discord bot//bot-env//chromedriver.exe',options=self.options)   
        
        driver.implicitly_wait(2)

        # 1. 네이버 이동
        driver.get('http://naver.com')

        # 2. 로그인 버튼 클릭
        elem = driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[3]/div/div[2]/a')
        elem.click()

        # 3. id 복사 붙여넣기
        elem_id = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[1]/input')
        elem_id.click()
        pyperclip.copy(self.user_id)
        elem_id.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 4. pw 복사 붙여넣기
        elem_pw = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[2]/input')
        elem_pw.click()
        pyperclip.copy(self.user_pw)
        elem_pw.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 5. 로그인 버튼 클릭
        driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[7]/button').click()

        # 핫클립 게시판으로 접속
        for now_mem in self.total_index:
            baseurls = ['https://cafe.naver.com/steamindiegame?iframe_url=/ArticleList.nhn%3Fsearch.clubid=27842958%26search.menuid=331%26userDisplay=50%26search.headid=581%26search.boardtype=L%26search.totalCount=501%26search.cafeId=27842958%26search.page=1',
            'https://cafe.naver.com/steamindiegame?iframe_url=/ArticleList.nhn%3Fsearch.clubid=27842958%26search.menuid=331%26userDisplay=50%26search.headid=584%26search.boardtype=L%26search.totalCount=501%26search.cafeId=27842958%26search.page=1',
            'https://cafe.naver.com/steamindiegame?iframe_url=/ArticleList.nhn%3Fsearch.clubid=27842958%26search.menuid=331%26userDisplay=50%26search.headid=583%26search.boardtype=L%26search.totalCount=501%26search.cafeId=27842958%26search.page=1',
            'https://cafe.naver.com/steamindiegame?iframe_url=/ArticleList.nhn%3Fsearch.clubid=27842958%26search.menuid=331%26userDisplay=50%26search.headid=586%26search.boardtype=L%26search.totalCount=501%26search.cafeId=27842958%26search.page=1',
            'https://cafe.naver.com/steamindiegame?iframe_url=/ArticleList.nhn%3Fsearch.clubid=27842958%26search.menuid=331%26userDisplay=50%26search.headid=585%26search.boardtype=L%26search.totalCount=501%26search.cafeId=27842958%26search.page=1',
            'https://cafe.naver.com/steamindiegame?iframe_url=/ArticleList.nhn%3Fsearch.clubid=27842958%26search.menuid=331%26userDisplay=50%26search.headid=582%26search.boardtype=L%26search.totalCount=501%26search.cafeId=27842958%26search.page=1',
            'https://cafe.naver.com/steamindiegame?iframe_url=/ArticleList.nhn%3Fsearch.clubid=27842958%26search.menuid=331%26userDisplay=50%26search.headid=619%26search.boardtype=L%26search.totalCount=501%26search.cafeId=27842958%26search.page=1']
            
            driver.get(baseurls[now_mem])  

            driver.switch_to.frame('cafe_main')
            
            tempsoup = bs(driver.page_source,'html.parser')
            buttons = tempsoup.find(class_='prev-next')
            count = len(buttons.find_all('a'))
            try:
                button = buttons.find(class_='pgR')
            except:
                button = NULL
                print('fail to find Next button --> last page')
            page = self.start_point
            while(True):   
                new_df = list()
                for i in range(0,7):
                    new_df.append(pd.DataFrame(columns=[self.total_list[0], self.total_list[1]]))

                if(count > 10):
                    pagenum = 10
                elif(page >= 10):
                    pagenum = count-1
                else:
                    pagenum = count
                
                for i in range(pagenum):
                    if(page >= self.end_point and self.end_point != -1):
                        search_end = True
                        break
                    page += 1
                    for member in self.total_index:
                        my_list = list(self.heads[member][1:len(self.heads[member])-1])
                        self.origin_PlayList_df[member] = pd.read_csv('./Data/{}/{}ArticleList.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')
                        self.origin_PlayList_download_df[member] = pd.read_csv('./Data/{}/{}ArticleList_Finish.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')

                    baseurl = baseurls[now_mem]
                    baseurl = baseurl[0:len(baseurl)-1]+'{}'.format(page) #팬영상 - 노래 모음 검색

                    driver.get(baseurl)  
                    driver.switch_to.frame('cafe_main')

                    soup = bs(driver.page_source,'html.parser')

                    #soup = soup.find(class_='article-board result-board m-tcol-c')
                    soup = soup.find_all(class_='article-board m-tcol-c')[1]

                    datas = soup.find_all(class_='td_article')
                    data_names = soup.find_all(class_='td_name')
                    data_dates = soup.find_all(class_='td_date')

                    p = re.compile('[0-9][0-9][0-9][0-9]')

                    j = 1

                    len_ = len(datas)
                    for data in datas:
                        article_title = datas[len_-j].find(class_='article')
                        index = now_mem
                        article_name = data_names[len_-j].find(class_='m-tcol-c')
                        link = article_title.get('href')
                        date_check = p.match(data_dates[len_-j].text)
                        
                        if(date_check):
                            article_date = data_dates[len_-j].text
                            article_date = article_date.split('.')
                            article_date = date(int(article_date[0]), int(article_date[1]), int(article_date[2]))
                        else:
                            today = datetime.datetime.now()
                            today = today.date()
                            article_date = today
                        if(self.date_start != '' and self.date_start != ''):
                            temp_s = self.date_start.split('.')
                            temp_s = date(int(temp_s[0]),int(temp_s[1]),int(temp_s[2]))
                            temp_e = self.date_end.split('.')
                            temp_e = date(int(temp_e[0]),int(temp_e[1]),int(temp_e[2]))
                            if(article_date < temp_s or article_date > temp_e):
                                continue

                        article_title = article_title.get_text().strip()

                        link_list = re.split('&|=', link)
                        link = link_list[11] #27  11 : 팬영상 작성자 검색 # 25 : 전체게시판 작성자 검색 # 팬영상 게시글+댓글 : 29 #핫클립 전체 검색 : 09 # 핫클립 전체 검색(50page) : 11
                        try:
                            checking_number = int(link)
                        except:
                            j += 1
                            continue

                        string_list = re.split(r'\s+', article_title)
                        title = ""

                        for data in string_list:
                            title += data
                            title += ' '
                        j += 1

                        title = re.sub("\\ufeff",'',title)
                        title = re.sub("\\\\ufeff",'',title)
                        title = re.sub("\\\\u0027",'\'',title)
                        title = re.sub("\\u0027",'\'',title)
                        title = re.sub("\\\\u0026",'&',title)
                        title = re.sub("\\u0026",'&',title)
                        title = re.sub("\\u003E",'>',title)
                        title = re.sub("\\\\u003E",'>',title)
                        title = re.sub("\\\\",'',title)
                        re_title = re.sub('[?/:|,<>] ',' ',title)
                        new_df[index] = new_df[index].append({'title':re_title, 'link': 'https://cafe.naver.com/steamindiegame'+ '/' +link}, ignore_index=True)             
                    #for member in self.total_index:
                    concat_df = pd.concat([self.origin_PlayList_df[now_mem], new_df[now_mem]])
                    concat_df = pd.concat([self.origin_PlayList_df[now_mem], concat_df])
                    concat_df = pd.concat([self.origin_PlayList_download_df[now_mem], concat_df])
                    concat_df = pd.concat([self.origin_PlayList_download_df[now_mem], concat_df])
                    concat_df = concat_df.drop_duplicates(['link'],keep=False)    
                    total_clip = len(self.origin_PlayList_df[now_mem]) + len(concat_df) 
                    #단순화 할 것
                    temp = len(self.origin_PlayList_df[now_mem])

                    new_clip_count = total_clip-temp#임시
                    print("Now Page : {}".format(page))
                    print(self.heads[now_mem],"'s New: ",new_clip_count)
                    my_list = list(self.heads[now_mem][1:len(self.heads[now_mem])-1])
                    concat_df.to_csv('./Data/{}/{}ArticleList.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),mode = 'a', header=False, index=False)
                if(not button):
                    break
                else:
                    try:
                        driver.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/a[{0}]'.format(count)).click()
                    except:
                        break
                    #driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/a[{0}]'.format(count)).click()
                tempsoup = bs(driver.page_source,'html.parser')
                buttons = tempsoup.find(class_='prev-next')
                count = len(buttons.find_all('a'))
                try:
                    button = buttons.find(class_='pgR')
                except:
                    button = NULL
                    print('fail to find Next button --> last page')
                new_df.clear()
        driver.close()

        for i in self.total_index:
            my_list = list(self.heads[i][1:len(self.heads[i])-1])
            self.origin_PlayList_df[i] = pd.read_csv('./Data/{}/{}ArticleList.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')
            self.origin_PlayList_download_df[i] = pd.read_csv('./Data/{}/{}ArticleList_Finish.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')
            print(self.heads[i])
            for (idx,title) in enumerate(self.origin_PlayList_df[i]['title']):
                print('{} : {}'.format(idx+1, title))
            print('\n') 
            
        self.check_article()
        self.download_video()

        new_clip_title.clear()
        new_clip_link.clear()
        print("종료")
        return
        
    
    def check_article(self):
        j = 0
        new_df = list()
        for i in range(0,7):
            new_df.append(pd.DataFrame(columns=[self.total_list[0], self.total_list[1]]))
        #driver = webdriver.Chrome('E://창작 활동//discord bot//bot-env//chromedriver.exe',options=self.options)   
        driver = webdriver.Chrome(self.driver_path,options=self.options)
        driver.implicitly_wait(2)

        # 1. 네이버 이동
        driver.get('http://naver.com')

        # 2. 로그인 버튼 클릭
        elem = driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[3]/div/div[2]/a')
        elem.click()

        # 3. id 복사 붙여넣기
        elem_id = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[1]/input')
        elem_id.click()
        pyperclip.copy(self.user_id)
        elem_id.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 4. pw 복사 붙여넣기
        elem_pw = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[2]/input')
        elem_pw.click()
        pyperclip.copy(self.user_pw)
        elem_pw.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 5. 로그인 버튼 클릭
        driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[7]/button').click()
        for member in self.total_index:
            my_list = list(self.heads[member][1:len(self.heads[member])-1])
            name = ''.join(s for s in my_list)
            for article_ in self.origin_PlayList_df[member]['link']:
                delete_article = False
                baseurl = article_
                self.origin_ClipList_df[member] = pd.read_csv('./Data/{}/{}ClipList.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')
                self.origin_ClipList_download_df[member] = pd.read_csv('./Data/{}/{}ClipList_Finish.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')
                try:
                    driver.get(baseurl)
                except Exception as e:
                    print(e)
                    continue  
                driver.switch_to.frame('cafe_main')
                
                all_clips_in_page = driver.find_elements(By.CLASS_NAME,'se-oglink-info')
                for clip_page in all_clips_in_page:
                    temp_link = clip_page.get_attribute('href')
                    temp = clip_page.find_element(By.CLASS_NAME,'se-oglink-title').text
                    temp_title = self.change_title(temp)
                    new_df[member] = new_df[member].append({'title':temp_title, 'link': temp_link}, ignore_index=True)
                concat_df = pd.concat([self.origin_ClipList_df[member], new_df[member]])
                concat_df = pd.concat([self.origin_ClipList_df[member], concat_df])
                concat_df = pd.concat([self.origin_ClipList_download_df[member], concat_df])
                concat_df = pd.concat([self.origin_ClipList_download_df[member], concat_df])
                concat_df = concat_df.drop_duplicates(['link'],keep=False)    
                print("클립 갯수 : ",len(concat_df) + len(self.origin_ClipList_df[member]))
                concat_df.to_csv('./Data/{}/{}ClipList.csv'.format(name,name),mode = 'a', header=False, index=False)
                
                temp_article = self.origin_PlayList_df[member][self.origin_PlayList_df[member]['link'] == article_]
                self.origin_PlayList_df[member] = self.origin_PlayList_df[member].drop(temp_article.index)
                    
                os.remove('./Data/{}/{}ArticleList.csv'.format(name,name))
                f = open('./Data/{}/{}ArticleList.csv'.format(name,name),'w',encoding='utf-8',newline='')
                wr = csv.writer(f)
                wr.writerow(['title','link'])
                f.close()
                    
                self.origin_PlayList_df[member].to_csv('./Data/{}/{}ArticleList.csv'.format(name,name),mode = 'a', header=False, index=False)
                temp_article = pd.DataFrame(temp_article)
                self.origin_PlayList_download_df[member] = pd.concat([self.origin_PlayList_download_df[member], temp_article])
                os.remove('./Data/{}/{}ArticleList_Finish.csv'.format(name,name))
                f = open('./Data/{}/{}ArticleList_Finish.csv'.format(name,name),'w',encoding='utf-8',newline='')
                wr = csv.writer(f)
                wr.writerow(['title','link'])
                f.close()
                self.origin_PlayList_download_df[member].to_csv('./Data/{}/{}ArticleList_Finish.csv'.format(name,name),mode = 'a', header=False, index=False)
                print("{} 클립 동기화 완료".format(name))
        driver.close()
        print('Finish!!')
        


    def download_video(self):
       
        driver = webdriver.Chrome(self.driver_path,options=self.options)
        driver.implicitly_wait(2)
        
        for member in self.total_index:
            my_list = list(self.heads[member][1:len(self.heads[member])-1])
            self.origin_ClipList_df[member] = pd.read_csv('./Data/{}/{}ClipList.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')
            self.origin_ClipList_download_df[member] = pd.read_csv('./Data/{}/{}ClipList_Finish.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')
            self.origin_ClipList_Fail_df[member] = pd.read_csv('./Data/{}/{}ClipList_Fail.csv'.format(''.join(s for s in my_list),''.join(s for s in my_list)),encoding='utf-8-sig')
        j = 0
        for member in self.total_index:
            my_list = list(self.heads[member][1:len(self.heads[member])-1])
            name = ''.join(s for s in my_list)
            directory = self.COMPLETED_PATH+'/{}'.format(name)

            if(not os.path.isdir(directory)):
                os.mkdir(directory)

            for article_ in self.origin_ClipList_df[member]['link']:
                driver.get(article_)

                time.sleep(2)
                
                vid_url_element = driver.find_element(By.TAG_NAME,'video')
                vid_url = vid_url_element.get_attribute('src')

                soup = bs(driver.page_source,'html.parser')

                try:
                    vid_title = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/span').text 
                except:
                    print("{} : 트위치 클립이 아니거나 문제가 있습니다.".format(vid_url))
                    j += 1
                    temp_article = self.origin_ClipList_df[member][self.origin_ClipList_df[member]['link'] == article_]
                    self.origin_ClipList_df[member] = self.origin_ClipList_df[member].drop(temp_article.index)
                        
                    os.remove('./Data/{}/{}ClipList.csv'.format(name,name))
                    f = open('./Data/{}/{}ClipList.csv'.format(name,name),'w',encoding='utf-8',newline='')
                    wr = csv.writer(f)
                    wr.writerow(['title','link'])
                    f.close()
                        
                    self.origin_ClipList_df[member].to_csv('./Data/{}/{}ClipList.csv'.format(name,name),mode = 'a', header=False, index=False)
                    temp_article = pd.DataFrame(temp_article)

                    self.origin_ClipList_download_df[member] = pd.concat([self.origin_ClipList_download_df[member], temp_article])
                    os.remove('./Data/{}/{}ClipList_Finish.csv'.format(name,name))
                    f = open('./Data/{}/{}ClipList_Finish.csv'.format(name,name),'w',encoding='utf-8',newline='')
                    wr = csv.writer(f)
                    wr.writerow(['title','link'])
                    f.close()
                    self.origin_ClipList_download_df[member].to_csv('./Data/{}/{}ClipList_Finish.csv'.format(name,name),mode = 'a', header=False, index=False)

                    self.origin_ClipList_Fail_df[member] = pd.concat([self.origin_ClipList_Fail_df[member], temp_article])
                    os.remove('./Data/{}/{}ClipList_Fail.csv'.format(name,name))
                    f = open('./Data/{}/{}ClipList_Fail.csv'.format(name,name),'w',encoding='utf-8',newline='')
                    wr = csv.writer(f)
                    wr.writerow(['title','link'])
                    f.close()
                    self.origin_ClipList_Fail_df[member].to_csv('./Data/{}/{}ClipList_Fail.csv'.format(name,name),mode = 'a', header=False, index=False)
                    continue
                vid_title = self.change_title(vid_title)
                try:
                    vid_date = soup.select_one('meta[property="og:video:release_date"]')['content']
                    vid_date = vid_date[0:vid_date.find('T')]
                except:
                    vid_date ="20xxXXxx"
                vid_date = self.change_title(vid_date)
                try:
                    urlretrieve(vid_url, directory+'/['+vid_date+']'+vid_title+'.mp4')
                except:
                    print("{} : 다운로드에 실패했습니다.".format(vid_url))
                    j += 1
                    temp_article = self.origin_ClipList_df[member][self.origin_ClipList_df[member]['link'] == article_]
                    self.origin_ClipList_df[member] = self.origin_ClipList_df[member].drop(temp_article.index)
                        
                    os.remove('./Data/{}/{}ClipList.csv'.format(name,name))
                    f = open('./Data/{}/{}ClipList.csv'.format(name,name),'w',encoding='utf-8',newline='')
                    wr = csv.writer(f)
                    wr.writerow(['title','link'])
                    f.close()
                        
                    self.origin_ClipList_df[member].to_csv('./Data/{}/{}ClipList.csv'.format(name,name),mode = 'a', header=False, index=False)
                    temp_article = pd.DataFrame(temp_article)
                    self.origin_ClipList_download_df[member] = pd.concat([self.origin_ClipList_download_df[member], temp_article])
                    os.remove('./Data/{}/{}ClipList_Finish.csv'.format(name,name))
                    f = open('./Data/{}/{}ClipList_Finish.csv'.format(name,name),'w',encoding='utf-8',newline='')
                    wr = csv.writer(f)
                    wr.writerow(['title','link'])
                    f.close()
                    self.origin_ClipList_download_df[member].to_csv('./Data/{}/{}ClipList_Finish.csv'.format(name,name),mode = 'a', header=False, index=False)

                    self.origin_ClipList_Fail_df[member] = pd.concat([self.origin_ClipList_Fail_df[member], temp_article])
                    os.remove('./Data/{}/{}ClipList_Fail.csv'.format(name,name))
                    f = open('./Data/{}/{}ClipList_Fail.csv'.format(name,name),'w',encoding='utf-8',newline='')
                    wr = csv.writer(f)
                    wr.writerow(['title','link'])
                    f.close()
                    self.origin_ClipList_Fail_df[member].to_csv('./Data/{}/{}ClipList_Fail.csv'.format(name,name),mode = 'a', header=False, index=False)
                    continue
                j += 1
                print('Download Complete : ',article_)
                print('download : {0}\n'.format(j))
                temp_article = self.origin_ClipList_df[member][self.origin_ClipList_df[member]['link'] == article_]
                self.origin_ClipList_df[member] = self.origin_ClipList_df[member].drop(temp_article.index)
                    
                os.remove('./Data/{}/{}ClipList.csv'.format(name,name))
                f = open('./Data/{}/{}ClipList.csv'.format(name,name),'w',encoding='utf-8',newline='')
                wr = csv.writer(f)
                wr.writerow(['title','link'])
                f.close()
                    
                self.origin_ClipList_df[member].to_csv('./Data/{}/{}ClipList.csv'.format(name,name),mode = 'a', header=False, index=False)
                temp_article = pd.DataFrame(temp_article)
                self.origin_ClipList_download_df[member] = pd.concat([self.origin_ClipList_download_df[member], temp_article])
                os.remove('./Data/{}/{}ClipList_Finish.csv'.format(name,name))
                f = open('./Data/{}/{}ClipList_Finish.csv'.format(name,name),'w',encoding='utf-8',newline='')
                wr = csv.writer(f)
                wr.writerow(['title','link'])
                f.close()
                self.origin_ClipList_download_df[member].to_csv('./Data/{}/{}ClipList_Finish.csv'.format(name,name),mode = 'a', header=False, index=False)
                print("다운로드 동기화 완료")
            print("{} 전 파일 다운 완료".format(name))    
                
    def change_title(self,title):
        title = re.sub("\\ufeff",'',title)
        title = re.sub("\\\\ufeff",'',title)
        title = re.sub("\\\\u0027",'\'',title)
        title = re.sub("\\u0027",'\'',title)
        title = re.sub("\\\\u0026",'&',title)
        title = re.sub("\\u0026",'&',title)
        title = re.sub("\\u003E",'>',title)
        title = re.sub("\\\\u003E",'>',title)
        title = re.sub("\\\\",'',title)
        title = re.sub('[?/:|,<>] ',' ',title)
        title = re.sub('\?','',title)
        title = re.sub('\"','',title)
        return title
        
if __name__ == "__main__":
    CLIP()
