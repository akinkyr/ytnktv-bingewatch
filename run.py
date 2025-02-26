from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

### GLOBAL VARIABLES

week = []
lectures = []

### WEBDRIVER AND INITIAL SETTINGS

driver = webdriver.Firefox()
driver.get("https://ytnk.tv")

### UTILITY FUNCTIONS AND CLASSES

def log(type=0,msg="Message"):

    if(type==0):
        type="BİLGİ"
    elif(type==1):
        type="HATA"
    else:
        type='?'

    if(len(msg)>60):
        msg=msg[:47]+"..."
    print(f"[{datetime.datetime.now().strftime("%X")}] [{type}] : {msg}")


def scroll_to(element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, -150);")
    time.sleep(1)

def relocate_elements(i):
    global week,lectures
    week = driver.find_elements(By.XPATH, f"//*[contains(text(),'{i}. HAFTA MODÜLÜ')]")

    if(len(week)>1 and i<10):
        for j in week:
            if(f"1{i}" in j.text):
                week.remove(j)
        week=week[0]
    
    lectures = week.find_elements(By.XPATH,"../..//li")

### CREDENTIAL HANDLER

missing_credentials = True
try:
    with open("credentials.txt","r") as f:
        username=f.readline().strip()
        password=f.readline()
    missing_credentials = False
except:
    log(0,"'credentials.txt' dosyası bulunamadı el ile giriş yapınız.")

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

watch_list=input("\n- Virgül kullanarak birden fazla hafta girilebilirsiniz.\n- Boş bırakılırsa tüm haftaları listeye ekler.\n-> HAFTA GİRİNİZ: ")
watch_list.strip()
if(',' in watch_list):
    watch_list=watch_list.split(sep=',')
    watch_list = [int(i) for i in watch_list]
elif(watch_list!=""):
    watch_list = [int(watch_list)]
else:
    weeks = driver.find_elements(By.XPATH, f"//*[contains(text(),'HAFTA MODÜLÜ')]")
    watch_list=[i for i in range(1,len(weeks)+1)]

for i in watch_list:
    relocate_elements(i)
    log(0,week.text)
    scroll_to(week)
    if(not lectures[0].is_displayed()):
        week.click()
    for j in range(len(lectures)):
        relocate_elements(i)
        log(0,f"[{j+1}/{len(lectures)}] " + lectures[j].text)
        scroll_to(lectures[j])
        lectures[j].click()
        try:
            wait_play = WebDriverWait(driver,timeout=5,poll_frequency=1)
            play_button = wait_play.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Play Video']/..")))
            scroll_to(play_button)
            play_button.click()
        except:
            try:
                replay_button = wait_play.until(EC.element_to_be_clickable((By.XPATH,"//button[@onclick='TekrarIzle();']")))
                log(0,"İzlenilen video atlanıyor.")
                continue
            except Exception as exc:
                log(1,"Video oynatılamadı. (Atlandı)")
                print(f"{exc}")
                continue

        wait_end = WebDriverWait(driver,timeout=60*60,poll_frequency=3)
        msg_element = wait_end.until(EC.presence_of_element_located((By.XPATH,"//*[text()='Konuyu Başarı İle Tamamladınız!']")))
        time.sleep(0.25)
        driver.find_element(By.XPATH,"//button[text()='Ok']").click()

log(0,"İzleme listesi bitti, program sonlandırılıyor.")
driver.quit()
exit(0)