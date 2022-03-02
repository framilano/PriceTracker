from selenium.webdriver.common.by import By
from terminal_colored_print import colored_print, colored_sprint
from time import sleep
from requests import get
import undetected_chromedriver as uc
import json

#Saving already sent offers to avoid repeating them
last_declared_offer = {}

#Config file with chromium_path_values and sites paths
config_file = open('configs/config.json', 'r')
json_config = json.load(config_file)

#Send message to chat_id user on Telegram
def send_telegram(chat_id, product_link, title, float_price, float_desired):
    bot_message = ("[{}]({})\nPrezzo attuale: €{:.2f} (più eventuale spedizione)" + \
    "\nPrezzo desiderato: €{:.2f}").format(title, product_link, float_price, float_desired)
    send_text = 'https://api.telegram.org/bot' + json_config['telegram_bot_token'] + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    req = get(send_text)
    if (req.status_code != 200): print("Couldn't send Telegram message to {}, maybe your BOT Token or Chat_ID is invalid".format(chat_id))

#Choose to alert user based on last_declared_offer
def update_user(user, float_price, float_desired, link, title):
    global last_declared_offer
    #Se per la prima volta si raggiunge il prezzo desiderato, informa l'utente
    if (link not in last_declared_offer[user]):
        colored_print("[Prezzo desiderato raggiunto]\nInvio un avviso su telegram", fg_color=34, format="Bold")
        last_declared_offer[user][link] = float_price
        send_telegram(user, link, title, float_price, float_desired)
    #Se il prezzo desiderato è già stato raggiunto ed è diverso dall'ultimo avvisato, informa l'utente
    else:
        if (float_price != last_declared_offer[user][link]):
            colored_print("[Prezzo desiderato raggiunto, ma cambiato]\nInvio un avviso su telegram", fg_color=92, format="Bold")  
            last_declared_offer[user][link] = float_price  
            send_telegram(user, link, title, float_price, float_desired)
    #Se il prezzo desiderato è già stato raggiunto ed è uguale all'ultimo avvisato, non informare l'utente
        else: colored_print("[Prezzo desiderato raggiunto, ma ho già avvisato]\nNon invio un avviso su telegram", fg_color=62, format="Bold")        

#Cycle over links_and_price users and check desired prices
def check_sites(stores_dict, driver, links_and_file_db):
    global last_declared_offer
    
    for user in links_and_file_db:
        #Adding the user to the last declared offer dictionary, only if it's not already
        if (user not in last_declared_offer): last_declared_offer[user] = {}

        for link in links_and_file_db[user]:
            colored_print("//////////", fg_color=196)
            colored_print("Parsing site for user: {}".format(user), format="Bold;Underline", fg_color=202)
            desired_price = links_and_file_db[user][link]
            driver.get(link)

            title_xpath = ""
            price_xpath = ""

            for store in stores_dict:
                if (stores_dict[store]['prefix'] in link): 
                    colored_print("{}".format(store), fg_color=69)
                    title_xpath = stores_dict[store]['title_xpath']
                    price_xpath = stores_dict[store]['price_xpath']
                    print(colored_sprint("Link: ", format="Bold") + "{}".format(link))
                    try:
                        title =  driver.find_element(By.XPATH, title_xpath)
                        price = driver.find_element(By.XPATH, price_xpath)
                    except:
                        colored_print("Prodotto non disponibile", format="Reversed")
                        continue
                    try: float_price = float(price.text.replace("€", ""))
                    except (ValueError): 
                        try: float_price = float(price.text.replace("€", "").replace(".", "").replace(",", "."))
                        except (ValueError): 
                            colored_print("Prodotto non disponibile", format="Reversed")
                            continue
                    
                    float_desired = float(desired_price)
                    print(
                        colored_sprint("Nome prodotto: ", format="Bold") + f"{title.text}\n" + 
                        colored_sprint("Prezzo attuale: ", format="Bold") +  f"€{float_price}\n" +
                        colored_sprint("Prezzo desiderato: ", format="Bold") + f"€{float_desired}"
                    )

                    #Se il prezzo attuale è inferiore o uguale a quello desiderato
                    if (float_price <= float_desired): 
                        update_user(user, float_price, float_desired, link, title.text)
                    else: 
                        #Il prezzo è tornato normale, resetta il dizionario per l'ultimo valore desiderato trovato
                        if (link in last_declared_offer[user]): 
                            del last_declared_offer[user][link]
                    



def main():
    global config_file
    global json_config
    #Hiding from bot detection
    option = uc.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--disable-gpu")
    option.binary_location = json_config['chromium_browser_path']

    #Creo il driver per Chrome
    driver = uc.Chrome(options=option, version_main=json_config['chromium_version'])

    stores_dict = json_config['stores']
    
    # Loop 
    while (True):
        #Opening jsons each time to update its content
        links_and_price_file = open('users_db/links_and_price.json', 'r')
        config_file = open('configs/config.json', 'r')
        links_and_file_db = json.load(links_and_price_file)
        json_config = json.load(config_file)

 
        check_sites(stores_dict, driver, links_and_file_db)

        #Closing files
        links_and_price_file.close()
        config_file.close()
        
        colored_print("//////////", fg_color=196)
        print("Last saved offers:\n" + str(last_declared_offer))

        #Opening a low resource site while idling
        driver.get("https://start.duckduckgo.com/")
        sleep(120)


if __name__ == '__main__': main()