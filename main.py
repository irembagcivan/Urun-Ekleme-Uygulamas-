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
        kayit_listele()
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

kayit_listele()

def kategoriye_gore_listele():
    listelenecek_kategori = ui.cmbKategoriListele.currentText()

    sorgu = "select * from urun where kategori = ?"
    islem.execute(sorgu,(listelenecek_kategori,))
    ui.tblListele.clear()

    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tblListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere, "Silme Onayı", "Silmek istediğinizden emin misiniz?",
                QMessageBox.Yes | QMessageBox.No)
    
    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tblListele.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()
        sorgu = "delete from urun where urunKodu = ?"
        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt başarıyla silindi!")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt silinemedi!" + str(error))

    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi!")
    
def kayit_guncelle():
    guncelle_mesaj = QMessageBox.question(pencere, "Güncelleme Onayı", "Bu kaydı güncellemek istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)

    if guncelle_mesaj == QMessageBox.Yes:
        try:
            UrunKodu = ui.lneurunKodu.text()
            UrunAdi = ui.lneurunAdi.text()
            BirimFiyat = ui.lnebirimFiyat.text()
            StokMiktari = ui.lnestokMiktari.text()
            UrunAciklama = ui.lneurunAciklama.text()
            Marka = ui.cmbMarka.currentText()
            Kategori = ui.cmbKategori.currentText()

            if UrunAdi == "" and BirimFiyat == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "":
                islem.execute("update urun set kategori = ? where urunKodu = ?", (Kategori, UrunKodu))

            elif UrunAdi == "" and BirimFiyat == "" and StokMiktari == "" and UrunAciklama == "" and Kategori == "":
                islem.execute("update urun set marka = ? where urunKodu = ?", (Marka, UrunKodu))
            
            elif UrunAdi == "" and BirimFiyat == "" and StokMiktari == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set urunAciklamasi = ? where urunKodu = ?", (UrunAciklama, UrunKodu))
            
            elif UrunAdi == "" and BirimFiyat == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set stokMiktari = ? where urunKodu = ?", (StokMiktari, UrunKodu))
            
            elif UrunAdi == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set birimFiyat = ? where urunKodu = ?", (BirimFiyat, UrunKodu))
             
            elif BirimFiyat == "" and StokMiktari  == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set urunAdi = ? where urunKodu = ?", (UrunAdi, UrunKodu))

            else:
                islem.execute("update urun set urunAdi = ?, birimFiyat = ?, stokMiktari = ?, urunAciklamasi = ?, marka = ?, kategori = ?, where urunKodu = ?", (UrunAdi, BirimFiyat, StokMiktari, UrunAciklama, Marka, Kategori, UrunKodu))
            baglanti.commit()
            kayit_listele()
            ui.statusbar.showMessage("Kayıt başarıyla güncellendi!")
        except Exception as error:
            ui.statusbar.showMessage("Kayıt güncellemede hata çıktı " + str(error))
    
    else:
        ui.statusbar.showMessage("Güncelleme iptal edildi!")
            

                            
                                                          

# Buton işlemleri
ui.btnEkle.clicked.connect(kayit_ekle)
ui.btnListele.clicked.connect(kayit_listele)
ui.btnKategoriyeGoreListele.clicked.connect(kategoriye_gore_listele)
ui.btnSil.clicked.connect(kayit_sil)
ui.btnGuncelle.clicked.connect(kayit_guncelle)
sys.exit(uygulama.exec_())
