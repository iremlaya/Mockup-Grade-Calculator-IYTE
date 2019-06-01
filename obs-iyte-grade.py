from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from python3_anticaptcha import ImageToTextTask
from PIL import Image
from io import BytesIO
import time
from requests_testadapter import Resp
import requests
import os
from selenium.webdriver.common.action_chains import ActionChains

class Lesson:
    def __init__(self,name,code,credit,hours):
        self.name = name
        self.code = code
        self.credit = credit
        self.hours = hours
        self.default_credit = credit

   
    def set_credit(self,credit):
        self.credit = credit
        return self.credit
    def set_grade(self,grade):
        self.grade = grade
        if hasattr(self,"letter") == False:
            self.calculate_letter()
        return self.grade
    def set_letter_grade(self,letter):
        self.letter = letter
        self.calculate_letter_gpa()
        return self.letter
    def calculate_letter(self):
        try:
            if self.grade>=90:
                letter = 'AA'
            elif self.grade>=85:
                letter = 'BA'
            elif self.grade>=80:
                letter = 'BB'                
            elif self.grade>=75:
                letter = 'CB'
            elif self.grade>=70:
                letter = 'CC'
            elif self.grade>=65:
                letter = 'DC'
            elif self.grade>=60:
                letter = 'DD'
            elif self.grade>=50:
                letter = 'FD'
            else:
                letter = 'FF'

            self.letter = letter
            return self.letter
        except AttributeError:
            print("Grade attribute does not exist for Lesson class.")

    def calculate_letter_gpa(self):
        try:
            if self.letter == 'AA':
                gpa = 4.0
            elif self.letter == 'BA':
                gpa = 3.5
            elif self.letter == 'BB':
                gpa = 3.0
            elif self.letter == 'CB':
                gpa = 2.5
            elif self.letter == 'CC':
                gpa = 2.0
            elif self.letter == 'DC':
                gpa = 1.5
            elif self.letter == 'DD':
                gpa = 1.0
            elif self.letter == 'FD':
                gpa = 0.5
            elif self.letter == 'FF':
                gpa = 0.0
            else: 
                raise ValueError
            
            self.gpa = gpa
            return gpa
        except AttributeError:
            print("Letter attribute doesn't exist for Lesson class.")
    
    def restore_original_credit(self):
        self.credit = self.default_credit
        return self.credit
    def stringify(self):
        return 'The class named {} with code {} has {} credits and {} hours per week.'.format(self.name,self.code,self.credit,self.hours)

def empty():
    max_len = 0
    for i in cnt_array:
        
        length = int(len(i))
        if length > max_len:
            max_len = length
    
    return max_len + 1

def empty_name(liste):
    max_len = 0
    for i in liste:
        
        length = int(len(i.name))
        if length > max_len:
            max_len = length
    
    return max_len + 1

def options():
    print("1 - Calculate this semester's GPA with mockup grade.\n2 - Show grades by semester\n: ")

def main():
    valid = True
    start = input("Enter 0 to start the program.")
    code = input("Please enter your anticaptcha key or press x if you do not have it.")
    num = int(input("Enter your std number"))
    psw = int(input("Enter your password"))
    path = input("give absoulute path to chromedriver")
    while(valid):
        
        options()
        opt = int(input())

        if(int(start) == 0 and code != "x"):
            login_captca(num,psw,code,path)
            print("login successful")
            if(opt==1):
                opt1()
                inp = input("x to quit or 1 to continue.")
                if(inp == "x"):
                    valid = False
                    driver.quit()
                    continue
                elif(int(inp) == 1):
                    driver.quit()
                    continue
            elif(opt==2):
                opt2()
                inp = input("x to quit or 1 to continue.")
                if(inp == "x"):
                    valid = False
                    driver.quit()
                    continue
                elif(int(inp) == 1):
                    driver.quit()
                    continue
        elif(int(start) == 0 and code == "x"):
            print("please enter captcha answer in chromedriver.")
            time.sleep(3)
            driver = login(num,psw,path)
            print("login successful")
            if(opt==1):
                opt1(driver)
                inp = input("x to quit or 1 to continue.")
                if(inp == "x"):
                    valid = False
                    driver.quit()
                    continue
                elif(int(inp) == 1):
                    driver.quit()
                    continue
            elif(opt==2):
                opt2(driver)
                inp = input("x to quit or 1 to continue.")
                if(inp == "x"):
                    valid = False
                    driver.quit()
                    continue
                elif(int(inp) == 1):
                    driver.quit()
                    continue
