import string
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def index_of_coincidence(segment: str) -> float:
    segment = ''.join(ch for ch in segment.upper() if ch.isalpha())
    n = len(segment)
    if n <= 1:
        return 0.0
    frequencies = Counter(segment)
    total_pairs = sum(v * (v - 1) for v in frequencies.values())
    return total_pairs / (n * (n - 1))


def average_ioc_for_key_length(text: str, key_len: int) -> float:
    text = ''.join(ch for ch in text.upper() if ch.isalpha())
    if key_len <= 0:
        return 0.0
    iocs = []
    for i in range(key_len):
        segment = text[i::key_len]
        iocs.append(index_of_coincidence(segment))
    if not iocs:
        return 0.0
    return sum(iocs) / len(iocs)


class IOCVisualizerApp:
    def __init__(self, root: tk.Tk | tk.Toplevel, initial_text: str = ''):
        self.root = root
        self.root.title('Index koincidence')
        self.root.state('zoomed')

        self._build_ui()

        if initial_text:
            self.text_widget.delete('1.0', 'end')
            self.text_widget.insert('1.0', initial_text)
            self.compute_ioc()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(side='top', fill='both', expand=True)

        ttk.Label(frame, text='Šifrovaný text (použijí se pouze písmena):').pack(anchor='w')
        self.text_widget = scrolledtext.ScrolledText(frame, width=80, height=8)
        self.text_widget.pack(fill='x', pady=4)

        param_frame = ttk.Frame(frame)
        param_frame.pack(fill='x', pady=(4, 8))

        ttk.Label(param_frame, text='Maximální délka klíče:').grid(row=0, column=0, sticky='w')
        self.maxkey_entry = ttk.Entry(param_frame, width=5)
        self.maxkey_entry.grid(row=0, column=1, padx=(4, 16))
        self.maxkey_entry.insert(0, '20')

        self.run_button = ttk.Button(param_frame, text='Vypočítat IOC', command=self.compute_ioc)
        self.run_button.grid(row=0, column=2)

        ttk.Label(param_frame, text='Analyzovat sloupce pro délku klíče:').grid(row=1, column=0, sticky='w', pady=(8,0))
        self.column_keylen_entry = ttk.Entry(param_frame, width=5)
        self.column_keylen_entry.grid(row=1, column=1, padx=(4, 16), pady=(8,0))
        self.column_keylen_entry.insert(0, '3')

        self.column_button = ttk.Button(param_frame, text='Četnost ve sloupcích', command=self.analyze_columns)
        self.column_button.grid(row=1, column=2, pady=(8,0))

        self.result_label = ttk.Label(frame, text='Vložte šifrovaný text a zvolte Vypočítat IOC.')
        self.result_label.pack(anchor='w', pady=(0, 8))

        self.column_text = scrolledtext.ScrolledText(frame, width=80, height=8)
        self.column_text.pack(fill='x', pady=(0, 8))

        chart_frame = ttk.Frame(frame)
        chart_frame.pack(fill='both', expand=True)
        self.figure, self.ax = plt.subplots(figsize=(9, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self._draw_ioc_chart([])

    def _draw_ioc_chart(self, ioc_values: list[float]):
        self.ax.clear()
        positions = list(range(1, len(ioc_values) + 1))
        if positions:
            self.ax.bar(positions, ioc_values, color='#2563EB', alpha=0.82, label='Vypočtené IOC')
            self.ax.set_xticks(positions)
        self.ax.axhline(0.065, color='#15803D', linestyle='--', linewidth=1.5, label='Angličtina přibližně 0,065')
        self.ax.axhline(0.0385, color='#B91C1C', linestyle='--', linewidth=1.5, label='Náhodný text přibližně 0,0385')
        self.ax.set_title('Index koincidence podle délky klíče')
        self.ax.set_xlabel('Délka klíče')
        self.ax.set_ylabel('Průměrné IOC')
        self.ax.set_ylim(0, max(0.08, max(ioc_values, default=0) * 1.1, 0.065))
        self.ax.grid(axis='y', alpha=0.25)
        self.ax.legend(loc='upper right')
        self.figure.tight_layout()
        self.canvas.draw()

    def compute_ioc(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text or not any(ch.isalpha() for ch in text):
            messagebox.showwarning('Chybí šifrovaný text', 'Zadejte šifrovaný text obsahující písmena.')
            return

        try:
            max_key = int(self.maxkey_entry.get())
        except ValueError:
            messagebox.showwarning('Neplatná délka klíče', 'Maximální délka klíče musí být celé číslo.')
            return

        if max_key < 1:
            messagebox.showwarning('Neplatná délka klíče', 'Maximální délka klíče musí být alespoň 1.')
            return

        ioc_values = []
        for key_len in range(1, max_key + 1):
            ioc_values.append(average_ioc_for_key_length(text, key_len))

        self._draw_ioc_chart(ioc_values)

        best_key = max(range(1, max_key + 1), key=lambda k: ioc_values[k - 1])
        best_ioc = ioc_values[best_key - 1]
        self.result_label.config(text=f'Nejsilnější kandidát délky klíče: {best_key}, IOC = {best_ioc:.5f}')

    def analyze_columns(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text or not any(ch.isalpha() for ch in text):
            messagebox.showwarning('Je potřeba vstup', 'Zadejte šifrovaný text obsahující písmena.')
            return

        try:
            key_len = int(self.column_keylen_entry.get())
        except ValueError:
            messagebox.showwarning('Neplatná délka klíče', 'Délka klíče musí být celé číslo.')
            return

        if key_len < 1:
            messagebox.showwarning('Neplatná délka klíče', 'Délka klíče musí být alespoň 1.')
            return

        raw = ''.join(ch for ch in text.upper() if ch.isalpha())
        columns = [raw[i::key_len] for i in range(key_len)]

        self.column_text.delete('1.0', 'end')
        for idx, col in enumerate(columns, start=1):
            freq = Counter(col)
            tot = len(col)
            if tot == 0:
                self.column_text.insert('end', f'Sloupec {idx}: prázdný\n')
                continue

            self.column_text.insert('end', f'Sloupec {idx}, délka = {tot}\n')
            for letter in string.ascii_uppercase:
                p = (freq[letter] / tot) * 100 if tot > 0 else 0.0
                self.column_text.insert('end', f'  {letter}: {p:5.2f}% ({freq[letter]})\n')
            self.column_text.insert('end', '\n')

        self.result_label.config(text=f'Analýza sloupců dokončena pro délku klíče {key_len}.')


def main():
    root = tk.Tk()
    app = IOCVisualizerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
