import re
from collections import defaultdict, Counter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def find_repeated_sequences(text: str, min_len: int = 3):
    text = re.sub('[^A-Za-z]', '', text).upper()
    seq_positions = defaultdict(list)

    for start in range(len(text) - min_len + 1):
        for size in range(min_len, min(len(text) - start, 10) + 1):
            seq = text[start:start + size]
            seq_positions[seq].append(start)

    repeats = {seq: pos for seq, pos in seq_positions.items() if len(pos) > 1}
    return repeats


def compute_distances(repeats: dict[str, list[int]]) -> list[int]:
    dists = []
    for positions in repeats.values():
        for i in range(1, len(positions)):
            dists.append(positions[i] - positions[i - 1])
    return dists


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def compute_gcds(distances: list[int]) -> Counter:
    gcd_counts = Counter()
    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            g = gcd(distances[i], distances[j])
            if g > 1:
                gcd_counts[g] += 1
    return gcd_counts


class KasiskiTestApp:
    def __init__(self, root: tk.Tk | tk.Toplevel, initial_text: str = ''):
        self.root = root
        self.root.title('Kasiskiho test')
        self.root.state('zoomed')

        self._build_ui()

        if initial_text:
            self.text_widget.insert('1.0', initial_text)
            self.run_analysis()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text='Šifrovaný text pro Kasiskiho analýzu:').pack(anchor='w')
        self.text_widget = scrolledtext.ScrolledText(frame, width=80, height=8)
        self.text_widget.pack(fill='x', pady=4)

        param_frame = ttk.Frame(frame)
        param_frame.pack(fill='x', pady=(4, 8))

        ttk.Label(param_frame, text='Minimální délka opakování:').grid(row=0, column=0, sticky='w')
        self.min_len_entry = ttk.Entry(param_frame, width=4)
        self.min_len_entry.grid(row=0, column=1, padx=(4, 12))
        self.min_len_entry.insert(0, '3')

        btn_run = ttk.Button(param_frame, text='Spustit Kasiskiho test', command=self.run_analysis)
        btn_run.grid(row=0, column=2, padx=8)

        btn_show_graph = ttk.Button(param_frame, text='Zobrazit kandidáty', command=self.show_graph)
        btn_show_graph.grid(row=0, column=3, padx=8)

        ttk.Label(param_frame, text='Zvolená délka klíče:').grid(row=1, column=0, sticky='w')
        self.final_keylen_entry = ttk.Entry(param_frame, width=4)
        self.final_keylen_entry.grid(row=1, column=1, padx=(4, 12))
        self.final_keylen_entry.insert(0, '')

        self.result_label = ttk.Label(frame, text='Vzdálenosti opakování a kandidáti společného dělitele se zobrazí níže.')
        self.result_label.pack(anchor='w', pady=(0, 8))

        chart_frame = ttk.Frame(frame)
        chart_frame.pack(fill='both', expand=True)
        self.figure, self.ax = plt.subplots(figsize=(9, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self._draw_candidates_chart([])

    def close(self):
        plt.close(self.figure)
        self.root.destroy()

    def _draw_candidates_chart(self, candidates: list[tuple[int, int]]):
        self.ax.clear()
        positions = list(range(len(candidates)))
        if candidates:
            values = [value for value, _ in candidates]
            counts = [count for _, count in candidates]
            self.ax.bar(positions, counts, color='#B45309', alpha=0.82)
            self.ax.set_xticks(positions, [str(value) for value in values], rotation=45, ha='right')
            self.ax.set_xlim(-0.5, len(positions) - 0.5)
        self.ax.set_title('Četnost kandidátů délky klíče')
        self.ax.set_xlabel('Kandidát délky klíče (NSD)')
        self.ax.set_ylabel('Počet výskytů')
        self.ax.grid(axis='y', alpha=0.25)
        self.figure.tight_layout()
        self.canvas.draw()

    def show_graph(self):
        if not hasattr(self, 'gcd_counts') or not self.gcd_counts:
            messagebox.showinfo('Chybí data', 'Nejprve spusťte Kasiskiho test, aby se vypočítali kandidáti.')
            return

        gcd_counts = self.gcd_counts
        sorted_by_count = gcd_counts.most_common()
        top_n = min(20, len(sorted_by_count))
        top_candidates = sorted_by_count[:top_n]
        top_candidates = sorted(top_candidates, key=lambda item: item[0])

        self._draw_candidates_chart(top_candidates)

        if len(gcd_counts) > top_n:
            self.result_label.config(
                text=f'Zobrazeno {top_n} nejsilnějších kandidátů. Úplný seznam je ve výsledku testu.')
        else:
            self.result_label.config(text='Zobrazeny počty kandidátů společného dělitele.')


    def run_analysis(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text or not any(ch.isalpha() for ch in text):
            messagebox.showwarning('Je potřeba vstup', 'Zadejte šifrovaný text obsahující písmena.')
            return

        try:
            min_len = max(2, int(self.min_len_entry.get()))
        except ValueError:
            messagebox.showwarning('Neplatná hodnota', 'Minimální délka opakování musí být celé číslo.')
            return

        repeats = find_repeated_sequences(text, min_len=min_len)
        distances = compute_distances(repeats)
        self.gcd_counts = compute_gcds(distances)

        if self.gcd_counts:
            sorted_by_count = self.gcd_counts.most_common()
            candidates = ', '.join(f'{k}:{v}' for k, v in sorted(sorted_by_count, key=lambda item: item[0]))

            self.result_label.config(
                    text=(f'Nalezeno opakovaných posloupností: {len(repeats)}, vzdáleností celkem: {len(distances)}. '
                        f'Kandidáti NSD (hodnota:počet): {candidates}. '
                        'Poté zvolte kandidáty pro přehled jejich četnosti.')
            )
        else:
            self.result_label.config(text='Nebyl nalezen žádný kandidát NSD. Zkuste kratší opakování nebo delší text.')
            self.gcd_counts = Counter()

        self._draw_candidates_chart([])


def main():
    root = tk.Tk()
    app = KasiskiTestApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