def login(num,psw,path):
    driver = webdriver.Chrome(path)
    driver.get("https://obs.iyte.edu.tr/oibs/ogrenci/login.aspx")

    assert "No results found." not in driver.page_source
    numara = num
    password = psw
    time.sleep(10)

    numara_input = driver.find_element_by_name("txtParamT01")
    numara_input.send_keys(numara)

    pass_input = driver.find_element_by_name("txtParamT02")
    pass_input.send_keys(password)

    submit = driver.find_element_by_name("btnLogin")
    submit.click()
    return driver
def login_captca(num,psw,code,path):      
    driver = webdriver.Chrome(path)
    driver.get("https://obs.iyte.edu.tr/oibs/ogrenci/login.aspx")

    assert "No results found." not in driver.page_source

    ANTICAPTCHA_KEY = str(code)

    image_link = 'https://obs.iyte.edu.tr/oibs/ogrenci/login.aspx'

    user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).\
                    captcha_handler(captcha_link=image_link)

    element = driver.find_element_by_id("imgCaptchaImg").screenshot_as_png
    im = Image.open(BytesIO(element))
    im.save('./image.png')
    image_path = '.\/image.png'
    user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).captcha_handler(captcha_file=image_path)
    solution = user_answer["solution"]["text"]
    print(user_answer)
    print(solution)

    numara = num
    password = psw
    time.sleep(10)

    numara_input = driver.find_element_by_name("txtParamT01")
    numara_input.send_keys(numara)

    pass_input = driver.find_element_by_name("txtParamT02")
    pass_input.send_keys(password)


    inputelem = driver.find_element_by_name("txtSecCode")
    inputelem.send_keys(solution)

    submit = driver.find_element_by_name("btnLogin")
    submit.click()

    return driver

def opt1(driver):
        
    driver.find_element_by_class_name("treeview").click()

    time.sleep(3)
    button = driver.find_element_by_xpath('//*[@class="treeview-menu"]/li[6]/a').click()

    time.sleep(5)

    driver.switch_to.frame(driver.find_element_by_id("IFRAME1"))
    elem = driver.find_elements_by_class_name("grd_altcizgi")
    table_content = [i.text for i in elem if i.text != '' and i.text != '--  ']

    lesson_list = []
    length = int(len(table_content))
    for i in range(0,length,10):
        code = table_content[i]
        name = table_content[i+2]
        cred = table_content[i+3]
        hour = table_content[i+5]

        lesson_list.append(Lesson(name,code,cred,hour))

    def build_piece(string,length):
        string = str(string)
        if len(string) % 2 == 0:
            return "|" + " "*int((length - len(string))/2) + string + " "*int((length-1 - len(string))/2) 
        else:
            return "|" + " "*int((length - len(string))/2) + string + " "*int((length - len(string))/2) 
    
    def build_name_piece(string,lesson_list):
        string = str(string)
        if len(string) % 2 == 0:
            return "|" + " "*int((empty_name(lesson_list) - len(string))/2) + string + " "*int((empty_name(lesson_list)-1 - len(string))/2) 
        else:
            return "|" + " "*int((empty_name(lesson_list) - len(string))/2) + string + " "*int((empty_name(lesson_list) - len(string))/2) 

    def enter_grades():
        print("Enter grade as letter (e.g AA) or as number (e.g 3.0); or enter x to skip.")

        all_creds = 0
        for i in lesson_list:
            grade = input("Enter grade for {}.".format(i.code))
            all_creds += int(i.credit)

            if grade == "x":
                continue
            else:
                try:
                    number = int(grade)
                    i.set_grade(number)
                except ValueError:
                    letter = grade.upper()
                    i.set_letter_grade(letter)
        return all_creds
        
    def build_string(lesson_list):
        all_creds = enter_grades()

        strings = build_name_piece("name",lesson_list) + build_name_piece("code",lesson_list) + build_piece("credits", len("credits")+4) + build_piece("hours", len("hours")+4)\
        + build_piece("letter",len("letter")+4) + build_piece("gpa",len("gpa")+4) + "|\n" 
        line_len = len(strings)

        strings+="-"*line_len + "\n"

        for i in lesson_list:
            string = ""
            string+=build_name_piece(i.name,lesson_list) + build_name_piece(i.code,lesson_list) + build_piece(i.credit,len("credits")+4) \
            + build_piece(i.hours,len("hours")+4)
            if hasattr(i,"letter") == False:
                string+='{}'.format(build_piece("x",len("letter")+4))
                string+='{}|\n'.format(build_piece("x",len("gpa")+4))
            else:
                string+='{}'.format(build_piece(i.letter,len("letter")+4))
                string+='{} |\n'.format(build_piece(i.calculate_letter_gpa(),len("gpa")+4))  
            strings+=string
            strings+="-"*line_len + "\n"
        
        return strings,all_creds
    strings,all_creds = build_string(lesson_list)
    print(strings)

    def calculate_term_gpa(all_creds):
            numerator = 0
            for i in lesson_list:
                numerator += float(i.credit) * float(i.gpa)
            
            return numerator / float(all_creds)

    print(calculate_term_gpa(all_creds))

    valid = True
    while(valid):

        inp = input("press 1 to calculate again, anything else to quit this option.")
        if(int(inp)==1):
            strings_new,all_creds_new = build_string(lesson_list)
            print(strings_new)
            print(calculate_term_gpa(all_creds_new))
            continue
        else:
            valid=False



