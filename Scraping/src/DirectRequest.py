# Para abrir o webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# Para esperar o elemento aparecer
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Para manipular a página
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs


from datetime import datetime
from time import sleep
import subprocess
import re
from src.classes import Matches

class Request:
    #Abre o driver
    def open_browser(self): 
        subprocess.Popen(
            '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --log-level=3 --remote-debugging-port=9222',
            shell=True,
        )
        sleep(1)
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.options.add_argument("disable-infobars")
        self.options.add_argument('--disable-application-cache')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=self.options
        )
        # self.browser.maximize_window()

    #Fecha o driver
    def quit_browser(self): 
        self.browser.quit()

    #Abre o site base e o espera carregar
    def open_site(self): 
        self.browser.get("https://www.sofascore.com/pt/torneio/futebol/brazil/brasileirao-serie-a/325#id:58766")
        self.wait_for_page_load()
        print("Página Carregada")

    #Pega o link das páginas com detalhes dos jogos baseado no last_date
    def get_link_by_date(self,last_date): 
        def get_game_list() -> list:
            new_games = []
            for i in range(10,0,-1):
                game = self.browser.find_element(By.XPATH,f'//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[3]/div/div/div[1]/div/div[2]/div[{i}]/a')
                
                date = re.findall(regex,game.text)
                state = re.search("F2°T", game.text)
                print(date,' ',state)

                game_date = datetime.strptime(date[0], "%d/%m/%y") if date else datetime.combine(datetime.now().date(), datetime.min.time())
                if game_date <= last_date:
                    break
                elif state:
                    new_games.append(game.get_attribute('href'))         

                if i == 1:
                    self.browser.find_element(By.CLASS_NAME, 'iCnTrv').click()
                    sleep(1)
                    new_games += get_game_list()

            return new_games       
         
        last_date = datetime.strptime(last_date, "%d/%m/%y")
        regex = r'\b\d{2}/\d{2}/\d{2}\b'

        self.wait_element('//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[2]/div[1]',5,'xpath').click()
        self.wait_element('sc-929a8fc9-0',15,'class')

        games = get_game_list()        

        return games

    #Pega os dados de um jogo
    def get_game_data(self,link):        
        self.browser.get(link)
        self.wait_for_page_load()
        print("Página Carregada")

        #Pegando avaliação dos jogadores
        self.browser.find_element(By.XPATH,'//*[@id="__next"]/main/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[2]').click()
        self.wait_element('.jbURkg',5,'css')

        home_button, away_button = self.browser.find_elements(By.CLASS_NAME,'jbURkg') 

        home_button.click()
        sleep(2)
        players_home = self.browser.find_elements(By.CSS_SELECTOR, 'tr.iFVxYz')
        player_score = [[],[]]

        for player in players_home[1:]:
            tds = player.find_elements(By.TAG_NAME, 'td')
            player_score[0].append({
                "name": tds[1].text,
                "score": tds[-1].accessible_name,
                "injurie": False
            })

        away_button.click()
        sleep(2)
        players_away = self.browser.find_elements(By.CSS_SELECTOR, 'tr.iFVxYz')

        for player in players_away[1:]:
            tds = player.find_elements(By.TAG_NAME, 'td')
            player_score[1].append({
                "name": tds[1].text,
                "score": tds[-1].accessible_name,
                "injurie": False
            })

        # #Pegando nome e placar dos times
        text_team_scoreboard = self.browser.find_element(By.CLASS_NAME,'dZNeJi').text
        home_team, scoreboard, _, away_team = text_team_scoreboard.split('\n')

        #Pegando classificação dos times
        text_class_away = self.browser.find_element(By.CLASS_NAME,'dABLHT').text
        text_class_home = self.browser.find_element(By.CLASS_NAME,'fjjfrT').text
        class_away = int(text_class_away.split("\n")[0])
        class_home = int(text_class_home.split("\n")[0])

        #Pegando estatísticas dos times
        self.scroll_until_find('.VhXzF','css')

        data_parent = self.browser.find_element(By.CLASS_NAME,'VhXzF')
        data_elements = data_parent.find_elements(By.CLASS_NAME,'dsybxc')

        game_statistic = {}

        for el in data_elements:
            data = el.text.split('\n')
            game_statistic[f"{data[1]}"] = [data[0],data[2]]
        
        try:
            game_statistic['Cartões vermelhos'] = sum(int(value) for value in game_statistic['Cartões vermelhos'])
        except:
            game_statistic.setdefault("Cartões vermelhos", 0)
        
        try:
            game_statistic['Cartões amarelos'] = sum(int(value) for value in game_statistic['Cartões amarelos'])
        except:
            game_statistic.setdefault("Cartões amarelos", 0)
        
        #Pegando dados adicionais
        stadium_regex = r"Estádio\n(.*?)\n"
        referee_regex = r"Árbitro\n(.*?)\n"
        date_regex = r'(\d{2}/\d{2}/\d{4})'

        extra_data = self.browser.find_element(By.XPATH,'//*[@id="__next"]/main/div[2]/div[2]/div[1]/div[1]/div[12]/div/div')

        date = re.findall(date_regex,extra_data.text)[0]
        stadium = re.findall(stadium_regex,extra_data.text)[0]
        referee = re.findall(referee_regex,extra_data.text)[0]

        #Pegando lesões
        referee_regex = r"Sai:\s*(.*)"
        events = self.browser.find_elements(By.CSS_SELECTOR, ".dtqDoQ")
        
        for event in events:
            try:
                title = event.find_element(By.CSS_SELECTOR, 'title')

                if title.get_attribute('innerHTML') == 'Substituição':
                    injurie_player = re.findall(referee_regex,event.text)[0]
                    first_name = injurie_player.split(" ")[0]
                    last_name = injurie_player.split(" ")[-1]
                    
                    regex_end_with = re.compile(f"{first_name}.*$", re.IGNORECASE)
                    player = next((player for player in player_score[0] + player_score[1] if regex_end_with.search(player["name"])), None)
                    
                    if player is None:
                        regex_start_with = re.compile(f"^.*{last_name}", re.IGNORECASE)
                        player = next((player for player in player_score[0] + player_score[1] if regex_start_with.search(player["name"])), None)
                    
                    player["injurie"] = True
                        

            except NoSuchElementException:
                pass                

        class_data = {
            "date": date,
            "home_team": home_team,
            "away_team": away_team,
            "scoreboard": scoreboard,
            "home_classification": class_home,
            "away_classification": class_away,
            "game_statistic": game_statistic,
            "home_player_score": player_score[0],
            "away_player_score": player_score[1],
            "referee": referee,
            "stadium": stadium,
        }
        
        return Matches(class_data)
        
        
    # FUNÇÕES DE AUXÍLIO
    #Espera a página carregar completamente
    def wait_for_page_load(self):
        WebDriverWait(self.browser, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    #Procura elementos que são carregados de forma "lazy", ou seja, só quando a tela chega perto dele
    def scroll_until_find(self,element,type):
        while True:
            try:
                if type == 'css':
                    elemento = self.browser.find_element(By.CSS_SELECTOR, element)
                elif type == 'xpath':
                    elemento = self.browser.find_element(By.XPATH, element)
                return elemento
            except NoSuchElementException:
                # Rola a página para baixo uma tela de distância
                self.browser.execute_script("window.scrollBy(0, window.innerHeight);")
                sleep(1)
                
                # Verifica se chegou ao fim da página
                scroll_height = self.browser.execute_script("return document.body.scrollHeight")
                current_height = self.browser.execute_script("return window.scrollY + window.innerHeight")
                
                if current_height >= scroll_height:
                    break  

        return None 

    # Espera o element que foi dado ser encontrado na página
    def wait_element(
        self, element, time, method
    ):  
        try:
            if method == "class":
                myElem = WebDriverWait(self.browser, time).until(
                    EC.presence_of_element_located((By.CLASS_NAME, element))
                )
            elif method == "xpath":
                myElem = WebDriverWait(self.browser, time).until(
                    EC.presence_of_element_located((By.XPATH, element))
                )
            elif method == "id":
                myElem = WebDriverWait(self.browser, time).until(
                    EC.presence_of_element_located((By.ID, element))
                )
            elif method == "css":
                myElem = WebDriverWait(self.browser, time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, element))
                )
            return myElem
        except TimeoutException:
            print(f"{element} ainda não carregou")
            return False