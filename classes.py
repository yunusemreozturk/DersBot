from userInformation import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from pathlib import Path


class MersinUni:
    def __init__(self, username, password):  # username ve password'u alıyor
        self.username = username
        self.password = password

    def sign_in_start(self):
        self.browser = webdriver.Chrome()  # bir Chrome değişkeni oluşturuyoruz

        self.browser.minimize_window()

        url = 'http://ue1.mersin.edu.tr/login/index.php'
        self.browser.get(url)  # get ile url'de olan sayfayı getiriyoruz

        self.sign_in()  # giriş yapıyoruz

    def sign_in(self):
        username_input = self.browser.find_element_by_xpath('//*[@id="username"]')  # sing in start fonksiyonu ile
        # getirdiğimiz sayfanın username ve password kısımları bunlar
        password_input = self.browser.find_element_by_xpath('//*[@id="password"]')

        username_input.send_keys(username)  # usernmame ve password kısımlarına parolalarımızı gönderiyoruz
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)  # ve enter tuşuna basıp giriş yapıyoruz.

    def get_lesson(self):
        self.sign_in_start()  # bu fonksiyon ilk çağırıldığında giriş yapmamızı sağlıyor

        lesson_title = []
        lesson_url = []
        content = self.browser.find_elements_by_css_selector('h4.card-title a')  # giriş yaptıktan sonra karşımıza
        # derslerin bulunduğu sayfa geliyor

        for item in content:
            lesson_title.append(item.text)  # for döngüsü ile isimlerini ve url'lerini alıyoruz
            lesson_url.append(item.get_attribute('href'))

        return lesson_title, lesson_url  # ve onları dönüyoruz.

    def get_lesson_page(self, url):
        self.browser.get(url)  # verilen sayfaya gidiyoruz

        content = []
        page_list = []
        date_list = []
        page_dict = {}
        count = 1

        lesson_name = self.browser.find_element_by_css_selector('div.page-header-headings h1').text
        number_element = len(self.browser.find_elements_by_css_selector('ul.weeks li.section')) - 1  # haftaların
        # sayılarını alıyoruz

        while count <= number_element:
            content.append(self.browser.find_element_by_xpath(f'//*[@id="section-{count}"]'))  # burada sectionları
            # sıra ile alıp content'e ekliyoruz (haftalık olarak)
            count += 1

        count = 1
        for item in content:
            date = item.find_element_by_css_selector('h3.sectionname a').text  # aldığımız haftalık bilgilerin
            # tarihlerini alıyoruz
            inner_content = item.find_elements_by_css_selector(
                f'li.section[id="section-{count}"] ul.section.img-text li.activity')  # href ve textlerin bulunduğu
            # kısım burası burada href ve text'in üst kısımlarını kapsayan bir li'yi alıyoruz

            for inner_item in inner_content:
                href = inner_item.find_element_by_css_selector('div.activityinstance a').get_attribute(
                    'href')  # hrefleri alıyoruz
                text = inner_item.find_element_by_css_selector(
                    'div.activityinstance span.instancename').text  # text'leri alıyoruz
                page_list.append({'href': href, 'text': text})  # bunları dict tipinde listeye ekliyoruz

            page_dict[date] = page_list  # listeleri date adıyla dicte kayıt ediyoruz
            page_list = []

            date_list.append(date)

            count += 1
            if count == 21:  # count 21 geldiği zaman döngüden çıkıp page dict'i dönüyoruz
                break

        return page_dict, date_list, lesson_name

    def get_url(self, url):  # verilen url almaya yarar
        self.browser.get(url)

    def close_window(self):  # Chrome penceresini kapatmaya yarar
        self.browser.quit()

    def announcements(self, url):
        self.browser.get(url)  # o anki verilen dersin url'ini alıyor

        announcements = []
        link = []

        content = self.browser.find_element_by_id('section-0') \
            .find_elements_by_css_selector(
            'ul.section.section.img-text li.activity')  # duyuru kısmı section 0'da olduğu
        # icin onu ve içindeki li'leri alıyoruz

        for item in content:
            announcements.append(item.find_element_by_css_selector('span.instancename').text)  # aldığımız duyuruları
            # listeye kayıt ediyoruz
            link.append(item.find_element_by_css_selector('div.activityinstance a').get_attribute('href'))  # aldığımız
            # duyuruların linklerini listeye kayıt ediyoruz

        return announcements, link

    def write_to_file_from_url(self, url):  # dosyaya yazmaya yarar
        page_dict = []
        date_list = []

        home = str(Path.home())
        page_dict, date_list, lesson_title = self.get_lesson_page(url)

        control = True
        if control:  # burası masaüstünde Uni adlı bir klasör var mı yok mu ona bakar
            for item in os.listdir(f'{home}\\Desktop'):  # yoksa oluşturur
                if item == 'Uni':
                    control = False
            if control:
                os.chdir(f'{home}\\Desktop')
                os.mkdir('Uni')

        open(f'{home}\\Desktop\\Uni\\{lesson_title}.txt', 'w').close()  # dosyanın içeriğini silmeye yarar

        for item in date_list:
            with open(f'{home}\\Desktop\\Uni\\{lesson_title}.txt', 'a', encoding='utf-8') as file:
                file.write(f' - {item}\n\n')  # ilk başta tarihleri yazdırıyoruz

            for inner_item in range(0, len(page_dict[item])):
                text = page_dict[item][inner_item]["text"]  # burada text kısmını alıyoruz

                with open(f'{home}\\Desktop\\Uni\\{lesson_title}.txt', 'a', encoding='utf-8') as file1:
                    file1.write(f'{text}\n\n')  # ve dosyaya yazıyoruz

    def write_to_file(self, url):  # dosyaya yazmaya yarar
        page_dict = []
        date_list = []

        page_dict, date_list, lesson_title = self.get_lesson_page(url)

        control = True
        if control:  # burası masaüstünde Uni adlı bir klasör var mı yok mu ona bakar
            for item in os.listdir():  # yoksa oluşturur
                if item == 'Uni':
                    control = False
            if control:
                os.mkdir('Uni')

        open('temp.txt', 'w').close()  # dosyanın içeriğini silmeye yarar

        for item in date_list:
            with open('temp.txt', 'a', encoding='utf-8') as file:
                file.write(f' - {item}\n\n')  # ilk başta tarihleri yazdırıyoruz

            for inner_item in range(0, len(page_dict[item])):
                text = page_dict[item][inner_item]["text"]  # burada text kısmını alıyoruz

                with open('temp.txt', 'a', encoding='utf-8') as file1:
                    file1.write(f'{text}\n\n')  # ve dosyaya yazıyoruz

    def what_happened_this_week(self, lesson_name, lesson_url):
        pass

        # home = str(Path.home())
        #
        # self.write_to_file(lesson_url)
        #
        # # geçici dosyamızın satır sayısını aldık
        # with open('temp.txt', 'r', encoding='utf-8') as file_temp:
        #     number_of_row_temp = file_temp.read().count("\n")
        #
        # # verile dosyamızın satır sayısını aldık
        # with open(f'{home}\\Desktop\\Uni\\{lesson_name}.txt', 'r', encoding='utf-8') as file_row:
        #     number_of_row = file_row.read().count("\n")
        #
        # # verilen dosyamızın satır sayısını geçici dosya ile aynı yaptık
        # with open(f'{home}\\Desktop\\Uni\\{lesson_name}.txt', 'a', encoding='utf-8') as file:
        #     for item in range(0, number_of_row_temp - number_of_row + 1):
        #         file.write('\n')
        #
        # # verilen ve geçici dosyalarımızın satırlarını list haline getirdik
        # file1 = open(f'temp.txt', 'r', encoding='utf-8').readlines()
        # file2 = open(f'{home}\\Desktop\\Uni\\{lesson_name}.txt', 'r', encoding='utf-8').readlines()
        #
        # # verilen ile geçici arasında bir kaşılaştırma yapılıyor
        # for item in range(0, number_of_row_temp):
        #     if file1[item] == file2[item]:
        #         continue
        #     elif file1[item] != file2[item]:
        #         print(file1[item])
        #         file2[item] = file1[item]
        #         continue
        #
        # with open(f'{home}\\Desktop\\Uni\\{lesson_name}.txt', 'w', encoding='utf-8') as lesson_file:
        #     for item in file2:
        #         lesson_file.write(item)
