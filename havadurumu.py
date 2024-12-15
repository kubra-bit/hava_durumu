import  requests
from pymongo import MongoClient
from prettytable import PrettyTable
client=MongoClient("mongodb://localhost:27017")
db=client["hava_durumu"]
sehirler=db["sehirler"]
def add_sehir(sehir,sicaklik,hissedilen_sicaklik,min_sicaklik,max_sicaklik,hava):
    veri={"name":sehir,"sicaklik":sicaklik,"hissedilen_sicaklik":hissedilen_sicaklik,"min_sicaklik":min_sicaklik,"max_sicaklik":max_sicaklik,"hava":hava}
    sehirler.insert_one(veri)
    print("sehir eklendi")
def print_sehirler():
    sh=sehirler.find()
    table=PrettyTable(["sehir","sicaklik","hissedilen sicaklik","min sicaklik","max sicaklik","hava"])
    for sehir in sh:
        table.add_row([str(sehir["name"]),f"{sehir["sicaklik"]:.2f}",f"{sehir["hissedilen_sicaklik"]:.2f}",f"{sehir["min_sicaklik"]:.2f}",f"{sehir["max_sicaklik"]:.2f}",str(sehir["hava"])])
    print(table)
def delete_sehir(name):
    sehirler.find({"name":name})
    print(f"{sehir} sehri tablodan silindi")


icerik="""
--------HAVA DURUMU SİSTEMİ-------
1. sehir ekle
2. sehirleri liste
3.sehir sil
4.cikis
"""
def main():
    while True:
        print(icerik)
        choice=int(input("tercihiniz:"))
        if choice==1:
            sehir=input("hava durumunu ogrenmek istediginiz sehri giriniz:")
            url = f"https://api.openweathermap.org/data/2.5/weather?q={sehir}&appid=99c93aeb6b44df36f8dea4d527eac439"
            istek = requests.get(url)
            veri = istek.json()
            sicaklik=veri["main"]["temp"]-273.15
            hissedilen_sicaklik=veri["main"]["feels_like"]-273.15
            min_sicaklik=veri["main"]["temp_min"]-273.15
            max_sicaklik=veri["main"]["temp_max"]-273.15
            hava=veri["weather"][0]["description"]
            add_sehir(sehir,sicaklik,hissedilen_sicaklik,min_sicaklik,max_sicaklik,hava)

        elif choice==2:
            print_sehirler()
        elif choice==3:
            name=input("silinmesini istediginiz sehri giriniz:")
            delete_sehir(name)
        elif choice==4:
            break
        else:
            print("yanlis secim yaptiniz")
if __name__=="__main__":
    main()


