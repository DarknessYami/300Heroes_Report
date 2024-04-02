from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ThreeHundredHeroes_Report:
    ID = ""
    
    ELO = []
    ELO_Change = []

    VOD = []
    VOD_type = []
    VOD_time = []


    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.Dr = webdriver.Chrome(options=chrome_options)
        self.Dr.get("https://300report.jumpw.com/#/")
# ————————————————————————————————————————————————————————————————
        #Queue
        self.PlayerIDSetup()
        self.ID_Search()

        self.PlayerVOD()
        self.PlayerELO()


# ————————————————————————————————————————————————————————————————
        self.Dr.quit()
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


if __name__ == "__main__":
    Report = ThreeHundredHeroes_Report()
