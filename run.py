from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Firefox()
action = ActionChains(driver)

week = []
lectures = []


def scroll_to(element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, -200);")
    time.sleep(1)

def relocate_elements(i):
    global week,lectures
    week = driver.find_element(By.XPATH, f"//*[contains(text(),'{i}. HAFTA MODÜLÜ')]")
    lectures = week.find_elements(By.XPATH,"../..//li")

driver.get("https://ytnk.tv")

try:
    with open("credentials.txt","r") as f:
        username=f.readline().strip()
        password=f.readline()
except:
    print("'credentials.txt' dosyası bulunamadı el ile giriş yapınız.")

time.sleep(3)   

login = driver.find_element(By.XPATH,"//*[text()='Giriş Yap']").click()
time.sleep(2)
driver.find_element(By.XPATH,"//*[@placeholder='posta@mail.com']").send_keys(username)
driver.find_element(By.XPATH,"//*[@placeholder='Şifreniz']").send_keys(password)
time.sleep(1)
driver.find_element(By.XPATH,"//*[@onclick='Giris()']").click()
time.sleep(2)
driver.find_element(By.XPATH,"//*[text()='Kariyer Planlama Dersi']").click()
time.sleep(5)
driver.find_elements(By.XPATH,"//div[@class='EgitimDtContendDt']")[1].click()
print("Hata giriş yapılamıyor.")

print("Devam etmeden önce ders izleme ekranına geldiğinizden emin olun.")

week = driver.find_elements(By.XPATH, f"//*[contains(text(),'HAFTA MODÜLÜ')]")

watch_list=input("\n- Virgül kullanarak birden fazla hafta girilebilirsiniz.\n- Boş bırakılırsa tüm haftaları listeye ekler.\nHAFTA GİRİNİZ): ")
if(watch_list==""):
    watch_list=[i for i in range(1,len(week)+1)]
elif(',' in watch_list):
    watch_list=watch_list.split(sep=',')
    watch_list = [int(i) for i in watch_list]
else:
    int(watch_list)

for i in watch_list:
    relocate_elements(i)
    print(week.text)
    scroll_to(week)
    week.click()
    for j in range(len(lectures)+1):
        print(lectures[j].text)
        relocate_elements(i)
        scroll_to(lectures[j])
        lectures[j].click()
        time.sleep(5)
        try:
            play_button = driver.find_element(By.XPATH, "//button[@title='Play Video']/..")
            scroll_to(play_button)
            play_button.click()
        except:
            # replay_button = driver.find_element(By.XPATH, "//button[@onclick='TekrarIzle();']")
            # scroll_to(replay_button)
            # replay_button.click()
            # print("- Video tekrar izleniyor.")
            # time.sleep(4)
            # play_button = driver.find_element(By.XPATH, "//button[@title='Play Video']/..")
            # scroll_to(play_button)
            # play_button.click()
            print("- İzlenilen video atlandı.")
            continue
        found_element = False
        while(not found_element):
            try:
                msg_element = driver.find_element(By.XPATH,"//*[text()='Konuyu Başarı İle Tamamladınız!']")
                found_element = True
            except:
                time.sleep(3)
        time.sleep(0.5)
        driver.find_element(By.XPATH,"//button[text()='Ok']").click()