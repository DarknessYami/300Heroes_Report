from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 【第一步】安装多个环境库
# pip install selenium
# pip install webdriver-manager
# pip install bs4

# 【第二步】 安装Chrome浏览器
# https://www.google.com/chrome/


# 【更新日志】—— 爬爬爬，我最会爬了!.jpg

# 2024.4.2 V0.1
# 初步建成主框架并能正常运行，目前主要功能是查询玩家最近对局的竞技力和竞技力增减。 

class ThreeHundredHeroes_Report:
    ID = ""
    
    ELO = []
    ELO_Change = []

    VOD = []
    VOD_type = []
    VOD_time = []

    def __init__(self):
# ————————————————————————————————————————————————————————————————
        #Queue
        try:
            self.PlayerIDSetup()

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.Dr = webdriver.Chrome(options=chrome_options)
            self.Dr.get("https://300report.jumpw.com/#/")

            self.ID_Search()

            self.PlayerVOD()
            self.PlayerELO()

            self.PlayerDataPrint()
        except Exception as e:
            print("[Main] Error: " + e)
        finally:
            self.Dr.quit()
# ————————————————————————————————————————————————————————————————
    def ID_Search(self):
        try:
            Search_ID_Input = self.Dr.find_element(By.CSS_SELECTOR, '.input-box input[type="text"]')
            Search_ID_Input.send_keys(self.ID)
            Search_ID_Input.send_keys(Keys.RETURN)
            Search_Confirm = self.Dr.find_element(By.CSS_SELECTOR, '.input-box .btn-search')
            Search_Confirm.click()
        except Exception as e:
            print("[ID_Search] Error: " + e)
            
    # IDsetup
    def PlayerIDSetup(self):
        try:
            self.ID = input("Input your game ID: ")
        except Exception as e:
            print("[PlayerIDSetup] Error: " + e)

    # VOD
    def PlayerVOD(self):
            try:
                list = WebDriverWait(self.Dr, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.score-list li')))
                for i in list:

                    item_vod = i.find_elements(By.CSS_SELECTOR, '.item-01.error')
                    if item_vod:
                        item_vod_val = item_vod[0].find_element(By.TAG_NAME, 'em').text
                        item_vod_type = item_vod[0].find_element(By.TAG_NAME,'span').text
                        item_vod_time = item_vod[0].find_element(By.TAG_NAME,'i').text

                        self.VOD.append(item_vod_val)
                        self.VOD_type.append(item_vod_type)
                        self.VOD_time.append(item_vod_time)
                        # print("【"+ item_vod_val +"】"+ item_vod_type +" "+ item_vod_time )
                    else:
                        item_vod = i.find_elements(By.CSS_SELECTOR, '.item-01')
                        if item_vod:
                            item_vod_val = item_vod[0].find_element(By.TAG_NAME, 'em').text
                            item_vod_type = item_vod[0].find_element(By.TAG_NAME,'span').text
                            item_vod_time = item_vod[0].find_element(By.TAG_NAME,'i').text

                            self.VOD.append(item_vod_val)
                            self.VOD_type.append(item_vod_type)
                            self.VOD_time.append(item_vod_time)
                            # print("【"+ item_vod_val +"】"+ item_vod_type +" "+ item_vod_time )
            except TimeoutException:
                print("[PlayerVOD] Error: Timeout waiting")
            except Exception as e:
                print("[PlayerVOD] Error:" + e)
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
            print("[PlayerELO] Error:" + e)

    # print data
    def PlayerDataPrint(self):
        try:
            if not (self.ELO and self.ELO_Change and self.VOD and self.VOD_type and self.VOD_time):
                print("Error: Some var are empty")
            else:
                print("—————————————————————————")
                print("\nYour ID: " + self.ID)
                num = 0
                while num < len(self.ELO):
                    print("\n【"+ self.VOD[num] +"】"+" "+self.VOD_type[num]+" "+self.VOD_time[num])
                    print("ELO: " + self.ELO[num])
                    print("ELO_Change: " + self.ELO_Change[num])
                    num+=1
                print("—————————————————————————")
        except Exception as e:
            print("[PlayerDataPrint] Error: " + e)

if __name__ == "__main__":
    Report = ThreeHundredHeroes_Report()