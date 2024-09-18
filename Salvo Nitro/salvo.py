import http.client
import random
import string
import ssl
import time
from urllib.parse import urlparse
from colorama import init, Fore

# Colorama'yı başlat
init(autoreset=True)

# SSL doğrulamasını devre dışı bırakacak bir SSL context oluşturuyoruz
context = ssl._create_unverified_context()

def generate_random_code(length=16):
    """Rastgele bir Discord Nitro kodu oluşturur."""
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

def check_gift_validity(url):
    """Bir Discord Nitro linkinin geçerliliğini kontrol eder."""
    parsed_url = urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.netloc, context=context)
    path = parsed_url.path

    try:
        conn.request("GET", path)
        response = conn.getresponse()

        if response.status == 301:
            new_location = response.getheader('Location')
            print(Fore.YELLOW + "Yönlendiriliyor: {}".format(new_location))
            return check_gift_validity(new_location)

        elif response.status == 200:
            content = response.read().decode('utf-8')
            if "Nitro" in content:
                return Fore.GREEN + "Geçerli: Nitro"
            else:
                return Fore.RED + "Geçerli değil: Nitro değil"
        else:
            return Fore.RED + "Geçersiz: Yanıt kodu {}".format(response.status)
    except Exception as e:
        return Fore.RED + "Geçersiz: {}".format(e)
    finally:
        conn.close()

def print_large_title():
    title = r"""
   ###    ######   ######   ####              ####      ###     ##      ##   ##   #####
  ## ##   ##   ##  ##      ##  ##            ##  ##    ## ##    ##      ##   ##  ##   ##
 ##   ##  ##   ##  ##      ##                ##       ##   ##   ##      ##   ##  ##   ##
 ##   ##  ##  ###  #####    #####             #####   ##   ##   ##      ### ###  ##   ##
 #######  #####    ##           ##                ##  #######   ##       #####   ##   ##
 ##   ##  ## ###   ##      ##   ##           ##   ##  ##   ##   ##   #    ###    ##   ##
 ##   ##  ##  ###  ######   #####             #####   ##   ##   ######     #      #####
    """
    print(Fore.RED + title)  # Koyu kırmızı renkli başlık

def check_codes_from_file(filename):
    """Belirtilen dosyadan kodları kontrol eder."""
    with open(filename, 'r') as file:
        codes = file.readlines()

    for code in codes:
        code = code.strip()
        if code:
            gift_url = "https://discord.gift/" + code
            print(Fore.YELLOW + "Kontrol ediliyor: {}".format(gift_url))
            result = check_gift_validity(gift_url)
            print("Sonuç: {}".format(result))
            if "Geçerli: Nitro" in result:
                print(Fore.GREEN + "Geçerli Nitro bulundu! Kodu: {}".format(code))

def main():
    print_large_title()  # ARES SALVO başlığı

    while True:
        print("Seçenekler:")
        print("1: Rastgele Nitro promo kodu oluştur ve kontrol et")
        print("2: .txt dosyası ile verilen promo kodlarını kontrol et")
        choice = input("Lütfen bir seçenek girin (1/2): ").strip()

        if choice == '1':
            while True:
                random_code = generate_random_code()
                gift_url = "https://discord.gift/" + random_code
                print(Fore.YELLOW + "Kontrol ediliyor: {}".format(gift_url))
                result = check_gift_validity(gift_url)
                print("Sonuç: {}".format(result))
                if "Geçerli: Nitro" in result:
                    print(Fore.GREEN + "Geçerli Nitro bulundu!")
                    break

                time.sleep(0.1)  # 0.1 saniye bekle

        elif choice == '2':
            filename = input("Kontrol edilecek .txt dosyasının adını girin: ").strip()
            check_codes_from_file(filename)

        else:
            print(Fore.RED + "Geçersiz seçenek, lütfen 1 veya 2 girin.")

if __name__ == "__main__":
    main()