def opt2(driver):
        
    button = driver.find_element_by_xpath('//*[@id="lblMenuBuf"]/ul/li[3]/ul/li[2]/a').click()

    time.sleep(5)
    driver.switch_to.frame(driver.find_element_by_id("IFRAME1"))
    table = driver.find_element_by_id("grdOrtalamasi")

    content = table.text.replace('\n', " ").split(" ")
    del content[len(content)-18:]

    donem_adi = " ".join(content[:2])
    aldigi_ders_sayisi = " ".join(content[2:5])
    toplam_kredi = " ".join(content[5:7])
    toplam_akts = " ".join(content[7:9])
    donem_ort = " ".join(content[9:11])
    genel_ort = " ".join(content[11:14])

    cnt_array = [donem_adi, aldigi_ders_sayisi, toplam_kredi, toplam_akts,donem_ort, genel_ort]
    contents = []
    for i in range(14,len(content),7):
        first = content[i] + " " + content[i+1]
        contents.append(first)
        arr = content[i+2:i+7]
        contents+=arr
    s = ""

    for i in cnt_array:
        empty = int((empty()-len(i))/2)
        if(len(i)%2==0):
            empty1 = int((empty()+1-len(i))/2)
            s += "|" + " "*empty + i + " "*(empty1) 
        else:
            s += "|"+" "*empty+i+" "*empty

    s += "|\n"
    j = 1
    for i in contents:
        empty = int((empty()-len(i))/2)
        if(len(i)%2==0):
            empty1 = int((empty()+1-len(i))/2)
            s += "|" + " "*empty + i + " "*(empty1) 
        else:
            s += "|"+" "*empty+i+" "*empty
        if j%6==0:
            s+= "|\n"
        j+=1
    
    print(s)















#table_content = ['HIST202', '1', 'ATATÜRK İLKELERİ VE İNKILAP TARİHİ II', '0', '2+0', '2', '2', 'Z', 'GENEL KÜLTÜR DERSLERİ', 'Dr.Öğr.Üyesi ELÇİN YILMAZ', 'EE272', '1', 'ELEKTRONIK DEVRELERI', '4', '3+2', '6', '2', 'Z', 'ELEKTRONİK VE HABERLEŞME MÜHENDİSLİĞİ', 'Öğr.Gör. MAHMUT CENK EFELER', 'CENG214', '1', 'MANTIK TASARIMI', '4', '3+2', '7', '2', 'Z', 'BİLGİSAYAR MÜHENDİSLİĞİ', 'Öğr.Gör. BURAK GALİP ASLAN', 'CENG212', '1', 'PROGRAMLAMA DILLERI KAVRAMI', '3', '3+0', '5', '2', 'Z', 'BİLGİSAYAR MÜHENDİSLİĞİ', 'Dr.Öğr.Üyesi SELMA TEKİR', 'CENG216', '1', 'SAYISAL HESAPLAMA', '3', '3+0', '5', '2', 'Z', 'BİLGİSAYAR MÜHENDİSLİĞİ', 'Dr.Öğr.Üyesi MUSTAFA ÖZUYSAL', 'JAP202', '2', 'TEMEL JAPONCA II', '3', '3+0', '3', '2', 'S', 'İNGİLİZCE', 'Öğr.Gör. HAYAT GÜRDAL', 'TURK202', '1', 'TÜRK DİLİ DERSLERİ II', '0', '2+0', '2', '2', 'Z', 'GENEL KÜLTÜR DERSLERİ', 'Öğr.Gör.Dr. YASEMİN ÖZCAN GÖNÜLAL']

main()

