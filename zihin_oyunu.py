import tkinter as tk
from tkinter import messagebox
import random
import webbrowser
import os
import tempfile
from pathlib import Path

# --- 1. OYUNUN BAŞLANGIÇ VERİLERİ ---
gizli_kimlik = 1
tur = 1
stres = 25
taban_nabiz = 80
anlik_nabiz = 80
goz_bebegi = 4.0
anlik_goz = 4.0
ses_titremesi = 5
oyun_bitti = False
ekg_sayac = 0

def yeni_oyun_baslat():
    global gizli_kimlik, tur, stres, taban_nabiz, anlik_nabiz, goz_bebegi, anlik_goz, ses_titremesi, oyun_bitti
    gizli_kimlik = random.randint(1, 3)
    tur = 1
    stres = 25
    oyun_bitti = False
    ses_titremesi = 5

    if gizli_kimlik == 1:   # Masum Mühendis
        taban_nabiz = 82
        goz_bebegi = 4.2
    elif gizli_kimlik == 2: # Eğitimli Köstebek
        taban_nabiz = 65
        goz_bebegi = 4.0
    else:                   # Sentetik Android
        taban_nabiz = 60
        goz_bebegi = 3.5

    anlik_nabiz = taban_nabiz
    anlik_goz = goz_bebegi

    lbl_diyalog.config(
        text="Yeni şüpheli sorgu odasına alındı.\nÖnce üstteki turuncu butondan Web Raporunu incele, sonra sorguya başla!",
        fg="white"
    )
    biyometri_yazisini_guncelle()

def biyometri_yazisini_guncelle():
    lbl_biyometri.config(
        text=f"Nabız: {anlik_nabiz} BPM (Taban: {taban_nabiz})   |   Göz Bebeği: {anlik_goz} mm   |   Ses Titremesi: %{ses_titremesi}"
    )

# --- 2. ZIRHLI WEB SAYFASI AÇMA FONKSİYONU (ASLA HATA VERMEZ) ---
def web_kanit_ac():
    html_icerik = f"""<!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>Gizli Adli Tıp Raporu</title></head>
    <body style="background-color:#121212; color:#00ff9d; font-family:Consolas, monospace; padding:30px;">
        <h1>MERKEZ KOMUTANLIK - GİZLİ KANIT VE PROFİL DOSYASI</h1>
        <hr style="border-color:#00ff9d;">
        <p><b>OLAY:</b> Savunma tesisi ana sunucusu gece 03:14'te sabote edildi.</p>
        <h3>ŞÜPHELİ TESPİT KILAVUZU (İPUÇLARI):</h3>
        <ul>
            <li><b>MASUM MÜHENDİS:</b> Çok korkmuştur. Baskı kurduğunda nabzı 110'un üzerine fırlar, sesi ve göz bebeği büyür.</li>
            <li><b>EĞİTİMLİ KÖSTEBEK (CASUS):</b> Özel eğitimlidir, nabzını hep düşük tutar! Ama <i>Mantık Tuzağı</i> kurarsan sesi %50'den fazla titrer ve göz bebeği büyür.</li>
            <li><b>SENTETİK ANDROİD:</b> Göz bebeği çapı (3.5 mm) ASLA değişmez ve sesi titremez. Sadece mantık sorusunda işlemcisi ısınır (nabzı 110+ fırlar).</li>
        </ul>
        <p style="color:#ffcc00; font-size:18px;">* Şüphelinin İlk Ölçülen Normal (Taban) Nabzı: <b>{taban_nabiz} BPM</b></p>
        <p style="color:#ffcc00; font-size:18px;">* Şüphelinin İlk Ölçülen Göz Bebeği Çapı: <b>{goz_bebegi} mm</b></p>
    </body>
    </html>
    """
    try:
        # Her bilgisayarda yazma izni olan güvenli Temp klasörünü kullanır
        gecici_klasor = tempfile.gettempdir()
        dosya_yolu = os.path.join(gecici_klasor, "gizli_kanit_raporu.html")
        with open(dosya_yolu, "w", encoding="utf-8") as dosya:
            dosya.write(html_icerik)
        
        # Türkçe karakter ve boşluk hatasını önleyen evrensel link çevirici
        web_linki = Path(dosya_yolu).as_uri()
        acildi_mi = webbrowser.open(web_linki)
        
        if not acildi_mi:
             yedek_rapor_penceresi_ac()
    except Exception:
        # Eğer bilgisayarda tarayıcı yoksa bile çökmez, oyun içi pencere açar!
        yedek_rapor_penceresi_ac()

