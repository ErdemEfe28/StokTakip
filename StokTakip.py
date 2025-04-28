import tkinter as tk
from tkinter import messagebox

class Urun:
    def __init__(self, ad, stok):
        self.ad = ad
        self.stok = stok

    def stok_guncelle(self, miktar):
        self.stok += miktar

class Siparis:
    siparis_no_counter = 1

    def __init__(self, urun, miktar):
        self.siparis_no = Siparis.siparis_no_counter
        Siparis.siparis_no_counter += 1
        self.urun = urun
        self.miktar = miktar

class StokTakip:
    def __init__(self):
        self.urunler = []
        self.siparisler = []

    def urun_ekle(self, urun):
        self.urunler.append(urun)

    def urun_guncelle(self, urun_adi, yeni_stok):
        for urun in self.urunler:
            if urun.ad == urun_adi:
                urun.stok = yeni_stok
                return urun
        return None

    def siparis_olustur(self, urun_adi, miktar):
        for urun in self.urunler:
            if urun.ad == urun_adi:
                if urun.stok >= miktar:
                    urun.stok_guncelle(-miktar)
                    yeni_siparis = Siparis(urun, miktar)
                    self.siparisler.append(yeni_siparis)
                    return yeni_siparis
                else:
                    return None
        return None

class StokTakipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stok Takip Sistemi")
        self.stok_takip = StokTakip()

        tk.Label(root, text="Ürün Adı:").grid(row=0, column=0)
        self.entry_urun_adi = tk.Entry(root)
        self.entry_urun_adi.grid(row=0, column=1)

        tk.Label(root, text="Stok Miktarı:").grid(row=1, column=0)
        self.entry_stok_miktari = tk.Entry(root)
        self.entry_stok_miktari.grid(row=1, column=1)

        self.btn_urun_ekle = tk.Button(root, text="Ürün Ekle", command=self.urun_ekle)
        self.btn_urun_ekle.grid(row=2, column=0, columnspan=2)

        tk.Label(root, text="Ürünler:").grid(row=3, column=0)
        self.lst_urunler = tk.Listbox(root, width=50)
        self.lst_urunler.grid(row=3, column=1)

        tk.Label(root, text="Sipariş Miktarı:").grid(row=4, column=0)
        self.entry_siparis_miktari = tk.Entry(root)
        self.entry_siparis_miktari.grid(row=4, column=1)

        self.btn_siparis_ver = tk.Button(root, text="Sipariş Ver", command=self.siparis_ver)
        self.btn_siparis_ver.grid(row=5, column=0, columnspan=2)

        tk.Label(root, text="Siparişler:").grid(row=6, column=0)
        self.lst_siparisler = tk.Listbox(root, width=50)
        self.lst_siparisler.grid(row=6, column=1)

        # Stok Güncelleme Alanı
        tk.Label(root, text="Yeni Stok Miktarı:").grid(row=7, column=0)
        self.entry_yeni_stok_miktari = tk.Entry(root)
        self.entry_yeni_stok_miktari.grid(row=7, column=1)

        self.btn_stok_guncelle = tk.Button(root, text="Stok Güncelle", command=self.stok_guncelle)
        self.btn_stok_guncelle.grid(row=8, column=0, columnspan=2)

    def urun_ekle(self):
        ad = self.entry_urun_adi.get()
        try:
            stok = int(self.entry_stok_miktari.get())
            if ad and stok >= 0:
                yeni_urun = Urun(ad, stok)
                self.stok_takip.urun_ekle(yeni_urun)
                self.guncelle_urun_listesi()
                messagebox.showinfo("Başarılı", "Ürün eklendi!")
                self.entry_urun_adi.delete(0, tk.END)
                self.entry_stok_miktari.delete(0, tk.END)
            else:
                messagebox.showerror("Hata", "Tüm alanları doğru doldurun!")
        except ValueError:
            messagebox.showerror("Hata", "Stok miktarı sayı olmalıdır!")

    def siparis_ver(self):
        secili = self.lst_urunler.curselection()
        if secili:
            urun_ad = self.lst_urunler.get(secili[0]).split(" - ")[0]
            try:
                miktar = int(self.entry_siparis_miktari.get())
                if miktar > 0:
                    siparis = self.stok_takip.siparis_olustur(urun_ad, miktar)
                    if siparis:
                        self.guncelle_urun_listesi()
                        self.guncelle_siparis_listesi()
                        messagebox.showinfo("Başarılı", f"Sipariş Oluşturuldu! Sipariş No: {siparis.siparis_no}")
                        self.entry_siparis_miktari.delete(0, tk.END)
                    else:
                        messagebox.showerror("Hata", "Yetersiz stok!")
                else:
                    messagebox.showerror("Hata", "Miktar pozitif olmalı!")
            except ValueError:
                messagebox.showerror("Hata", "Miktar sayı olmalıdır!")
        else:
            messagebox.showerror("Hata", "Lütfen bir ürün seçin!")

    def stok_guncelle(self):
        secili = self.lst_urunler.curselection()
        if secili:
            urun_ad = self.lst_urunler.get(secili[0]).split(" - ")[0]
            try:
                yeni_stok = int(self.entry_yeni_stok_miktari.get())
                if yeni_stok >= 0:
                    urun = self.stok_takip.urun_guncelle(urun_ad, yeni_stok)
                    if urun:
                        self.guncelle_urun_listesi()
                        messagebox.showinfo("Başarılı", f"Stok güncellendi! Yeni Stok: {yeni_stok}")
                        self.entry_yeni_stok_miktari.delete(0, tk.END)
                    else:
                        messagebox.showerror("Hata", "Ürün bulunamadı!")
                else:
                    messagebox.showerror("Hata", "Yeni stok miktarı negatif olamaz!")
            except ValueError:
                messagebox.showerror("Hata", "Stok miktarı sayı olmalıdır!")
        else:
            messagebox.showerror("Hata", "Lütfen bir ürün seçin!")

    def guncelle_urun_listesi(self):
        self.lst_urunler.delete(0, tk.END)
        for urun in self.stok_takip.urunler:
            self.lst_urunler.insert(tk.END, f"{urun.ad} - Stok: {urun.stok}")

    def guncelle_siparis_listesi(self):
        self.lst_siparisler.delete(0, tk.END)
        for siparis in self.stok_takip.siparisler:
            self.lst_siparisler.insert(tk.END, f"No: {siparis.siparis_no} | Ürün: {siparis.urun.ad} | Miktar: {siparis.miktar}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StokTakipApp(root)
    root.mainloop()
