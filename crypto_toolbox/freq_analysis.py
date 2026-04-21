import string
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# English letter frequency (approximate, as percent)
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974, 'Z': 0.074,
}

LETTERS = list(string.ascii_uppercase)


def caesar_shift_text(text: str, shift: int) -> str:
    shifted_chars = []
    shift = shift % 26
    for ch in text:
        if 'A' <= ch <= 'Z':
            shifted_chars.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        elif 'a' <= ch <= 'z':
            shifted_chars.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        else:
            shifted_chars.append(ch)
    return ''.join(shifted_chars)


def compute_frequency(text: str) -> list[float]:
    text = text.upper()
    letters = [ch for ch in text if ch.isalpha()]
    total = len(letters)
    if total == 0:
        return [0.0] * 26
    counter = Counter(letters)
    return [(counter[l] / total) * 100.0 for l in LETTERS]


class BaseFrequencyAnalysisApp:
    def __init__(self, root: tk.Tk | tk.Toplevel, title: str, back_callback):
        self.root = root
        self.root.title(title)
        self.back_callback = back_callback

        self.base_text = ''
        self.original_text = ''
        self.current_text_view = ''
        self.current_shift = 0
        self.undo_stack = []

        self._build_shared_ui()
        self._build_mode_ui()
        self._init_plot()

    def _build_shared_ui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side='top', fill='x', padx=8, pady=8)

        label = ttk.Label(top_frame, text='Enter cipher text:')
        label.grid(row=0, column=0, sticky='w')

        self.text_widget = scrolledtext.ScrolledText(top_frame, width=70, height=10)
        self.text_widget.grid(row=1, column=0, columnspan=6, padx=0, pady=6)

        btn_analyze = ttk.Button(top_frame, text='Analyze', command=self.analyze)
        btn_analyze.grid(row=2, column=0, pady=4)

        btn_left = ttk.Button(top_frame, text='Shift ⬅', command=lambda: self.shift_text(-1))
        btn_left.grid(row=2, column=1, pady=4, padx=(10, 0))

        btn_right = ttk.Button(top_frame, text='Shift ➡', command=lambda: self.shift_text(1))
        btn_right.grid(row=2, column=2, pady=4, padx=(8, 0))

        btn_reset = ttk.Button(top_frame, text='Reset', command=self.reset_text)
        btn_reset.grid(row=2, column=3, pady=4, padx=(8, 0))

        btn_undo = ttk.Button(top_frame, text='Undo', command=self.undo)
        btn_undo.grid(row=2, column=4, pady=4, padx=(8, 0))

        self.current_shift_label = ttk.Label(top_frame, text='Current shift: 0')
        self.current_shift_label.grid(row=2, column=5, padx=(8, 0))

        btn_back = ttk.Button(top_frame, text='Back', command=self.back)
        btn_back.grid(row=3, column=0, pady=4, sticky='w')

        ttk.Label(top_frame, text='Solve shift:').grid(row=4, column=0, sticky='e')
        self.solve_shift_var = tk.StringVar(value='0')
        self.solve_entry = ttk.Entry(top_frame, width=5, textvariable=self.solve_shift_var)
        self.solve_entry.grid(row=4, column=1, sticky='w', padx=(10, 0))

        self.validation_label = ttk.Label(top_frame, text='', foreground='red')
        self.validation_label.grid(row=4, column=2, columnspan=4, sticky='w', padx=(8, 0))

        self.mode_controls_row = 6
        self.top_frame = top_frame

    def _build_mode_ui(self):
        raise NotImplementedError('Subclass must implement mode UI')

    def _init_plot(self):
        chart_frame = ttk.Frame(self.root)
        chart_frame.pack(side='top', fill='both', expand=True, padx=8, pady=8)

        self.freq_text = scrolledtext.ScrolledText(chart_frame, width=70, height=16, font=('Consolas', 10), wrap='none')
        self.freq_text.pack(fill='both', expand=True)
        self.freq_text.config(state='disabled')
        self._draw_frequency_from_text('')

        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side='bottom', fill='x', padx=8, pady=6)

        self.info_label = ttk.Label(bottom_frame, text='Type or paste text, then click Analyze.')
        self.info_label.pack(side='left')

    def back(self):
        self.back_callback()

    def analyze(self):
        raise NotImplementedError('Subclasses must implement analyze()')

    def shift_text(self, delta: int):
        raise NotImplementedError('Subclasses must implement shift_text()')

    def reset_text(self):
        raise NotImplementedError('Subclasses must implement reset_text()')

    def _save_undo_state(self, extra=None):
        state = {
            'base_text': self.base_text,
            'current_text_view': self.current_text_view,
            'current_shift': self.current_shift,
        }
        if extra:
            state.update(extra)
        self.undo_stack.append(state)
        if len(self.undo_stack) > 3:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            messagebox.showinfo('Undo', 'No changes to undo.')
            return

        state = self.undo_stack.pop()
        self.base_text = state.get('base_text', '')
        self.current_text_view = state.get('current_text_view', '')
        self.current_shift = state.get('current_shift', 0)

        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', self.base_text)
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self._draw_frequency_from_text(self.current_text_view or self.base_text)
        self.info_label.config(text='Undid last action.')

    def validate_shift(self) -> int | None:
        raw = self.solve_shift_var.get().strip()
        if not raw.isdigit():
            self.validation_label.config(text='Invalid shift: please enter integer 0-25.')
            return None
        self.validation_label.config(text='')
        return int(raw) % 26

    def update_current_shift(self, delta: int):
        self.current_shift = (self.current_shift + delta) % 26
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')

    def _draw_frequency(self, freq_values: list[float]):
        eng_values = [ENGLISH_FREQ[l] for l in LETTERS]
        lines = [
            'Letter | Cipher % | English % | Cipher bar                    | English bar',
            '-------+----------+-----------+-------------------------------+----------------',
        ]

        for letter, freq, eng in zip(LETTERS, freq_values, eng_values):
            cipher_bar = '█' * min(int(freq / 15 * 20), 20) if freq > 0 else ''
            english_bar = '░' * min(int(eng / 15 * 20), 20) if eng > 0 else ''
            lines.append(
                f'{letter:>6} | {freq:7.2f} | {eng:9.2f} | {cipher_bar:<31} | {english_bar}'
            )

        self.freq_text.config(state='normal')
        self.freq_text.delete('1.0', 'end')
        self.freq_text.insert('1.0', '\n'.join(lines))
        self.freq_text.config(state='disabled')

    def _draw_frequency_from_base(self, shift: int):
        base_freq = compute_frequency(self.base_text)
        rotated = [base_freq[(i - shift) % 26] for i in range(26)]
        self._draw_frequency(rotated)

    def _draw_frequency_from_text(self, text: str):
        freq = compute_frequency(text)
        self._draw_frequency(freq)

    def show_mapping(self):
        if not self.base_text:
            messagebox.showinfo('No data', 'Analyze text first to see mapping.')
            return

        shift = self.validate_shift()
        if shift is None:
            shift = 0

        mapping_text = '\n'.join(
            f'{plain} -> {LETTERS[(i + shift) % 26]}'
            for i, plain in enumerate(LETTERS)
        )

        win = tk.Toplevel(self.root)
        win.title(f'Letter mapping for shift {shift}')
        ttk.Label(win, text=f'Mapping for shift {shift}:', font=('Segoe UI', 10, 'bold')).pack(padx=12, pady=8)

        txt = scrolledtext.ScrolledText(win, width=24, height=14, wrap='none', font=('Consolas', 10))
        txt.pack(padx=12, pady=(0, 8))
        txt.insert('1.0', mapping_text)
        txt.config(state='disabled')

        ttk.Button(win, text='Close', command=win.destroy).pack(pady=(0, 12))


