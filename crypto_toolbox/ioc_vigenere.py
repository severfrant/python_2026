import string
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


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
        self.root.title('Vigenère IOC visualizer')
        self.root.state('zoomed')

        self._build_ui()

        if initial_text:
            self.text_widget.delete('1.0', 'end')
            self.text_widget.insert('1.0', initial_text)
            self.compute_ioc()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(side='top', fill='both', expand=True)

        ttk.Label(frame, text='Ciphertext (only letters will be used):').pack(anchor='w')
        self.text_widget = scrolledtext.ScrolledText(frame, width=80, height=8)
        self.text_widget.pack(fill='x', pady=4)

        param_frame = ttk.Frame(frame)
        param_frame.pack(fill='x', pady=(4, 8))

        ttk.Label(param_frame, text='Max key length:').grid(row=0, column=0, sticky='w')
        self.maxkey_entry = ttk.Entry(param_frame, width=5)
        self.maxkey_entry.grid(row=0, column=1, padx=(4, 16))
        self.maxkey_entry.insert(0, '20')

        self.run_button = ttk.Button(param_frame, text='Compute IOC', command=self.compute_ioc)
        self.run_button.grid(row=0, column=2)

        ttk.Label(param_frame, text='Analyze columns for key len:').grid(row=1, column=0, sticky='w', pady=(8,0))
        self.column_keylen_entry = ttk.Entry(param_frame, width=5)
        self.column_keylen_entry.grid(row=1, column=1, padx=(4, 16), pady=(8,0))
        self.column_keylen_entry.insert(0, '3')

        self.column_button = ttk.Button(param_frame, text='Column freq', command=self.analyze_columns)
        self.column_button.grid(row=1, column=2, pady=(8,0))

        self.result_label = ttk.Label(frame, text='Enter ciphertext and press Compute IOC.')
        self.result_label.pack(anchor='w', pady=(0, 8))

        self.column_text = scrolledtext.ScrolledText(frame, width=80, height=8)
        self.column_text.pack(fill='x', pady=(0, 8))

        self.ioc_text = scrolledtext.ScrolledText(frame, width=80, height=10, wrap='none', font=('Consolas', 10))
        self.ioc_text.pack(fill='both', expand=True)
        self.ioc_text.config(state='disabled')

    def compute_ioc(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text or not any(ch.isalpha() for ch in text):
            messagebox.showwarning('No ciphertext', 'Please provide ciphertext containing letters.')
            return

        try:
            max_key = int(self.maxkey_entry.get())
        except ValueError:
            messagebox.showwarning('Invalid key length', 'Max key length must be an integer.')
            return

        if max_key < 1:
            messagebox.showwarning('Invalid key length', 'Max key length must be at least 1.')
            return

        ioc_values = []
        for key_len in range(1, max_key + 1):
            ioc_values.append(average_ioc_for_key_length(text, key_len))

        self.ioc_text.config(state='normal')
        self.ioc_text.delete('1.0', 'end')
        self.ioc_text.insert('1.0', 'Key length | Avg IOC\n')
        self.ioc_text.insert('end', '-----------+--------\n')
        for key_len, ioc in enumerate(ioc_values, start=1):
            self.ioc_text.insert('end', f'{key_len:>10} | {ioc:7.5f}\n')
        self.ioc_text.config(state='disabled')

        best_key = max(range(1, max_key + 1), key=lambda k: ioc_values[k - 1])
        best_ioc = ioc_values[best_key - 1]
        self.result_label.config(text=f'Best key length candidate: {best_key}, IOC={best_ioc:.5f}')

    def analyze_columns(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text or not any(ch.isalpha() for ch in text):
            messagebox.showwarning('Input required', 'Please enter ciphertext with letters.')
            return

        try:
            key_len = int(self.column_keylen_entry.get())
        except ValueError:
            messagebox.showwarning('Invalid key length', 'Key length must be an integer.')
            return

        if key_len < 1:
            messagebox.showwarning('Invalid key length', 'Key length must be >= 1.')
            return

        raw = ''.join(ch for ch in text.upper() if ch.isalpha())
        columns = [raw[i::key_len] for i in range(key_len)]

        self.column_text.delete('1.0', 'end')
        for idx, col in enumerate(columns, start=1):
            freq = Counter(col)
            tot = len(col)
            if tot == 0:
                self.column_text.insert('end', f'Column {idx}: empty\n')
                continue

            self.column_text.insert('end', f'Column {idx} length={tot}\n')
            for letter in string.ascii_uppercase:
                p = (freq[letter] / tot) * 100 if tot > 0 else 0.0
                self.column_text.insert('end', f'  {letter}: {p:5.2f}% ({freq[letter]})\n')
            self.column_text.insert('end', '\n')

        self.result_label.config(text=f'Column analysis completed for key length {key_len}.')


def main():
    root = tk.Tk()
    app = IOCVisualizerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
