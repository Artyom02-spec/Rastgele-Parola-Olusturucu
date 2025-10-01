import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox

FIXED_LENGTH = 20

def build_charset(upper, lower, digits, symbols, exclude_ambiguous):
    charset = ""
    if lower:
        charset += string.ascii_lowercase
    if upper:
        charset += string.ascii_uppercase
    if digits:
        charset += string.digits
    if symbols:
        charset += "!@#$%^&*()-_=+[]{};:,.<>/?"
    if exclude_ambiguous:
        for ch in "Il1O0|`'\"~,;:. ":
            charset = charset.replace(ch, "")
    return charset

def generate_password(length, charset):
    if not charset:
        raise ValueError("Karakter secenekleri bos.")
    return ''.join(secrets.choice(charset) for _ in range(length))

def estimate_strength(pw):
    score = 0
    if any(c.islower() for c in pw): score += 1
    if any(c.isupper() for c in pw): score += 1
    if any(c.isdigit() for c in pw): score += 1
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>/?'\"" for c in pw): score += 1
    if len(pw) >= 16:
        score += 2
    elif len(pw) >= 12:
        score += 1
    if score >= 5:
        return "Çok güçlü"
    if score >= 4:
        return "Güçlü"
    if score >= 2:
        return "Zayif"
    return "Çok zayif"

class PasswordApp:
    def __init__(self, root):
        self.root = root
        root.title("Rastgele Parola Olusturucu")
        root.resizable(False, False)
        pad = 8

        frame = ttk.Frame(root, padding=pad)
        frame.grid(row=0, column=0, sticky="nsew")

        # Ayarlar Kısmı
        opts = ttk.Labelframe(frame, text="Ayarlar", padding=8)
        opts.grid(row=0, column=0, sticky="ew", padx=pad, pady=pad)

        # Uzunluk bilgisi
        ttk.Label(opts, text=f"Uzunluk: {FIXED_LENGTH} (fixed)").grid(row=0, column=0, sticky="w", columnspan=2, pady=(0,6))

        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digit_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.ambig_var = tk.BooleanVar(value=True)  # Karışık karakterleri çıkart

        ttk.Checkbutton(opts, text="Küçük harf", variable=self.lower_var).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(opts, text="Büyük harf", variable=self.upper_var).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(opts, text="Digitler", variable=self.digit_var).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(opts, text="Semboller", variable=self.symbol_var).grid(row=2, column=1, sticky="w")
        ttk.Checkbutton(opts, text="Karışık karakterleri çikart (Il1O0)", variable=self.ambig_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=(4,0))

        # Butonlar
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, sticky="ew", padx=pad)
        gen_btn = ttk.Button(btn_frame, text="Oluştur", command=self.on_generate)
        gen_btn.grid(row=0, column=0, sticky="w")
        copy_btn = ttk.Button(btn_frame, text="Kopyala", command=self.copy_selected)
        copy_btn.grid(row=0, column=1, sticky="w", padx=(8,0))

        # Çıktı
        out_frame = ttk.Labelframe(frame, text="Parola Oluşturuldu.", padding=8)
        out_frame.grid(row=2, column=0, sticky="nsew", padx=pad, pady=(0,pad))
        self.pw_var = tk.StringVar()
        self.pw_entry = ttk.Entry(out_frame, textvariable=self.pw_var, width=48, font=("Consolas", 10))
        self.pw_entry.grid(row=0, column=0, sticky="ew")
        self.pw_entry.bind("<Double-Button-1>", self.on_double_click)
        # Sağ tık menü
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Copy", command=self.copy_selected)
        self.menu.add_command(label="Clear", command=self.clear_password)
        self.pw_entry.bind("<Button-3>", self.show_menu)

        # Parola güçlülüğü ve bilgi 
        info_frame = ttk.Frame(frame)
        info_frame.grid(row=3, column=0, sticky="ew", padx=pad)
        self.str_var = tk.StringVar(value="Durum: -")
        ttk.Label(info_frame, textvariable=self.str_var).grid(row=0, column=0, sticky="w")
        ttk.Label(info_frame, text="|| Parolayi kopyalamak için çift tikla.").grid(row=0, column=1, sticky="e")

        # Tek parola
        self.generate_and_set()

    def generate_and_set(self):
        charset = build_charset(
            upper=self.upper_var.get(),
            lower=self.lower_var.get(),
            digits=self.digit_var.get(),
            symbols=self.symbol_var.get(),
            exclude_ambiguous=self.ambig_var.get()
        )
        if not charset:
            messagebox.showerror("Error", "Karakter seti boş, ayarlamalar yapin.")
            return
        pw = generate_password(FIXED_LENGTH, charset)
        self.pw_var.set(pw)
        self.str_var.set(f"Durum: {estimate_strength(pw)}")

    def on_generate(self):
        self.generate_and_set()

    def copy_selected(self):
        pw = self.pw_var.get()
        if not pw:
            messagebox.showinfo("Info", "Kopyalanacak parola bulunmuyor.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(pw)
        messagebox.showinfo("Copied", "Parola panoya kopyalandi.")

    def on_double_click(self, event):
        self.copy_selected()

    def clear_password(self):
        self.pw_var.set("")
        self.str_var.set("Durum: -")

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

def main():
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()