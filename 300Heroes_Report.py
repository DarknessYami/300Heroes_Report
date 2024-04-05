from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import json

# 【更新日志】—— 爬爬爬，我最会爬了!.jpg

# 2024.4.2 V0.1
# 初步建成主框架并能正常运行，目前主要功能是查询玩家最近对局的竞技力和竞技力增减。 

# 2024.4.3 V0.2
# 新增PlayerHeroID方法，查询对局英雄的ID。
# 新增HeroID.json文件记录英雄id和名字。但只有144个英雄记录，实际游戏上有240+个英雄（这方面需要补足）
# 新增PlayerHeroName方法，将PlayerHeroID方法保存的HeroID通过HeroID.json数据提取对应英雄ID的英雄名称。


class ThreeHundredHeroes_Report:
    ID = "雪樱ッ乳液狂飙"
    
    ELO = []
    ELO_Change = []

    WOL = []
    WOL_type = []
    WOL_time = []

    HeroID = []
    HeroName = []
    def __init__(self):
# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        #Queue
        try:
            # self.PlayerIDSetup()

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.Dr = webdriver.Chrome(options=chrome_options)
            self.Dr.get("https://300report.jumpw.com/#/")

            self.ID_Search()

            self.PlayerWOL()
            self.PlayerELO()

            self.PlayerHeroID()
            self.PlayerHeroName()

            self.PlayerDataPrint()
        except Exception as e:
            print("[Main] Error: " + str(e))
        finally:
            self.Dr.quit()
# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def ID_Search(self):
        try:
            Search_ID_Input = self.Dr.find_element(By.CSS_SELECTOR, '.input-box input[type="text"]')
            Search_ID_Input.send_keys(self.ID)
            Search_ID_Input.send_keys(Keys.RETURN)
            Search_Confirm = self.Dr.find_element(By.CSS_SELECTOR, '.input-box .btn-search')
            Search_Confirm.click()
        except Exception as e:
            print("[ID_Search] Error: " + str(e))

    # IDsetup
    def PlayerIDSetup(self):
        try:
            self.ID = input("Input your game ID: ")
        except Exception as e:
            print("[PlayerIDSetup] Error: " + str(e))

    # WIN OR LOSE
    def PlayerWOL(self):
            try:
                list = WebDriverWait(self.Dr, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.score-list li')))
                for i in list:

                    item_WOL = i.find_elements(By.CSS_SELECTOR, '.item-01.error')
                    if item_WOL:
                        item_WOL_val = item_WOL[0].find_element(By.TAG_NAME, 'em').text
                        item_WOL_type = item_WOL[0].find_element(By.TAG_NAME,'span').text
                        item_WOL_time = item_WOL[0].find_element(By.TAG_NAME,'i').text

                        self.WOL.append(item_WOL_val)
                        self.WOL_type.append(item_WOL_type)
                        self.WOL_time.append(item_WOL_time)
                        # print("【"+ item_WOL_val +"】"+ item_WOL_type +" "+ item_WOL_time )
                    else:
                        item_WOL = i.find_elements(By.CSS_SELECTOR, '.item-01')
                        if item_WOL:
                            item_WOL_val = item_WOL[0].find_element(By.TAG_NAME, 'em').text
                            item_WOL_type = item_WOL[0].find_element(By.TAG_NAME,'span').text
                            item_WOL_time = item_WOL[0].find_element(By.TAG_NAME,'i').text

                            self.WOL.append(item_WOL_val)
                            self.WOL_type.append(item_WOL_type)
                            self.WOL_time.append(item_WOL_time)
                            # print("【"+ item_WOL_val +"】"+ item_WOL_type +" "+ item_WOL_time )
            except TimeoutException:
                print("[PlayerWOL] Error: Timeout waiting")
            except Exception as e:
                print("[PlayerWOL] Error:" + str(e))
    # ELO 
    def PlayerELO(self):
        try:
            list = WebDriverWait(self.Dr, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.score-list li')))
            for i in list:
                player_elo = i.find_element(By.CSS_SELECTOR, '.center.elo')
                if player_elo:
                    player_elo_val = player_elo.text.split()
                    self.ELO.append(player_elo_val[0])
                    self.ELO_Change.append(player_elo_val[1])
                    # print("ELO: " + self.ELO)
                    # print("ELO_Change: " + self.ELO_Change)
        except TimeoutException:
            print("[PlayerELO] Error: Timeout waiting")  
        except Exception as e:
            print("[PlayerELO] Error:" + str(e))

# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    def PlayerHeroID(self):
        try:
            list = WebDriverWait(self.Dr, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.score-list li')))
            for i in list:
                player_heroid = i.find_element(By.CSS_SELECTOR, '.img img').get_attribute("src")
                player_herotext = re.search(r'chara_0(\d+)\.png', player_heroid)
                if player_herotext:
                    heroid = player_herotext.group(1)
                    self.HeroID.append(heroid)
                else:
                    print("[PlayerHeroID] Error: Message lost")
        except Exception as e:
            print("[PlayerHeroID] Error: " + str(e))

    def PlayerHeroName(self):
        try:
            with open('HeroID.json', 'r', encoding='utf-8') as jf:
                Data_load = json.load(jf)
                if Data_load:
                    for hero_id in self.HeroID:
                        if hero_id in Data_load:
                            self.HeroName.append(Data_load[hero_id]["NAME"])
                        else:
                            self.HeroName.append("[PlayerHeroName] Error: Data_load id not found")

                else:
                    print("[PlayerHeroName] Error: Data_load lost")
        except Exception as e:
            print("[PlayerHeroName] Error: " + str(e))


# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # print data
    def PlayerDataPrint(self):
        try:
            if not (self.ELO and self.ELO_Change and self.WOL and self.WOL_type and self.WOL_time):
                print("Error: Some var are empty")
            else:
                print("—————————————————————————")
                print("\nYour ID: " + self.ID)
                num = 0
                while num < len(self.ELO):
                    print("\n【"+ self.WOL[num] +"】"+" "+self.WOL_type[num]+" "+self.WOL_time[num])
                    print("HeroID: " + self.HeroID[num])
                    print("HeroName: " + self.HeroName[num])
                    print("ELO: " + self.ELO[num])
                    print("ELO_Change: " + self.ELO_Change[num])
                    num+=1
                print("—————————————————————————")
        except Exception as e:
            print("[PlayerDataPrint] Error: " + str(e))
# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

if __name__ == "__main__":
    Report = ThreeHundredHeroes_Report()