import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


from freq_analysis import FrequencyToolApp
from ioc_vigenere import IOCVisualizerApp
from kasiski_vigenere import KasiskiTestApp


class CryptoToolboxApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('SlopSolver')
        self.root.state('zoomed')

        frame = ttk.Frame(root, padding=16)
        frame.pack(fill='both', expand=True)

        title = ttk.Label(frame, text='Crypto Toolbox', font=('Segoe UI', 16, 'bold'))
        title.pack(pady=(0, 16))

        ttk.Label(frame, text='Shared ciphertext for tools:').pack(anchor='w')
        self.shared_text = scrolledtext.ScrolledText(frame, width=40, height=10)
        self.shared_text.pack(pady=(0, 12))

        btn_freq = ttk.Button(frame, text='Frequency Analysis', width=24, command=self.open_frequency_tool)
        btn_freq.pack(pady=4)

        btn_ioc = ttk.Button(frame, text='Vigenère IOC Visualizer', width=24, command=self.open_ioc_tool)
        btn_ioc.pack(pady=4)

        btn_kasiski = ttk.Button(frame, text='Kasiski Test Visualizer', width=24, command=self.open_kasiski_tool)
        btn_kasiski.pack(pady=4)

        future = ttk.Label(frame, text='Future tools: ???', foreground='gray')
        future.pack(pady=(18, 0))

        btn_quit = ttk.Button(frame, text='Quit', command=self.root.quit)
        btn_quit.pack(side='bottom', pady=(12, 0))

    def get_shared_ciphertext(self) -> str:
        return self.shared_text.get('1.0', 'end').strip()

    def open_frequency_tool(self):
        win = tk.Toplevel(self.root)
        win.state('zoomed')
        injected = self.get_shared_ciphertext()
        app = FrequencyToolApp(win, initial_text=injected)

    def open_ioc_tool(self):
        win = tk.Toplevel(self.root)
        win.state('zoomed')
        injected = self.get_shared_ciphertext()
        IOCVisualizerApp(win, initial_text=injected)

    def open_kasiski_tool(self):
        win = tk.Toplevel(self.root)
        win.state('zoomed')
        injected = self.get_shared_ciphertext()
        KasiskiTestApp(win, initial_text=injected)


def main():
    root = tk.Tk()
    app = CryptoToolboxApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
