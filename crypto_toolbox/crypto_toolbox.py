import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import matplotlib.pyplot as plt

from freq_analysis import FrequencyToolApp
from ioc_vigenere import IOCVisualizerApp
from kasiski_vigenere import KasiskiTestApp


def configure_school_theme(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('TFrame', background='#F5F7F2')
    style.configure('TLabel', background='#F5F7F2', foreground='#1E2930', font=('Segoe UI', 11))
    style.configure('Title.TLabel', font=('Segoe UI', 22, 'bold'), foreground='#164E63')
    style.configure('Subtitle.TLabel', foreground='#475569')
    style.configure('Tool.Frequency.TButton', font=('Segoe UI', 12, 'bold'), background='#0F766E', foreground='#FFFFFF', padding=(18, 12))
    style.map('Tool.Frequency.TButton', background=[('active', '#115E59')])
    style.configure('Tool.IOC.TButton', font=('Segoe UI', 12, 'bold'), background='#2563EB', foreground='#FFFFFF', padding=(18, 12))
    style.map('Tool.IOC.TButton', background=[('active', '#1D4ED8')])
    style.configure('Tool.Kasiski.TButton', font=('Segoe UI', 12, 'bold'), background='#B45309', foreground='#FFFFFF', padding=(18, 12))
    style.map('Tool.Kasiski.TButton', background=[('active', '#92400E')])
    style.configure('Action.TButton', font=('Segoe UI', 10, 'bold'), background='#0F766E', foreground='#FFFFFF', padding=(10, 6))
    style.map('Action.TButton', background=[('active', '#115E59')])
    style.configure('Shift.TButton', font=('Segoe UI', 10, 'bold'), background='#2563EB', foreground='#FFFFFF', padding=(10, 6))
    style.map('Shift.TButton', background=[('active', '#1D4ED8')])
    style.configure('Solve.TButton', font=('Segoe UI', 10, 'bold'), background='#B45309', foreground='#FFFFFF', padding=(10, 6))
    style.map('Solve.TButton', background=[('active', '#92400E')])
    style.configure('Reset.TButton', font=('Segoe UI', 10), background='#64748B', foreground='#FFFFFF', padding=(10, 6))
    style.map('Reset.TButton', background=[('active', '#475569')])


class CryptoToolboxApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Kryptografická laboratoř')
        self.root.state('zoomed')
        configure_school_theme(root)
        self.root.protocol('WM_DELETE_WINDOW', self.close_application)
        self.is_closing = False

        frame = ttk.Frame(root, padding=(36, 28))
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text='Kryptografická laboratoř', style='Title.TLabel').pack(anchor='w')
        ttk.Label(
            frame,
            text='Prozkoumejte šifrovaný text pomocí frekvenční analýzy, indexu koincidence a Kasiskiho testu.',
            style='Subtitle.TLabel',
        ).pack(anchor='w', pady=(4, 24))

        ttk.Label(frame, text='Šifrovaný text pro analýzu:').pack(anchor='w')
        self.shared_text = scrolledtext.ScrolledText(frame, width=72, height=10, font=('Segoe UI', 11))
        self.shared_text.pack(fill='x', pady=(6, 20))

        ttk.Label(frame, text='Vyberte metodu:').pack(anchor='w', pady=(0, 8))
        btn_freq = ttk.Button(frame, text='Frekvenční analýza', width=30, style='Tool.Frequency.TButton', command=self.open_frequency_tool)
        btn_freq.pack(anchor='w', pady=4)

        btn_ioc = ttk.Button(frame, text='Index koincidence', width=30, style='Tool.IOC.TButton', command=self.open_ioc_tool)
        btn_ioc.pack(anchor='w', pady=4)

        btn_kasiski = ttk.Button(frame, text='Kasiskiho test', width=30, style='Tool.Kasiski.TButton', command=self.open_kasiski_tool)
        btn_kasiski.pack(anchor='w', pady=4)

        ttk.Label(
            frame,
            text='Text zůstane při otevření vybraného nástroje k dispozici.',
            style='Subtitle.TLabel',
        ).pack(anchor='w', pady=(16, 0))

        btn_quit = ttk.Button(frame, text='Ukončit', command=self.close_application)
        btn_quit.pack(anchor='w', pady=(22, 0))

    def get_shared_ciphertext(self) -> str:
        return self.shared_text.get('1.0', 'end').strip()

    def close_application(self):
        if self.is_closing:
            return

        self.is_closing = True
        plt.close('all')
        self.root.quit()
        self.root.destroy()

    def open_frequency_tool(self):
        win = tk.Toplevel(self.root)
        win.state('zoomed')
        injected = self.get_shared_ciphertext()
        app = FrequencyToolApp(win, initial_text=injected)
        win.protocol('WM_DELETE_WINDOW', app.close)

    def open_ioc_tool(self):
        win = tk.Toplevel(self.root)
        win.state('zoomed')
        injected = self.get_shared_ciphertext()
        app = IOCVisualizerApp(win, initial_text=injected)
        win.protocol('WM_DELETE_WINDOW', app.close)

    def open_kasiski_tool(self):
        win = tk.Toplevel(self.root)
        win.state('zoomed')
        injected = self.get_shared_ciphertext()
        app = KasiskiTestApp(win, initial_text=injected)
        win.protocol('WM_DELETE_WINDOW', app.close)


def main():
    root = tk.Tk()
    app = CryptoToolboxApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
