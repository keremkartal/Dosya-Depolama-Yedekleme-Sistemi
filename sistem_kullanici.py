import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import json
import os
from tkinter import filedialog


def sistem_kullanici_sayfasi(user):
    
    def kullanici_profilleri_yonet():
    # Kullanıcı profillerini düzenleme arayüzü burada tanımlanır
        messagebox.showinfo("Kullanıcı Profilleri", "Kullanıcı profilleri yönetme arayüzü.")
    def depolama_limitlerini_kontrol_et():
        # Depolama limitlerini düzenleme arayüzü burada tanımlanır
        messagebox.showinfo("Depolama Limitleri", "Depolama limitlerini kontrol etme arayüzü.")
   
    
    def cikis_yap():
        sistem_pencere.destroy()


    def bildirimleri_goster(user):
        
        def bildirim_isle(bildirim, action):
            print(bildirim)
            print("Bildirim okundu.")

            try:
                conn = sqlite3.connect("veritabanim.db")
                cursor = conn.cursor()

                # Bildirimin parola değiştirme isteği olup olmadığını kontrol et
                if "parola değiştirme isteği gönderdi" in bildirim:
                    kullanici_adi = bildirim.split()[0]  # Kullanıcı adı, bildirimin ilk kısmı
                    print(f"Kullanıcı Adı: {kullanici_adi}")
                    
                    # Parola isteğini onayla ya da reddet
                    if action == "Kabul":
                        # Parola isteğini onayla
                        cursor.execute("UPDATE kullanicilar SET parolaistek = 1 WHERE kullanici_adi = ?", (kullanici_adi,))
                        bildirimi = "Şifre değiştirme işlemine onay verildi"
                        cursor.execute("UPDATE kullanicilar SET bildirimler = ? WHERE kullanici_adi = ?",
                                    (json.dumps([bildirimi]), kullanici_adi))
                        messagebox.showinfo("Onaylandı", f"Kullanıcı '{kullanici_adi}' parola değiştirme isteği onaylandı.")
                    
                    elif action == "Reddet":
                        # Parola isteğini reddet
                        cursor.execute("UPDATE kullanicilar SET parolaistek = 0 WHERE kullanici_adi = ?", (kullanici_adi,))
                        bildirimi = "Şifre değiştirme işlemine onay verilmedi"
                        cursor.execute("UPDATE kullanicilar SET bildirimler = ? WHERE kullanici_adi = ?",
                                    (json.dumps([bildirimi]), kullanici_adi))
                        messagebox.showinfo("Reddedildi", f"Kullanıcı '{kullanici_adi}' parola değiştirme isteği reddedildi.")
                    
                    # Kullanıcıya bildirim gönderildiğini bildir
                    print("İşlem tamamlandı.")
                    
                # Bildirimi sistem yöneticisinin listelerinden kaldır
                cursor.execute("SELECT bildirimler FROM kullanicilar WHERE id = ?", (user[0],))
                bildirimler = json.loads(cursor.fetchone()[0])
                if bildirim in bildirimler:
                    bildirimler.remove(bildirim)
                    cursor.execute("UPDATE kullanicilar SET bildirimler = ? WHERE id = ?", (json.dumps(bildirimler), user[0]))
                    
                conn.commit()
                conn.close()
            except Exception as e:
                messagebox.showerror("Hata", f"Bildirim işlenirken bir hata oluştu: {str(e)}")

        # Bildirimleri Al ve Göster
        conn = sqlite3.connect("veritabanim.db")
        cursor = conn.cursor()
        cursor.execute("SELECT bildirimler FROM kullanicilar WHERE id = ?", (user[0],))
        bildirimler = json.loads(cursor.fetchone()[0])
        conn.close()

        # Bildirimler penceresi
        bildirimler_pencere = Toplevel()
        bildirimler_pencere.title("Bildirimler")

        for bildirim in bildirimler:
            frame = Frame(bildirimler_pencere)
            frame.pack(pady=5)
            Label(frame, text=bildirim, wraplength=300).pack(side=LEFT)

            # Parola değiştirme talebi için işlem butonları
            if "parola değiştirme isteği gönderdi" in bildirim:
                kabul_button = Button(frame, text="Kabul", command=lambda b=bildirim: bildirim_isle(b, "Kabul"))
                kabul_button.pack(side=LEFT, padx=5)

                red_button = Button(frame, text="Reddet", command=lambda b=bildirim: bildirim_isle(b, "Reddet"))
                red_button.pack(side=LEFT, padx=5)

    sistem_pencere = Toplevel()
    sistem_pencere.title("Sistem Yöneticisi Paneli")

    # Kullanıcı paneline butonlar ekleme
    Button(sistem_pencere, text="Kullanıcı Profillerini Yönet", command=kullanici_profilleri_yonet).pack(pady=5)
    Button(sistem_pencere, text="Depolama Limitlerini Kontrol Et", command=depolama_limitlerini_kontrol_et).pack(pady=5)
    Button(sistem_pencere, text="Bildirimleri Göster", command=lambda: bildirimleri_goster(user)).pack(pady=5)

    # Button(sistem_pencere, text="Kullanıcı Dokümanlarına Eriş", command=kullanici_dokumanlarini_gor).pack(pady=5)
    # Button(sistem_pencere, text="Paylaşımlara Eriş", command=kullanici_paylasimlarini_gor).pack(pady=5)
    # Button(sistem_pencere, text="Şifrelenmiş Parolalara Eriş", command=sifrelenmis_parolalari_gor).pack(pady=5)
    # Button(sistem_pencere, text="Log Dosyalarını Gör", command=log_dosyalarini_gor).pack(pady=5)
    Button(sistem_pencere, text="Çıkış", command=cikis_yap).pack(pady=5)

    sistem_pencere.protocol("WM_DELETE_WINDOW", cikis_yap)  # Pencereyi kapatma işlevi

