from clases.Web_driver import Web_driver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from clases.User_objetive import User_objetive
from clases.Search import Search
import random

#########################################
# Clase para abstraer metodos sobre la Cuenta que se usa
# para ingresar a facebook, navegar y ubicar la seccion que nos interesa
#############################3##########

class Account_scraper(Web_driver):
    def __init__(self, mail_or_phone_number, password, user_obetive = None, search=None):
        self.mail_or_phone_number = mail_or_phone_number
        self.password = password
        self.list_frends = []
        self.user_obetive = user_obetive
        self.search = search

        super().__init__()
    
    #metodo para iniciar session en facebook mediante unas credenciales ya ingresadas
    def login(self):
        print('logueando')
        self.driver.get('https://www.facebook.com/')
        time.sleep(20)

        self.set_credentials()
        time.sleep(20)

        '''name_png = 'login_'+self.str_datetime()
        self.driver.save_screenshot('screenshot/'+ name_png + '.png')'''

        print('logueado')

    #metodo para realizar el proceso de rellenar el formulario de iniciar sesion
    def set_credentials(self):
        self.fill_mail_or_phone_number()
        self.fill_password()
        self.click_login()
    
    #Metodo para rellenar el input de mail_or_number
    def fill_mail_or_phone_number(self):
        input_mail_or_phone_number = self.driver.find_element_by_id('email')
        input_mail_or_phone_number.send_keys(self.mail_or_phone_number, Keys.ARROW_DOWN)
    
    #Metodo para rellenar el input de password
    def fill_password(self):
        input_pass = self.driver.find_element_by_id('pass')
        input_pass.send_keys(self.password, Keys.ARROW_DOWN)

    #Metodo para hacer click al boton de entrar para enviar los datos ingresados
    def click_login(self):
        button_send_content = self.driver.find_elements_by_css_selector('div._6ltg')[0]
        button_send = button_send_content.find_element_by_css_selector('button')
        self.driver.execute_script("arguments[0].click();", button_send)
    
    #Metodo que ubica las url y nombres de los primeros usuarios de la lista de amigos
    def find_friends(self):
        self.driver.get('https://www.facebook.com/friends/list')
        #este sleep es para que cargue la pagina
        time.sleep(25)

        #opcionalmente podemmos scar una captura de pantalla
        '''name_png = 'friends_'+self.str_datetime()+'.csv'
        self.driver.save_screenshot('screenshot/'+ name_png + '.png')'''

        my_list_frends = self.driver.find_elements_by_css_selector('div.sxpk6l6v a')
        print(len(my_list_frends))
        for friend in my_list_frends:
            url = friend.get_attribute('href')
            name = friend.find_element_by_css_selector('span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.jq4qci2q.a3bd9o3v')
            self.list_frends.append({'url': url, 'name': name.text})
    
    # Selecciona de forma aleatoria a uno de los usuarios de la lista de amigos ubicada
    def select_user_objetive(self):
        size = len(self.list_frends)
        if size ==0:
            self.user_obetive = None
        else:
            #friend = self.list_frends[random.randint(0, size-1)]
            friend = self.list_frends[7]
            self.user_obetive = User_objetive(friend['url'] , friend['name'], self.driver)
    
    def search_set(self, terminos):
        self.search = Search(terminos, self.driver)
    
    def link_set(self, link):
        self.search = Search(None, self.driver, link)
    
    # Otro metodo para obtener un usuario de forma aleatoria de la lista de amigos ya ubicada
    def get_friend_random(self):
        return self.list_frends[random.randint(0, len(self.list_frends)-1)]
        
    # metodo usado para pruebas y agilizar el proceso danto una lista sin buscarla con el webdriver
    def set_list(self):
        self.list_frends = [
            {'url': 'https://www.facebook.com/darvinson.santoyo', 'name': 'Darvinson Jose'}, 
            {'url': 'https://www.facebook.com/sergio.leon.3910', 'name': 'Sergio Jesus Leon'}, 
            {'url': 'https://www.facebook.com/hectorramon.carrionmendez', 'name': 'Hector Carrion'}, 
            {'url': 'https://www.facebook.com/celemar', 'name': 'Celenia Febres'}, 
            {'url': 'https://www.facebook.com/yosnel.febres', 'name': 'Yosnel Febres'}, 
            {'url': 'https://www.facebook.com/yurvielys.figuera', 'name': 'Yurvielys Figuera'}, 
            {'url': 'https://www.facebook.com/jennis.febres', 'name': 'Jennis Febres'}, 
            {'url': 'https://www.facebook.com/nerismar.febres', 'name': 'Nerismar Febres'}, 
            {'url': 'https://www.facebook.com/josejavier.figuera', 'name': 'Jose Javier Figuera'}, 
            {'url': 'https://www.facebook.com/maryuli.febres', 'name': 'Maryuli Febres'}, 
            {'url': 'https://www.facebook.com/ronnymixx.vera', 'name': 'Ronny Vera'}, 
            {'url': 'https://www.facebook.com/jairo.vera.509', 'name': 'Jairo Vera'}, 
            {'url': 'https://www.facebook.com/rosdeinys.rodriguez', 'name': 'Rosdeinys Rodriguez'}, 
            {'url': 'https://www.facebook.com/chismeliciosouneg', 'name': 'Uneg Uneg'}, 
            {'url': 'https://www.facebook.com/angelmanuel.verafebres', 'name': 'Angel Manuel Vera Febres'}, 
            {'url': 'https://www.facebook.com/labebakeli.fuentes', 'name': 'Keliannys Gabriela Fuentes'}, 
            {'url': 'https://www.facebook.com/Solangelcamila89', 'name': 'Maurera Sol'}, 
            {'url': 'https://www.facebook.com/eliezer.26', 'name': 'Eliezer Romero'}, 
            {'url': 'https://www.facebook.com/yarii.zuniga', 'name': 'Yáríí Zúñígá'}]

    # metodo para establecer la fecha y hora como un string 
    # y usarlo como nombres de las capturas de pantalla    
    def str_datetime(self):
        return str(datetime.now()).replace(':','_').replace(' ','_')
