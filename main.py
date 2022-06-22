"""
Bu program eğitim amaçlıdır. BTK(Bilişim Teknolojileri ve İletişim Kurulu) Akademide Python Derslerinde gördüğüm dersleri, yeteneklerimi geliştirmek için uygulamaya çalışıyorum. Hiçbir şekilde zararlı değildir.
"""

from userInformation import username, password
import classes
import os.path

uni_object = classes.MersinUni(username, password)  # username ve password'u MersinUni clasına gönderiyoruz
lesson_title, lesson_url = uni_object.get_lesson()  # derslerin url'lerini ve isimlerini alıyoruz

while True:
    print('MENÜ'.center(50, '*'))
    try:
        choice = int(input(
            '1- Dersler\n2- Bugün Ne Oldu?\n3- Yeni Ödev Yüklendi Mi?\n4- Update\n5- Çıkış\n    -Seçim Yapınız: '))
        print()
    except ValueError:
        print('Lütfen Sayı Giriniz.')
        continue

    if choice == 1:
        while True:
            count = 1

            for item in lesson_title:
                print(f'{count}- {item}')
                count += 1
            print(f'{count}- Geri')
            print()

            try:
                lesson_input = int(input('  -Ders Seçiniz: '))
            except ValueError:
                print('\nLütfen sayı giriniz.\n')
                continue

            if lesson_input == count:
                break
            elif lesson_input > count:
                print('\nBöyle bir sayı yok!\n')
                continue
            elif lesson_input == 0:
                print('\nSayı 0 olamaz\n')
                continue

            print()
            lesson_content, temp1, temp2 = uni_object.get_lesson_page(
                lesson_url[lesson_input - 1])  # get lesson page'e url'leri
            # veriyoruz o da bize verdiğiimiz ders url'inin bilgileri dict içinde yolluyor
            announcements, link = uni_object.announcements(
                lesson_url[lesson_input - 1])  # verilen dersin duyurular kısmı

            while True:
                count = 0
                keys_list = []

                print(f'    {count}-   {announcements[0]}'.replace('\nForum', ''))

                print()

                count = 1
                for key in lesson_content.keys():  # verilen bilgilerin keys'lerini alıp onları key'e atıyoruz
                    keys_list.append(key)  # key list'e haftaları gönderiyoruz.
                    print(f'{count}- {key}')
                    count += 1
                print(f'{count}- Geri\n')

                try:
                    l_content_input = int(input('   -Hangi haftayı seçmek istersiniz? '))
                    print()
                except ValueError:
                    print('\nLütfen Sayı Giriniz.\n')
                    continue

                if l_content_input == 21:
                    break
                elif l_content_input > 21:
                    print('\nBöyle bir sayı yok!\n')
                    continue

                while True:
                    if l_content_input == 0:  # bu bölüm duyurular kısmını yazdırıyor
                        count = 1
                        for item in announcements:
                            print(f' {count}- {item}'.replace('\nForum', '').replace('\nÖdev', ''))
                            count += 1
                        print(f' {count}- Geri')

                        try:
                            announcements_input = int(input('   -Seçim yapınız? '))
                            print()
                        except ValueError:
                            print('\nLütfen Sayı Giriniz.\n')
                            continue

                        if announcements_input == count:
                            break
                        elif announcements_input > count:
                            print('\nBöyle bir sayı yok!\n')
                            continue
                        elif announcements_input == 0:
                            print('\n0 sayısı yok olamaz.\n')
                            continue

                        uni_object.get_url(link[announcements_input - 1])
                        continue

                    index = keys_list[l_content_input - 1]  # seçilen haftayı index'e atıyoruz
                    inner_list = lesson_content[index]  # ve atılan haftaların bilgilerini inner list'e atıyoruz

                    count = 1
                    for inner_item in inner_list:  # inner list'in içindeki bilgileri sekme halinde inner item'a atıyoruz
                        print(f'{count}- {inner_item["text"]}')  # inner item'ın içindeki texleri count ile birlikte
                        # yazdırıyoruz
                        print()
                        count += 1
                    print(f'{count}- Geri')

                    try:
                        inner_input = int(input('Sayı giriniz: '))
                    except ValueError:
                        print('\nLütfen Sayı Giriniz.\n')
                        continue

                    if inner_input == count:
                        break
                    elif inner_input > len(inner_list):
                        print('\nBöyle bir sayı yok!\n')
                        continue
                    elif inner_input == 0:
                        print('\nSayı 0 olamaz.\n')
                        continue

                    count = 1

                    url = inner_list[inner_input - 1]["href"]  # inner list'den url'i alıyoruz

                    uni_object.get_url(url)  # ve url'li açıyoruz

                    continue

    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        for item in lesson_url:
            uni_object.write_to_file_from_url(item)
        print('Update Tamamlandı.\n')
    elif choice == 5:
        print('Programdan çıkış yapıldı.')
        break
    else:
        print('Yanlış bir değer girdiniz.')
        break
