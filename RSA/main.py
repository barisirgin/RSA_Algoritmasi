import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# Girilen sayilarin asal olup olmadiini kontrol eder.
def asal_mi(n):
    test = 3
    if n % 2 == 0:
        return False
    while test < n:
        if n % test == 0:
            return False
        test += 2
    return True

# Oklid algoritması kullanarak E ile Q(n) in aralarinda asalligi kontrol edilir.
def oklid(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def anahtar_olustur(p, q):
    if not (asal_mi(p) and asal_mi(q)):
        raise ValueError('Her iki sayı da asal olmalıdır.')
    elif p == q:
        raise ValueError('p ve q aynı degeri alamaz')

    # N = P * Q
    n = p * q

    # Q(n) = (p-1) * (q-1)
    phi = (p-1) * (q-1)

    # E açık anahtar değerini gir
    e = int(input("E açık anahtarını Giriniz : "))

    # 1 < E < Q(n) - E ve Q(n) aralarında asal olacak sekilde olusmasi için oklid algoritmasi kullan.
    g = oklid(e, phi)
    while g != 1:
        g = oklid(e, phi)

    # Özel anahtarı oluşturmak için Genişletilmiş Öklid Algoritmasını kullanın
    d = D_anahtar_bulma(e, phi)

    # Genel anahtar (e, n) ve özel anahtar (d, n)
    print(f"(E,n) : {e,n}\n(D,n) : {d,n}")
    return ((e, n), (d, n))

#Girilen E degerine uygun D gizli anahtarini olusturur.
def D_anahtar_bulma(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

#Girilen metni şifreleyen Fonksiyon
def sifreleme(pk, plaintext):
    # Anahtarı bileşenlerine ayırın
    key, n = pk
    # a^b mod m kullanarak düz metindeki her harfi karaktere göre sayılara dönüştürün
    cipher = [pow(ord(char), key, n) for char in plaintext]
    # bayt dizisini döndür
    return cipher

#Şifrelenmiş metni deşifreleyen fonksiyon
def desifreleme(pk, ciphertext):
    # Anahtarı bileşenlerine ayırın
    key, n = pk
    # a^b mod m kullanarak şifreli metne ve anahtara dayalı olarak düz metin oluşturun
    aux = [str(pow(char, key, n)) for char in ciphertext]
    # bayt dizisini bir dize olarak döndür
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


if __name__ == '__main__':

    print("================================== RSA Şifreleme / Deşifreleme ==============================================")

    p = int(input(" - P değerini giriniz :  "))
    q = int(input(" - Q değerini giriniz (P değerinden farklı bir asal sayi olacak):  "))

    print(f"{Fore.LIGHTYELLOW_EX} - Anahtar çifti oluşturuluyor . . .")

    public, private = anahtar_olustur(p, q)

    print(f"{Fore.LIGHTYELLOW_EX} - Genel Anahtarınız : {public} \n - Gizli Anahtarınız : {private}")

    message = input(" - Şifrelenecek Mesajı Giriniz :  ")
    encrypted_msg = sifreleme(public, message)

    print(f"{Fore.LIGHTYELLOW_EX} - Şifreli mesajınız: ", ''.join(map(lambda x: str(x), encrypted_msg)))
    print(" - Özel anahtarla mesajın şifresini çözme ", private, " . . .")
    print(f"{Fore.LIGHTYELLOW_EX} - Deşifrelenmiş mesajınız :  {desifreleme(private, encrypted_msg)}")

