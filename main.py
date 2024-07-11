import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from arayuz import *

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()


# Veritabanı işlemleri
import sqlite3

baglanti = sqlite3.connect("urunler.db") # oluşturmak istediğimiz database ismi
islem = baglanti.cursor() # imleç
baglanti.commit() # yapmış olduğumuz işlemleri veritabanında kayıt etme 

table = islem.execute("create table if not exists urun (urunKodu int, urunAdi text, birimFiyat int,\
                      stokMiktari int, urunAciklamasi text, marka text, kategori text)") 
""" Oluşturduğumuz tablo bir sonraki çalışmada veritabanında yoksa, oluşturulur; tablo veri tabanında varsa var olan tablo
üzerinden işlemleri gerçekleştirecektir."""
baglanti.commit()

def kayit_ekle():
    UrunKodu = int(ui.lneurunKodu.text())
    UrunAdi = ui.lneurunAdi.text()
    BirimFiyat = int(ui.lnebirimFiyat.text())
    StokMiktari = int(ui.lnestokMiktari.text())
    UrunAciklama = ui.lneurunAciklama.text()
    Marka = ui.cmbMarka.currentText() # o an seçilmiş 1olan alanın texti alınır.
    Kategori = ui.cmbKategori.currentText()

    try:
        ekle = "insert into urun (urunKodu,urunAdi,birimFiyat,stokMiktari,urunAciklamasi,marka,kategori)\
            values (?,?,?,?,?,?,?)"
        islem.execute(ekle,(UrunKodu,UrunAdi,BirimFiyat,StokMiktari,UrunAciklama,Marka,Kategori))
        baglanti.commit()
        ui.statusbar.showMessage("Kayıt ekleme işlemi başarılı!", 10000)

    except Exception as error:
        ui.statusbar.showMessage("Kayıt eklenemedi!" + str(error))

def kayit_listele():
    ui.tblListele.clear()
    ui.tblListele.setHorizontalHeaderLabels(("Ürün Kodu", "Ürün Adı", "Birim Fiyatı", "Stok Miktarı", "Ürün Açıklama",
                                             "Marka", "Kategori" ))
    sorgu = "select * from urun"
    islem.execute(sorgu)

    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tblListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

def kategoriye_gore_listele():
    listelenecek_kategori = ui.cmbKategoriListele.currentText()

    sorgu = "select * from urun where kategori = ?"
    islem.execute(sorgu,(listelenecek_kategori,))
    ui.tblListele.clear()

    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tblListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))




                                                          

# Buton işlemleri
ui.btnEkle.clicked.connect(kayit_ekle)
ui.btnListele.clicked.connect(kayit_listele)
ui.btnKategoriyeGoreListele.clicked.connect(kategoriye_gore_listele)


sys.exit(uygulama.exec_())