class CaesarFrequencyAnalysisApp(BaseFrequencyAnalysisApp):
    def __init__(self, root: tk.Tk | tk.Toplevel, back_callback, initial_text: str = ''):
        super().__init__(root, 'Caesar Frequency Analysis', back_callback)
        if initial_text:
            self.text_widget.delete('1.0', 'end')
            self.text_widget.insert('1.0', initial_text)
            self.analyze()

    def _build_mode_ui(self):
        btn_solve = ttk.Button(self.top_frame, text='Solve', command=self.solve_shift)
        btn_solve.grid(row=5, column=0, pady=4)

        btn_map = ttk.Button(self.top_frame, text='Show mapping', command=self.show_mapping)
        btn_map.grid(row=5, column=1, pady=4, padx=(8, 0))

    def analyze(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text:
            messagebox.showwarning('No input', 'Please enter cipher text to analyze.')
            return

        self.original_text = text
        self.base_text = text
        self.current_text_view = text
        self.current_shift = 0
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self._draw_frequency_from_text(text)
        self.info_label.config(text=f'Cipher text length {len(text)} chars, alphabetic {sum(ch.isalpha() for ch in text)} letters.')

    def shift_text(self, delta: int):
        if not self.current_text_view:
            messagebox.showinfo('Analyze first', 'Please click Analyze before shifting.')
            return

        self._save_undo_state()
        shifted = caesar_shift_text(self.current_text_view, delta)
        self.current_text_view = shifted
        self.update_current_shift(delta)
        self._draw_frequency_from_text(shifted)
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', shifted)
        self.validation_label.config(text='')

    def solve_shift(self):
        if not self.base_text:
            messagebox.showinfo('Analyze first', 'Please click Analyze first before solving.')
            return

        shift = self.validate_shift()
        if shift is None:
            return

        self._save_undo_state()
        solved_text = caesar_shift_text(self.base_text, shift)
        self.base_text = solved_text
        self.current_text_view = solved_text
        self.current_shift = shift
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', solved_text)
        self._draw_frequency_from_text(solved_text)
        self.info_label.config(text=f'Solved with shift {shift}.')

    def reset_text(self):
        self.solve_shift_var.set('0')
        self.validation_label.config(text='')
        self.current_shift = 0
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self.undo_stack.clear()

        if self.original_text:
            self.base_text = self.original_text
            self.current_text_view = self.original_text
            self.text_widget.delete('1.0', 'end')
            self.text_widget.insert('1.0', self.original_text)
            self._draw_frequency_from_text(self.original_text)
            self.info_label.config(text='Reset to original ciphertext.')
        else:
            self.base_text = ''
            self.current_text_view = ''
            self.text_widget.delete('1.0', 'end')
            self._draw_frequency_from_text('')
            self.info_label.config(text='Type or paste text, then click Analyze.')


class VigenereFrequencyAnalysisApp(BaseFrequencyAnalysisApp):
    def __init__(self, root: tk.Tk | tk.Toplevel, back_callback, initial_text: str = ''):
        self.column_keylen = None
        self.column_index = None
        self.column_selection = ''
        super().__init__(root, 'Vigenere Frequency Analysis', back_callback)
        if initial_text:
            self.text_widget.delete('1.0', 'end')
            self.text_widget.insert('1.0', initial_text)
            self.analyze()

    def _build_mode_ui(self):
        ttk.Label(self.top_frame, text='Key length n:').grid(row=6, column=0, sticky='e')
        self.keylen_entry = ttk.Entry(self.top_frame, width=5)
        self.keylen_entry.grid(row=6, column=1, sticky='w', padx=(10, 0))
        self.keylen_entry.insert(0, '1')

        ttk.Label(self.top_frame, text='Column i (0..n-1):').grid(row=6, column=2, sticky='e')
        self.column_entry = ttk.Entry(self.top_frame, width=5)
        self.column_entry.grid(row=6, column=3, sticky='w', padx=(8, 0))
        self.column_entry.insert(0, '0')

        btn_column = ttk.Button(self.top_frame, text='Analyze column', command=self.analyze_column)
        btn_column.grid(row=6, column=4, pady=4, padx=(8, 0))

        btn_solve_col = ttk.Button(self.top_frame, text='Solve column', command=self.solve_column_shift)
        btn_solve_col.grid(row=5, column=1, pady=4, padx=(8, 0))

        btn_map = ttk.Button(self.top_frame, text='Show mapping', command=self.show_mapping)
        btn_map.grid(row=5, column=2, pady=4, padx=(8, 0))

        btn_column = ttk.Button(self.top_frame, text='Analyze column', command=self.analyze_column)
        btn_column.grid(row=7, column=1, pady=4)

        btn_solve_col = ttk.Button(self.top_frame, text='Solve column', command=self.solve_column_shift)
        btn_solve_col.grid(row=5, column=1, pady=4, padx=(8, 0))

        btn_map = ttk.Button(self.top_frame, text='Show mapping', command=self.show_mapping)
        btn_map.grid(row=5, column=2, pady=4, padx=(8, 0))

    def analyze(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text:
            messagebox.showwarning('No input', 'Please enter cipher text to analyze.')
            return

        self.original_text = text
        self.base_text = text
        self.current_text_view = text
        self.current_shift = 0
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self.column_selection = ''
        self.column_keylen = None
        self.column_index = None
        self._draw_frequency_from_text(text)
        self.info_label.config(text=f'Cipher text length {len(text)} chars, alphabetic {sum(ch.isalpha() for ch in text)} letters.')

    def analyze_column(self):
        text = self.text_widget.get('1.0', 'end').strip()
        if not text:
            messagebox.showwarning('No input', 'Please enter cipher text to analyze.')
            return

        try:
            key_len = max(1, int(self.keylen_entry.get()))
            col_idx = int(self.column_entry.get())
        except ValueError:
            messagebox.showwarning('Invalid input', 'Key length and column must be integers.')
            return

        if key_len < 1 or col_idx < 0 or col_idx >= key_len:
            messagebox.showwarning('Invalid input', 'Column index must be between 0 and key length - 1.')
            return

        sanitized = ''.join(ch for ch in text.upper() if ch.isalpha())
        selected = sanitized[col_idx::key_len]

        if not selected:
            messagebox.showinfo('Empty subset', 'No letters in chosen column; check key length or text.')
            return

        freq = compute_frequency(selected)
        self._draw_frequency(freq)
        self.column_selection = selected
        self.current_text_view = selected
        self.current_shift = 0
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')

        self.column_keylen = key_len
        self.column_index = col_idx
        self.info_label.config(text=f'Column {col_idx} of key length {key_len} subset size {len(selected)}.')


    def _save_undo_state(self, extra=None):
        state = {
            'base_text': self.base_text,
            'current_text_view': self.current_text_view,
            'current_shift': self.current_shift,
            'column_keylen': self.column_keylen,
            'column_index': self.column_index,
            'column_selection': self.column_selection,
        }
        if extra:
            state.update(extra)
        self.undo_stack.append(state)
        if len(self.undo_stack) > 3:
            self.undo_stack.pop(0)


    def shift_text(self, delta: int):
        if not self.current_text_view:
            messagebox.showinfo('Analyze first', 'Please click Analyze or Analyze column before shifting.')
            return

        self._save_undo_state()
        shifted = caesar_shift_text(self.current_text_view, delta)
        self.current_text_view = shifted
        self.current_shift = (self.current_shift + delta) % 26
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self._draw_frequency_from_text(shifted)
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', shifted)
        self.validation_label.config(text='')

    def solve_shift(self):
        if not self.base_text:
            messagebox.showinfo('Analyze first', 'Please click Analyze first before solving.')
            return

        shift = self.validate_shift()
        if shift is None:
            return

        self._save_undo_state()
        solved_text = caesar_shift_text(self.base_text, shift)
        self.base_text = solved_text
        self.current_text_view = solved_text
        self.current_shift = shift
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', solved_text)
        self._draw_frequency_from_text(solved_text)
        self.info_label.config(text=f'Solved with shift {shift}.')

    def solve_column_shift(self):
        if not self.base_text or self.column_keylen is None or self.column_index is None or not self.column_selection:
            messagebox.showinfo('Select column', 'Please run Analyze column first before solving this column.')
            return

        shift = self.validate_shift()
        if shift is None:
            return

        decrypted_column = caesar_shift_text(self.column_selection, shift)
        result_chars = []
        col_pos = 0
        alpha_count = 0

        for ch in self.base_text:
            if ch.isalpha():
                if alpha_count % self.column_keylen == self.column_index:
                    d = decrypted_column[col_pos]
                    result_chars.append(d.upper() if ch.isupper() else d.lower())
                    col_pos += 1
                else:
                    result_chars.append(ch)
                alpha_count += 1
            else:
                result_chars.append(ch)

        self._save_undo_state()
        solved_text = ''.join(result_chars)
        self.base_text = solved_text
        self.current_text_view = decrypted_column
        self.current_shift = shift
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', solved_text)
        self._draw_frequency_from_text(decrypted_column)
        self.info_label.config(text=f'Solved column {self.column_index} (keylen {self.column_keylen}) with shift {shift}.')

    def reset_text(self):
        self.solve_shift_var.set('0')
        self.validation_label.config(text='')
        self.current_shift = 0
        self.current_shift_label.config(text=f'Current shift: {self.current_shift}')
        self.undo_stack.clear()

        if self.original_text:
            self.base_text = self.original_text
            self.current_text_view = self.original_text
            self.column_selection = ''
            self.column_keylen = None
            self.column_index = None
            self.text_widget.delete('1.0', 'end')
            self.text_widget.insert('1.0', self.original_text)
            self._draw_frequency_from_text(self.original_text)
            self.info_label.config(text='Reset to original ciphertext.')
        else:
            self.base_text = ''
            self.current_text_view = ''
            self.text_widget.delete('1.0', 'end')
            self._draw_frequency_from_text('')
            self.info_label.config(text='Type or paste text, then click Analyze.')


class FrequencyToolApp:
    def __init__(self, root: tk.Tk | tk.Toplevel, initial_text: str = ''):
        self.root = root
        self.root.title('Frequency Analysis Toolbox')
        self.root.state('zoomed')
        self.initial_text = initial_text
        self.show_menu()

    def clear_root(self):
        for child in self.root.winfo_children():
            child.destroy()

    def show_menu(self):
        self.clear_root()
        self.root.title('Frequency Analysis Toolbox')

        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text='Choose frequency analysis mode:', font=('Segoe UI', 14, 'bold')).pack(pady=(0, 16))

        btn_caesar = ttk.Button(frame, text='Caesar frequency analysis', command=self.show_caesar)
        btn_caesar.pack(pady=8, ipadx=20, ipady=10)

        btn_vigenere = ttk.Button(frame, text='Vigenere frequency analysis', command=self.show_vigenere)
        btn_vigenere.pack(pady=8, ipadx=20, ipady=10)

        ttk.Label(frame, text='Caesar: simple letter shift analysis. Vigenere: column-based key building and subset frequency analysis.', wraplength=760).pack(pady=(12, 0))

    def show_caesar(self):
        self.clear_root()
        CaesarFrequencyAnalysisApp(self.root, self.show_menu, initial_text=self.initial_text)

    def show_vigenere(self):
        self.clear_root()
        VigenereFrequencyAnalysisApp(self.root, self.show_menu, initial_text=self.initial_text)


def main():
    root = tk.Tk()
    app = FrequencyToolApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
