import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import json
import os
from tkinter import filedialog
def bireysel_kullanici_sayfasi(user):
   
    def Sifre_degistir(user):
        # Veritabanı bağlantısını burada aç
        conn = sqlite3.connect("veritabanim.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT parolaistek FROM kullanicilar WHERE id = ?", (user[0],))
        parolaistek = cursor.fetchone()[0]
        
        if parolaistek == 0:
            # Şifre değiştirilemez, uyarı göster
            messagebox.showwarning("Uyarı", "Şifre değiştirme talebinde bulunun.")
        elif parolaistek == 1:
            # Şifre değiştirme sayfası
            sifre_degistir_penceresi(user, conn, cursor)
        


    def sifre_degistir_penceresi(user, conn, cursor):
        # Şifre değiştirme penceresi
        sifre_degistir_pencere = Toplevel()
        sifre_degistir_pencere.title("Şifre Değiştir")
        
        Label(sifre_degistir_pencere, text="Eski Şifre:").pack(pady=5)
        eski_sifre_entry = Entry(sifre_degistir_pencere, show="*")
        eski_sifre_entry.pack(pady=5)

        Label(sifre_degistir_pencere, text="Yeni Şifre:").pack(pady=5)
        yeni_sifre_entry = Entry(sifre_degistir_pencere, show="*")
        yeni_sifre_entry.pack(pady=5)

        Label(sifre_degistir_pencere, text="Yeni Şifreyi Tekrar:").pack(pady=5)
        yeni_sifre_tekrar_entry = Entry(sifre_degistir_pencere, show="*")
        yeni_sifre_tekrar_entry.pack(pady=5)

        def sifre_degistir():
            eski_sifre = eski_sifre_entry.get()
            yeni_sifre = yeni_sifre_entry.get()
            yeni_sifre_tekrar = yeni_sifre_tekrar_entry.get()

            # Eski şifreyi doğrula
            cursor.execute("SELECT sifre FROM kullanicilar WHERE id = ?", (user[0],))
            mevcut_sifre = cursor.fetchone()[0]
            
            if eski_sifre != mevcut_sifre:
                messagebox.showerror("Hata", "Eski şifre yanlış!")
            elif yeni_sifre != yeni_sifre_tekrar:
                messagebox.showerror("Hata", "Yeni şifreler uyuşmuyor!")
            elif len(yeni_sifre) < 6:
                messagebox.showerror("Hata", "Şifre en az 6 karakter olmalıdır.")
            else:
                # Yeni şifreyi veritabanına kaydet
                cursor.execute("UPDATE kullanicilar SET sifre = ? WHERE id = ?", (yeni_sifre, user[0]))
                conn.commit()
                messagebox.showinfo("Başarılı", "Şifre başarıyla değiştirildi.")
                sifre_degistir_pencere.destroy()

        Button(sifre_degistir_pencere, text="Şifreyi Değiştir", command=sifre_degistir).pack(pady=10)
        Button(sifre_degistir_pencere, text="İptal", command=sifre_degistir_pencere.destroy).pack(pady=5)

    def takim_olustur():
        def takim_ekle():
            takim_adi = entry_takim_adi.get()
            secilen_kullanicilar = [kullanici_listesi.get(idx) for idx in kullanici_listesi.curselection()]

            if not takim_adi:
                messagebox.showerror("Hata", "Takım adını girin!")
                return
            
            if not secilen_kullanicilar:
                messagebox.showerror("Hata", "En az bir kullanıcı seçmelisiniz!")
                return

            conn = sqlite3.connect("veritabanim.db")
            cursor = conn.cursor()

            try:
                # Takımı ekle
                cursor.execute("INSERT INTO takimlar (takim_adi) VALUES (?)", (takim_adi,))
                conn.commit()


                # Takımın ID'sini al
                cursor.execute("SELECT id FROM takimlar WHERE takim_adi = ?", (takim_adi,))
                takim_id = cursor.fetchone()[0]

                # Kurucuyu takıma ekle
                cursor.execute("INSERT INTO takim_uyeleri (takim_id, kullanici_id) VALUES (?, ?)", (takim_id, user[0]))

                # Takım üyelerini ekle
                # Takım davetlerini gönder
                for secilen in secilen_kullanicilar:
                    cursor.execute("SELECT id FROM kullanicilar WHERE kullanici_adi = ?", (secilen,))
                    kullanici_id = cursor.fetchone()[0]
                    
                    # Kullanıcının bildirimlerine davet ekle
                    cursor.execute("SELECT bildirimler FROM kullanicilar WHERE id = ?", (kullanici_id,))
                    bildirimler = json.loads(cursor.fetchone()[0])
                    bildirimler.append(f"{user[1]} sizi '{takim_adi}' takımına davet etti.")
                    cursor.execute("UPDATE kullanicilar SET bildirimler = ? WHERE id = ?", (json.dumps(bildirimler), kullanici_id))

                conn.commit()
                messagebox.showinfo("Başarılı", f"'{takim_adi}' takımı başarıyla oluşturuldu ve davetler gönderildi!")
                takim_pencere.destroy()
                
                
            
           
            except sqlite3.IntegrityError:
                messagebox.showerror("Hata", "Takım adı zaten mevcut!")
            finally:
                conn.close()

        takim_pencere = Toplevel()
        takim_pencere.title("Takım Oluştur")

        Label(takim_pencere, text="Takım Adı:").pack()
        entry_takim_adi = Entry(takim_pencere)
        entry_takim_adi.pack()

        Label(takim_pencere, text="Takım Üyeleri:").pack()
        kullanici_listesi = Listbox(takim_pencere, selectmode=MULTIPLE, height=10, width=30)
        kullanici_listesi.pack()

        conn = sqlite3.connect("veritabanim.db")
        cursor = conn.cursor()
        cursor.execute("SELECT kullanici_adi FROM kullanicilar WHERE rol = 'Bireysel Kullanıcı' AND id != ?", (user[0],))
        bireysel_kullanicilar = cursor.fetchall()
        conn.close()

        for kullanici in bireysel_kullanicilar:
            kullanici_listesi.insert(END, kullanici[0])

        Button(takim_pencere, text="Takım Oluştur", command=takim_ekle).pack()

    def takimlarimi_gor():
        
        def takim_uyelerini_goster():
            secilen_takim = takim_listesi.get(ACTIVE)
            if not secilen_takim:
                messagebox.showerror("Hata", "Bir takım seçin!")
                return

            conn = sqlite3.connect("veritabanim.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM takimlar WHERE takim_adi = ?", (secilen_takim,))
            takim_id = cursor.fetchone()[0]

            cursor.execute("""
            SELECT kullanicilar.kullanici_adi 
            FROM takim_uyeleri
            INNER JOIN kullanicilar ON takim_uyeleri.kullanici_id = kullanicilar.id
            WHERE takim_uyeleri.takim_id = ?
            """, (takim_id,))
            uyeler = cursor.fetchall()
            conn.close()

            takim_uyeleri_pencere = Toplevel()
            takim_uyeleri_pencere.title(f"'{secilen_takim}' Takım Üyeleri")

            for uye in uyeler:
                Label(takim_uyeleri_pencere, text=uye[0]).pack()


        takimlar_pencere = Toplevel()
        takimlar_pencere.title("Takımlarım")

        takim_listesi = Listbox(takimlar_pencere, height=10, width=30)
        takim_listesi.pack()

        conn = sqlite3.connect("veritabanim.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT takimlar.takim_adi 
        FROM takimlar
        INNER JOIN takim_uyeleri ON takimlar.id = takim_uyeleri.takim_id
        WHERE takim_uyeleri.kullanici_id = ?
        """, (user[0],))
        takımlar = cursor.fetchall()
        conn.close()

        for takim in takımlar:
            takim_listesi.insert(END, takim[0])

        Button(takimlar_pencere, text="Üyeleri Göster", command=takim_uyelerini_goster).pack()

    def kullanici_adi_degistir():
        def degistir():
            yeni_kullanici_adi = entry_kullanici_adi.get()
            if not yeni_kullanici_adi:
                messagebox.showerror("Hata", "Yeni kullanıcı adını girin!")
                return

            conn = sqlite3.connect("veritabanim.db")
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE kullanicilar SET kullanici_adi = ? WHERE id = ?",
                               (yeni_kullanici_adi, user[0]))
                conn.commit()
                messagebox.showinfo("Başarılı", "Kullanıcı adı başarıyla değiştirildi!")
                kullanici_adi_pencere.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Hata", "Kullanıcı adı zaten mevcut!")
            finally:
                conn.close()

        kullanici_adi_pencere = Toplevel()
        kullanici_adi_pencere.title("Kullanıcı Adı Değiştir")

        Label(kullanici_adi_pencere, text="Yeni Kullanıcı Adı:").pack()
        entry_kullanici_adi = Entry(kullanici_adi_pencere)
        entry_kullanici_adi.pack()

        Button(kullanici_adi_pencere, text="Değiştir", command=degistir).pack()



    def parola_degistirme_istegi():
        try:
            conn = sqlite3.connect("veritabanim.db")
            cursor = conn.cursor()
            
            # Kullanıcının parola isteğini kontrol et
            cursor.execute("SELECT parolaistek FROM kullanicilar WHERE id = ?", (user[0],))
            parolaistek = cursor.fetchone()[0]

            if parolaistek == 1:
                messagebox.showinfo("Uyarı", "Zaten onaylanmış bir parola değişikliği talebiniz var.")
            else:
                # Sistem yöneticisine bildirim ekle
                cursor.execute("SELECT bildirimler FROM kullanicilar WHERE rol = 'Sistem Yöneticisi'")
                admin_bildirimler = cursor.fetchall()

                for admin_bildirim in admin_bildirimler:
                    bildirimler = json.loads(admin_bildirim[0])

                    yeni_bildirim = f"{user[1]} parola değiştirme isteği gönderdi."
                    bildirimler.append(yeni_bildirim)

                    # Sistem yöneticisinin bildirimlerini güncelle
                    cursor.execute("UPDATE kullanicilar SET bildirimler = ? WHERE rol = 'Sistem Yöneticisi'",
                                (json.dumps(bildirimler),))

                # Kullanıcının parolaistek değerini güncelle
                cursor.execute("UPDATE kullanicilar SET parolaistek = 0 WHERE id = ?", (user[0],))

                conn.commit()
                messagebox.showinfo("Başarılı", "Parola değiştirme talebiniz sistem yöneticisine gönderildi.")
            conn.close()
        except Exception as e:
            messagebox.showerror("Hata", f"Parola değiştirme isteği gönderilirken bir hata oluştu: {str(e)}")

    
     
    def bildirimleri_goster():
        def bildirim_isle(bildirim, action):
            try:
                if "takımına davet etti" in bildirim:
                    # Takım adı ve davet göndereni ayıkla
                    takim_adi = bildirim.split("'")[1]
                    conn = sqlite3.connect("veritabanim.db")
                    cursor = conn.cursor()

                    # Takım bilgisi al
                    cursor.execute("SELECT id FROM takimlar WHERE takim_adi = ?", (takim_adi,))
                    takim_id = cursor.fetchone()[0]

                    if action == "Kabul":
                        # Kullanıcıyı takıma ekle
                        cursor.execute("INSERT INTO takim_uyeleri (takim_id, kullanici_id) VALUES (?, ?)", (takim_id, user[0]))

                   
                   
                    # Bildirimi kaldır
                    cursor.execute("SELECT bildirimler FROM kullanicilar WHERE id = ?", (user[0],))
                    bildirimler = json.loads(cursor.fetchone()[0])
                    bildirimler.remove(bildirim)
                    cursor.execute("UPDATE kullanicilar SET bildirimler = ? WHERE id = ?", (json.dumps(bildirimler), user[0]))

                    conn.commit()
                    if action == "Kabul":
                        messagebox.showinfo("Başarılı", f"'{takim_adi}' takımına başarıyla katıldınız!")
                    elif action == "Reddet":
                        messagebox.showinfo("Red Edildi", f"'{takim_adi}' takımına katılma daveti reddedildi.")
                conn.close()
            except Exception as e:
                messagebox.showerror("Hata", f"Bildirim işlenirken bir hata oluştu: {str(e)}")

        # Bildirimleri al ve pencere oluştur
        conn = sqlite3.connect("veritabanim.db")
        cursor = conn.cursor()
        cursor.execute("SELECT bildirimler FROM kullanicilar WHERE id = ?", (user[0],))
        bildirimler = json.loads(cursor.fetchone()[0])
        conn.close()

        bildirimler_pencere = Toplevel()
        bildirimler_pencere.title("Bildirimler")
        print(bildirimler)
        for bildirim in bildirimler:
            frame = Frame(bildirimler_pencere)
            frame.pack(pady=5)
            Label(frame, text=bildirim, wraplength=300).pack(side=LEFT)
            if "parola değiştirme isteği" in bildirim:
                Label(frame, text="Parola değiştirme isteği: Lütfen işlemi tamamlayın.", wraplength=300).pack(side=LEFT)

            if "takımına davet etti" in bildirim:
                Button(frame, text="Kabul", command=lambda b=bildirim: bildirim_isle(b, "Kabul")).pack(side=LEFT)
                Button(frame, text="Reddet", command=lambda b=bildirim: bildirim_isle(b, "Reddet")).pack(side=LEFT)


    def dosya_yukle():
        dosya_yolu = filedialog.askopenfilename()
        if not dosya_yolu:
            return

        dosya_adi = os.path.basename(dosya_yolu)
        erisebilen_kullanici_id = str(user[0])  # Kullanıcı ID'si
        
        conn = sqlite3.connect("veritabanim.db")
        cursor = conn.cursor()

        try:
            # Aynı dosya adı ve aynı kullanıcı ID'si varsa tekrar eklemeyelim
            cursor.execute("""
            SELECT * FROM dosyalar 
            WHERE dosya_adi = ? AND erisebilen_kullanici_id = ?
            """, (dosya_adi, erisebilen_kullanici_id))
            mevcut_dosya = cursor.fetchone()

            if mevcut_dosya:
                messagebox.showinfo("Bilgi", f"{dosya_adi} zaten yüklenmiş.")
            else:
                cursor.execute("""
                INSERT INTO dosyalar (dosya_adi, dosya_yolu, erisebilen_kullanici_id)
                VALUES (?, ?, ?)
                """, (dosya_adi, dosya_yolu, erisebilen_kullanici_id))
                conn.commit()
                messagebox.showinfo("Başarılı", f"{dosya_adi} başarıyla yüklendi!")

        except Exception as e:
            messagebox.showerror("Hata", str(e))
        finally:
            conn.close()
    def dosya_paylas():
        # İlk pencere: Kullanıcının sahip olduğu dosyaları seçmesi için
        dosyalar_pencere = Toplevel()
        dosyalar_pencere.title("Dosya Seç")

        dosya_listesi = Listbox(dosyalar_pencere, height=15, width=50)
        dosya_listesi.pack()

        conn = sqlite3.connect("veritabanim.db")
        cursor = conn.cursor()

        try:
            # Giriş yapan kullanıcıya ait dosyaları çek
            cursor.execute("""
            SELECT id, dosya_adi, dosya_yolu 
            FROM dosyalar
            WHERE erisebilen_kullanici_id = ?
            """, (str(user[0]),))
            dosyalar = cursor.fetchall()

            for dosya in dosyalar:
                dosya_listesi.insert(END, dosya[1])

        except Exception as e:
            messagebox.showerror("Hata", str(e))
            dosyalar_pencere.destroy()
            conn.close()  # Hata durumunda bağlantıyı kapat
            return

        def sonraki_adim():
            # Kullanıcı bir dosya seçti mi kontrol et
            secilen_idx = dosya_listesi.curselection()
            if not secilen_idx:
                messagebox.showerror("Hata", "Bir dosya seçmelisiniz!")
                return

            # Seçilen dosyanın bilgilerini al
            secilen_dosya = dosyalar[secilen_idx[0]]
            dosya_id, dosya_adi, dosya_yolu = secilen_dosya

            dosyalar_pencere.destroy()  # İlk pencereyi kapat

            # İkinci pencere: Takım üyelerini seçmek için
            takim_pencere = Toplevel()
            takim_pencere.title("Kullanıcı Seç")

            uye_listesi = Listbox(takim_pencere, height=15, width=50)
            uye_listesi.pack()

            try:
                # Takım üyesi olan diğer kullanıcıları çek
                cursor.execute("""
                SELECT DISTINCT kullanicilar.id, kullanicilar.kullanici_adi
                FROM kullanicilar
                INNER JOIN takim_uyeleri ON kullanicilar.id = takim_uyeleri.kullanici_id
                WHERE kullanicilar.id != ?
                """, (user[0],))
                takim_uyeleri = cursor.fetchall()

                for uye in takim_uyeleri:
                    uye_listesi.insert(END, uye[1])

            except Exception as e:
                messagebox.showerror("Hata", str(e))
                takim_pencere.destroy()
                return

            def kullaniciya_dosya_paylas():
                # Kullanıcı bir üye seçti mi kontrol et
                secilen_idx = uye_listesi.curselection()
                if not secilen_idx:
                    messagebox.showerror("Hata", "Bir kullanıcı seçmelisiniz!")
                    return

                # Seçilen üyenin bilgilerini al
                secilen_uye = takim_uyeleri[secilen_idx[0]]
                hedef_kullanici_id = str(secilen_uye[0])

                try:
                    # Dosyayı seçilen kullanıcıya paylaş
                    cursor.execute("""
                    INSERT INTO dosyalar (dosya_adi, dosya_yolu, erisebilen_kullanici_id)
                    VALUES (?, ?, ?)
                    """, (dosya_adi, dosya_yolu, hedef_kullanici_id))
                    conn.commit()
                    messagebox.showinfo("Başarılı", f"{dosya_adi} başarıyla paylaşıldı!")

                except Exception as e:
                    messagebox.showerror("Hata", str(e))

                finally:
                    takim_pencere.destroy()

            Button(takim_pencere, text="Paylaş", command=kullaniciya_dosya_paylas).pack()

        Button(dosyalar_pencere, text="Sonraki", command=sonraki_adim).pack()

        # Bağlantıyı burada kapatmak için bağlantıyı pencere kapatmadan sonra bırakıyoruz


    def dosyalarimi_gor():
        dosyalar_pencere = Toplevel()
        dosyalar_pencere.title("Dosyalarım")

        dosya_listesi = Listbox(dosyalar_pencere, height=15, width=50)
        dosya_listesi.pack()

        conn = sqlite3.connect("veritabanim.db")
        cursor = conn.cursor()

        try:
            # Giriş yapan kullanıcıya ait dosyaları al
            cursor.execute("""
            SELECT dosya_adi, dosya_yolu 
            FROM dosyalar
            WHERE erisebilen_kullanici_id = ?
            """, (str(user[0]),))
            dosyalar = cursor.fetchall()

            for dosya in dosyalar:
                dosya_listesi.insert(END, dosya[0])

        except Exception as e:
            messagebox.showerror("Hata", str(e))
        finally:
            conn.close()

        def dosya_ac():
            secilen_idx = dosya_listesi.curselection()
            if not secilen_idx:
                messagebox.showerror("Hata", "Bir dosya seçmelisiniz!")
                return
            
            secilen_dosya_yolu = dosyalar[secilen_idx[0]][1]
            os.startfile(secilen_dosya_yolu)

        Button(dosyalar_pencere, text="Aç", command=dosya_ac).pack()


    def cikis_yap():
        bireysel_pencere.destroy()

   
   
   
    bireysel_pencere = Toplevel()
    bireysel_pencere.title("Bireysel Kullanıcı Paneli")
    
    
    
    # Kullanıcı paneline butonu ekleme
    Button(bireysel_pencere, text="Takımlarım", command=takimlarimi_gor).pack(pady=5)
    Button(bireysel_pencere, text="Takım Oluştur", command=takim_olustur).pack(pady=5)
    Button(bireysel_pencere, text="Kullanıcı Adı Değiştir", command=kullanici_adi_degistir).pack(pady=5)
    Button(bireysel_pencere, text="Parola Değiştirme İsteği Gönder", command=parola_degistirme_istegi).pack(pady=5)
    Button(bireysel_pencere, text="Bildirimleri Göster", command=bildirimleri_goster).pack(pady=5)
    Button(bireysel_pencere, text="Çıkış", command=cikis_yap).pack(pady=5)
    Button(bireysel_pencere, text="Dosya Yükle", command=dosya_yukle).pack(pady=5)
    Button(bireysel_pencere, text="Dosya Paylaş", command=dosya_paylas).pack(pady=5)
    Button(bireysel_pencere, text="Dosyalarımı Gör", command=dosyalarimi_gor).pack(pady=5)
    Button(bireysel_pencere, text="Şifre değiştir", command=lambda: Sifre_degistir(user)).pack(pady=5)


