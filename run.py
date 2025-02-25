from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

### GLOBAL VARIABLES

week = []
lectures = []

### WEBDRIVER AND INITIAL SETTINGS

driver = webdriver.Firefox()
driver.get("https://ytnk.tv")

watch_list=input("\n- Virgül kullanarak birden fazla hafta girilebilirsiniz.\n- Boş bırakılırsa tüm haftaları listeye ekler.\n-> HAFTA GİRİNİZ: ")
if(',' in watch_list):
    watch_list=watch_list.split(sep=',')
    watch_list = [int(i) for i in watch_list]
elif(watch_list!=""):
    int(watch_list)

### UTILITY FUNCTION

def relocate_elements(i):
    global week,lectures
    week = driver.find_elements(By.XPATH, f"//*[contains(text(),'{i}. HAFTA MODÜLÜ')]")

    if(len(week)>1):
        for j in week:
            if(i<10 and f"1{i}" in j.text):
                week.remove(j)
                week=week[0]
                break
    
    lectures = week.find_elements(By.XPATH,"../..//li")

### CREDENTIAL HANDLER

missing_credentials = True
try:
    with open("credentials.txt","r") as f:
        username=f.readline().strip()
        password=f.readline()
    missing_credentials = False
except:
    print("'credentials.txt' dosyası bulunamadı el ile giriş yapınız.")

### LOGIN HANDLER

if(not missing_credentials):
    login_button = driver.find_element(By.XPATH,"//*[text()='Giriş Yap']")
    email_box = driver.find_element(By.XPATH,"//*[@placeholder='posta@mail.com']")
    password_box = driver.find_element(By.XPATH,"//*[@placeholder='Şifreniz']")
    submit_button = driver.find_element(By.XPATH,"//*[@onclick='Giris()']")

    wait_login = WebDriverWait(driver,timeout=10,poll_frequency=1)
    wait_login.until(lambda _ : login_button.is_displayed())

    login_action = ActionChains(driver)\
        .click(login_button)\
        .pause(0.25)\
        .send_keys_to_element(email_box,username)\
        .send_keys_to_element(password_box,password)\
        .pause(0.25)\
        .click(submit_button)

    login_action.perform()

### LOCATE VIDEOS

time.sleep(2)

wait_locate0 = WebDriverWait(driver,timeout=10,poll_frequency=1)
target_lecture_link0 = wait_locate0.until(EC.presence_of_element_located((By.XPATH,"//*[text()='Kariyer Planlama Dersi']")))
time.sleep(1)
target_lecture_link0.click()

wait_locate1 = WebDriverWait(driver,timeout=10,poll_frequency=1)
target_lecture_link1 = wait_locate0.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='EgitimDtContendDt']")))
time.sleep(1)
target_lecture_link1[1].click()

### WATCH VIDEOS

if(watch_list==""):
    weeks = driver.find_elements(By.XPATH, f"//*[contains(text(),'HAFTA MODÜLÜ')]")
    watch_list=[i for i in range(1,len(weeks)+1)]

for i in watch_list:
    relocate_elements(i)
    print("- " + week.text)
    action_week = ActionChains(driver)\
        .move_to_element(week)\
        .click(week)\
        .perform()
    for j in range(len(lectures)+1):
        relocate_elements(i)
        print("- " + lectures[j].text)
        action_lecture = ActionChains(driver)\
            .move_to_element_with_offset(lectures[j],0,100)\
            .click(lectures[j])\
            .perform()
        try:
            wait_play = WebDriverWait(driver,timeout=10,poll_frequency=1)
            play_button = wait_play.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Play Video']/..")))
            play_action = ActionChains(driver)\
                .move_to_element_with_offset(play_button,0,100)\
                .click(play_button)\
                .perform()
        except:
            # replay_button = driver.find_element(By.XPATH, "//button[@onclick='TekrarIzle();']")
            # scroll_to(replay_button)
            # replay_button.click()
            # print("- Video tekrar izleniyor.")
            # time.sleep(4)
            # play_button = driver.find_element(By.XPATH, "//button[@title='Play Video']/..")
            # scroll_to(play_button)
            # play_button.click()
            print("- Önceden izlenilen video atlandı.")
            continue
        wait_end = WebDriverWait(driver,timeout=60*60,poll_frequency=3)
        msg_element = wait_end.until(EC.presence_of_element_located((By.XPATH,"//*[text()='Konuyu Başarı İle Tamamladınız!']")))
        time.sleep(0.25)
        driver.find_element(By.XPATH,"//button[text()='Ok']").click()