def yedek_rapor_penceresi_ac():
    rapor_pen = tk.Toplevel(pencere)
    rapor_pen.title("Gizli Adli Tıp Raporu")
    rapor_pen.geometry("550x320")
    rapor_pen.configure(bg="#121212")
    metin = (
        "MERKEZ KOMUTANLIK - GİZLİ KANIT DOSYASI\n"
        "--------------------------------------------------\n\n"
        "1) MASUM MÜHENDİS:\n"
        "   Korkudan nabzı çok hızlı fırlar (110+ BPM), gözü ve sesi büyür.\n\n"
        "2) EĞİTİMLİ KÖSTEBEK:\n"
        "   Nabzını hep düşük tutar! Ama Mantık Tuzağında sesi %50 üstü titrer.\n\n"
        "3) SENTETİK ANDROİD:\n"
        "   Göz bebeği (3.5 mm) ve sesi HİÇ değişmez. Mantık sorusunda nabzı fırlar.\n\n"
        f"* Şüphelinin Taban Nabzı: {taban_nabiz} BPM | Göz Bebeği: {goz_bebegi} mm"
    )
    tk.Label(rapor_pen, text=metin, font=("Consolas", 10), bg="#121212", fg="#00ff9d", justify="left", padx=15, pady=15).pack()

# --- 3. SORU SORMA VE BİYOMETRİ HESAPLAMA FONKSİYONU ---
def hamle_yap(yaklasim):
    global tur, stres, anlik_nabiz, anlik_goz, ses_titremesi

    if oyun_bitti:
        messagebox.showinfo("Oyun Bitti", "Bu vaka kapandı! Yeni şüpheli almak için en alttaki 'Yeni Şüpheli Al' butonuna bas.")
        return

    if tur > 4:
        messagebox.showinfo("Sorgu Tamamlandı", "4 sorgu hakkın doldu! Artık aşağıdaki butonlardan teşhisini koymalısın.")
        return

    if yaklasim == "baski":
        stres += 25
    elif yaklasim == "empati":
        stres = max(10, stres - 10)
    elif yaklasim == "mantik":
        stres += 15

    if gizli_kimlik == 1: # Masum
        anlik_nabiz = taban_nabiz + int(stres * 0.8) + random.randint(0, 8)
        ses_titremesi = int(stres * 0.7)
        anlik_goz = round(goz_bebegi + (stres * 0.03), 1)
        cevap = "Şüpheli: 'Yemin ederim ben sadece alarmı kapatmaya çalışıyordum! Lütfen bana inanın!'"

    elif gizli_kimlik == 2: # Köstebek
        anlik_nabiz = taban_nabiz + random.randint(2, 10)
        if yaklasim == "mantik":
            ses_titremesi = random.randint(55, 80)
            anlik_goz = round(goz_bebegi + 1.4, 1)
            cevap = "Şüpheli: 'Şey... O kapının şifresi bende yoktu, sistem yanlış kaydetmiş olmalı...'"
        else:
            ses_titremesi = random.randint(8, 15)
            anlik_goz = round(goz_bebegi + 0.2, 1)
            cevap = "Şüpheli: 'Sakin olun memur bey, tüm ifadelerim prosedüre uygun.'"

    else: # Sentetik Android
        anlik_goz = goz_bebegi
        ses_titremesi = random.randint(0, 2)
        if yaklasim == "mantik":
            anlik_nabiz = taban_nabiz + random.randint(50, 70)
            cevap = "Şüpheli: 'Bu... Bu sorunun parametreleri hatalı. Ben... sıradan bir insanım.'"
        else:
            anlik_nabiz = taban_nabiz + random.randint(0, 4)
            cevap = "Şüpheli: 'Korkuyorum. Beni eve gönderin.' (Tamamen düz ve duygusuz bir sesle)"

    lbl_diyalog.config(text=f"[TUR {tur}/4] {cevap}", fg="#ffffff")
    biyometri_yazisini_guncelle()
    tur += 1

