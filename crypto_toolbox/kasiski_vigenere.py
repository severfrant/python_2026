import re
from collections import defaultdict, Counter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


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
        self.root.title('Kasiski Test Visualizer')
        self.root.state('zoomed')

        self._build_ui()

        if initial_text:
            self.text_widget.insert('1.0', initial_text)
            self.run_analysis()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text='Ciphertext for Kasiski analysis:').pack(anchor='w')
        self.text_widget = scrolledtext.ScrolledText(frame, width=80, height=8)
        self.text_widget.pack(fill='x', pady=4)

        param_frame = ttk.Frame(frame)
        param_frame.pack(fill='x', pady=(4, 8))

        ttk.Label(param_frame, text='Min repeat length:').grid(row=0, column=0, sticky='w')
        self.min_len_entry = ttk.Entry(param_frame, width=4)
        self.min_len_entry.grid(row=0, column=1, padx=(4, 12))
        self.min_len_entry.insert(0, '3')

        btn_run = ttk.Button(param_frame, text='Run Kasiski', command=self.run_analysis)
        btn_run.grid(row=0, column=2, padx=8)

        btn_show_graph = ttk.Button(param_frame, text='Show candidates', command=self.show_graph)
        btn_show_graph.grid(row=0, column=3, padx=8)

        ttk.Label(param_frame, text='Final key length:').grid(row=1, column=0, sticky='w')
        self.final_keylen_entry = ttk.Entry(param_frame, width=4)
        self.final_keylen_entry.grid(row=1, column=1, padx=(4, 12))
        self.final_keylen_entry.insert(0, '')

        self.result_label = ttk.Label(frame, text='Repeat distances and GCD candidates appear below')
        self.result_label.pack(anchor='w', pady=(0, 8))

        self.gcd_text = scrolledtext.ScrolledText(frame, width=80, height=16, wrap='none', font=('Consolas', 10))
        self.gcd_text.pack(fill='both', expand=True)
        self.gcd_text.config(state='disabled')

    def show_graph(self):
        if not hasattr(self, 'gcd_counts') or not self.gcd_counts:
            messagebox.showinfo('No data', 'Run Kasiski first to compute GCD candidates.')
            return

        gcd_counts = self.gcd_counts
        sorted_by_count = gcd_counts.most_common()
        top_n = min(20, len(sorted_by_count))
        top_candidates = sorted_by_count[:top_n]
        top_candidates = sorted(top_candidates, key=lambda item: item[0])

        self.gcd_text.config(state='normal')
        self.gcd_text.delete('1.0', 'end')
        self.gcd_text.insert('1.0', 'GCD candidate | Count\n')
        self.gcd_text.insert('end', '--------------+------\n')
        for gcd_value, count in top_candidates:
            self.gcd_text.insert('end', f'{gcd_value:>13} | {count}\n')

        if len(gcd_counts) > top_n:
            self.result_label.config(
                text=f'Top {top_n} GCD candidates shown. Full list is available in the results.')
        else:
            self.result_label.config(text='GCD candidate counts shown.')

        self.gcd_text.config(state='disabled')

    def run_analysis(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text or not any(ch.isalpha() for ch in text):
            messagebox.showwarning('Input required', 'Please enter ciphertext with letters.')
            return

        try:
            min_len = max(2, int(self.min_len_entry.get()))
        except ValueError:
            messagebox.showwarning('Invalid value', 'Min repeat length must be an integer.')
            return

        repeats = find_repeated_sequences(text, min_len=min_len)
        distances = compute_distances(repeats)
        self.gcd_counts = compute_gcds(distances)

        if self.gcd_counts:
            sorted_by_count = self.gcd_counts.most_common()
            candidates = ', '.join(f'{k}:{v}' for k, v in sorted(sorted_by_count, key=lambda item: item[0]))

            self.result_label.config(
                text=(f'Found {len(repeats)} repeated sequences, total distances {len(distances)}. '
                      f'GCD candidates (value:count): {candidates}. '
                      'Choose final key length and press Show graph when ready.')
            )
        else:
            self.result_label.config(text='No gcd candidates found. Try smaller min repeat length or longer text.')
            self.gcd_counts = Counter()

        self.gcd_text.config(state='normal')
        self.gcd_text.delete('1.0', 'end')
        self.gcd_text.insert('1.0', 'Run Show graph to list the top GCD candidates by frequency.\n')
        self.gcd_text.config(state='disabled')


def main():
    root = tk.Tk()
    app = KasiskiTestApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