# --- 4. SUÇLUYU SEÇME (FİNAL) FONKSİYONU ---
def karar_ver(tahmin):
    global oyun_bitti
    if oyun_bitti:
        return

    oyun_bitti = True
    isimler = {1: "Masum Mühendis", 2: "Eğitimli Köstebek", 3: "Sentetik Android"}
    gercek = isimler[gizli_kimlik]

    if tahmin == gizli_kimlik:
        lbl_diyalog.config(
            text=f"TEBRİKLER DOĞRU TEŞHİS!\nKarşındaki kişi gerçekten '{gercek}' idi. Biyometrik verileri kusursuz analiz ettin!",
            fg="#a6e3a1"
        )
        messagebox.showinfo("BAŞARILI OPERASYON", f"Doğru Teşhis! Karşındaki kişi: {gercek}.")
    else:
        lbl_diyalog.config(
            text=f"YANLIŞ TEŞHİS!\nSen '{isimler[tahmin]}' dedin ama gerçek kimliği '{gercek}' idi!",
            fg="#f38ba8"
        )
        messagebox.showerror("OPERASYON BAŞARISIZ", f"Yanlış Teşhis!\nGerçek kimliği: {gercek} idi.")

# --- 5. CANLI GÖRSEL SİMÜLASYON EKRANI (DIŞ RESİM GEREKTİRMEZ!) ---
def canli_monitor_ciz():
    global ekg_sayac
    try:
        monitor.delete("all")
        ekg_sayac += 1

        # 1. SOL PANEL: Canlı EKG (Nabız) Grafiği
        monitor.create_text(110, 15, text=f"CANLI EKG ({anlik_nabiz} BPM)", fill="#00ff9d", font=("Consolas", 9, "bold"))
        monitor.create_rectangle(15, 30, 215, 115, outline="#00ff9d", fill="#090d16")
        
        noktalar = []
        frekans = max(2, int(130 / max(60, anlik_nabiz)))
        genlik = min(35, int((anlik_nabiz - 45) * 0.45))
        for x in range(20, 210, 5):
            if ((x // 5) + ekg_sayac) % frekans == 0:
                y = 72 - genlik
            elif ((x // 5) + ekg_sayac) % frekans == 1:
                y = 72 + int(genlik * 0.6)
            else:
                y = 72 + random.randint(-2, 2)
            noktalar.extend([x, y])
        if len(noktalar) >= 4:
            monitor.create_line(noktalar, fill="#00ff00", width=2)

        # 2. ORTA PANEL: Canlı Göz Bebeği (İris) Kamerası
        monitor.create_text(340, 15, text=f"OPTİK İRİS KAMERASI ({anlik_goz} mm)", fill="#89b4fa", font=("Consolas", 9, "bold"))
        monitor.create_rectangle(235, 30, 445, 115, outline="#89b4fa", fill="#090d16")
        # Göz akı ve İris
        monitor.create_oval(295, 42, 385, 102, fill="#d8e2dc", outline="#89b4fa", width=2)
        monitor.create_oval(315, 47, 365, 97, fill="#2b6cb0", outline="#1a365d", width=2)
        # Büyüyüp küçülen Göz Bebeği
        r = int(anlik_goz * 3.8)
        monitor.create_oval(340 - r, 72 - r, 340 + r, 72 + r, fill="black")
        monitor.create_oval(333, 62, 338, 67, fill="white", outline="") # Göz parlaması

        # 3. SAĞ PANEL: Ses Titreme Spektrumu
        monitor.create_text(555, 15, text=f"SES SPEKTRUMU (%{ses_titremesi})", fill="#f9e2af", font=("Consolas", 9, "bold"))
        monitor.create_rectangle(465, 30, 645, 115, outline="#f9e2af", fill="#090d16")
        for i in range(10):
            bar_x = 480 + (i * 15)
            max_yukseklik = max(4, int(ses_titremesi * 0.45))
            h = random.randint(2, max_yukseklik)
            renk = "#f38ba8" if ses_titremesi > 40 else "#f9e2af"
            monitor.create_rectangle(bar_x, 72 - h, bar_x + 8, 72 + h, fill=renk, outline="")

        pencere.after(150, canli_monitor_ciz)
    except tk.TclError:
        pass

# ==========================================================
# 6. FORM ARAYÜZÜ TASARIMI
# ==========================================================
pencere = tk.Tk()
pencere.title("PROTOKOL: ZİHİN AYNASI - Biyometrik Sorgu Simülasyonu")
pencere.geometry("700x640")
pencere.configure(bg="#1e1e2e")

tk.Label(pencere, text="BİYOMETRİK SORGU VE DAVRANIŞ ANALİZ SİSTEMİ", font=("Arial", 14, "bold"), bg="#1e1e2e", fg="#00ffcc").pack(pady=8)

btn_web = tk.Button(pencere, text="1. ADIM: Gizli Kanıt ve İpucu Dosyasını Web Sayfasında Aç", font=("Arial", 10, "bold"), bg="#ff9900", fg="black", command=web_kanit_ac, cursor="hand2")
btn_web.pack(pady=4, ipadx=10, ipady=4)

# Canlı Görsel Sensör Monitörü (Canvas)
monitor = tk.Canvas(pencere, width=660, height=125, bg="#11111b", highlightthickness=1, highlightbackground="#45475a")
monitor.pack(pady=6)

lbl_biyometri = tk.Label(pencere, text="", font=("Consolas", 10, "bold"), bg="#11111b", fg="#00ff00", pady=8, width=78)
lbl_biyometri.pack(pady=4)

lbl_diyalog = tk.Label(pencere, text="", font=("Arial", 11, "bold"), bg="#313244", fg="white", wraplength=620, height=4, width=70)
lbl_diyalog.pack(pady=8)

tk.Label(pencere, text="--- 2. ADIM: SORGULAMA YÖNTEMİNİ SEÇ (4 Hakkın Var) ---", bg="#1e1e2e", fg="#cdd6f4", font=("Arial", 10, "bold")).pack(pady=4)

cerceve_sorular = tk.Frame(pencere, bg="#1e1e2e")
cerceve_sorular.pack(pady=4)

tk.Button(cerceve_sorular, text="Baskı Kur (Suçla)", font=("Arial", 10, "bold"), bg="#f38ba8", width=20, command=lambda: hamle_yap("baski")).grid(row=0, column=0, padx=5, ipady=5)
tk.Button(cerceve_sorular, text="Empati Yap (Sakinleştir)", font=("Arial", 10, "bold"), bg="#a6e3a1", width=22, command=lambda: hamle_yap("empati")).grid(row=0, column=1, padx=5, ipady=5)
tk.Button(cerceve_sorular, text="Mantık Tuzağı Kur", font=("Arial", 10, "bold"), bg="#89b4fa", width=20, command=lambda: hamle_yap("mantik")).grid(row=0, column=2, padx=5, ipady=5)

tk.Label(pencere, text="--- 3. ADIM: NİHAİ TEŞHİSİNİ KOY ---", bg="#1e1e2e", fg="#f9e2af", font=("Arial", 10, "bold")).pack(pady=8)

cerceve_karar = tk.Frame(pencere, bg="#1e1e2e")
cerceve_karar.pack(pady=4)

tk.Button(cerceve_karar, text="Kararım: MASUM MÜHENDİS", bg="#45475a", fg="white", font=("Arial", 9, "bold"), width=22, command=lambda: karar_ver(1)).grid(row=0, column=0, padx=5, ipady=5)
tk.Button(cerceve_karar, text="Kararım: EĞİTİMLİ KÖSTEBEK", bg="#45475a", fg="white", font=("Arial", 9, "bold"), width=22, command=lambda: karar_ver(2)).grid(row=0, column=1, padx=5, ipady=5)
tk.Button(cerceve_karar, text="Kararım: SENTETİK ANDROİD", bg="#45475a", fg="white", font=("Arial", 9, "bold"), width=22, command=lambda: karar_ver(3)).grid(row=0, column=2, padx=5, ipady=5)

# Yeni Oyun Butonu (Ekranın kapanmasını önler)
tk.Button(pencere, text="Yeni Şüpheli Al (Sıfırla / Tekrar Oyna)", font=("Arial", 9, "bold"), bg="#cba6f7", fg="black", command=yeni_oyun_baslat).pack(pady=10, ipadx=10, ipady=3)

# Oyunu ve canlı grafikleri başlat
yeni_oyun_baslat()
canli_monitor_ciz()
pencere.mainloop()
