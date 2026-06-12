import tkinter as tk
from tkinter import messagebox

from phase1 import (
    lex,
    Parser,
    CodeGenerator,
    SemanticAnalyzer,
    optimize_instructions,
    format_tokens,
    format_ast,
    format_semantic,
    format_codegen,
    format_optimized,
)

# Layout / theme
BG_APP = "#1a1d23"
BG_PANEL = "#252830"
BG_TITLE = "#2f3540"
BG_TEXT = "#1e2229"
FG_TEXT = "#e6e8ef"
FG_MUTED = "#9aa3b2"
ACCENT = "#3d9eff"
ACCENT_DIM = "#4a5568"
HIGHLIGHT_BORDER = "#3d9eff"
HIGHLIGHT_TITLE = "#2563a8"
HIGHLIGHT_PANEL = "#1a3048"


class CompilerFrontend(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Intermediate Code Generator - Full Program Pipeline")
        self.geometry("1580x800")
        self.minsize(1280, 680)
        self.configure(bg=BG_APP)

        self._phase_border_idle = ["#4a5568", "#5c6570", "#6b7280", "#5c6570", "#4a5568"]
        self._build_ui()

    def _build_ui(self) -> None:
        header = tk.Frame(self, bg=BG_APP)
        header.pack(fill="x", padx=28, pady=(18, 8))

        title = tk.Label(
            header,
            text="Intermediate Code Generator",
            font=("Segoe UI", 22, "bold"),
            fg="#ffffff",
            bg=BG_APP,
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Paste code -> see 5 simple phases: tokens, AST, semantic, code, optimized",
            font=("Segoe UI", 12),
            fg=FG_MUTED,
            bg=BG_APP,
        )
        subtitle.pack(anchor="w", pady=(6, 0))

        input_frame = tk.Frame(self, bg=BG_APP)
        input_frame.pack(fill="x", padx=28, pady=(12, 4))

        input_label = tk.Label(
            input_frame,
            text="Source code:",
            font=("Segoe UI", 11),
            fg="#ffffff",
            bg=BG_APP,
        )
        input_label.pack(side="left")

        run_button = tk.Button(
            input_frame,
            text="Run pipeline",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT,
            fg="#ffffff",
            activebackground="#2b7fd4",
            activeforeground="#ffffff",
            relief="flat",
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.run_pipeline,
        )
        run_button.pack(side="right")

        self.input_entry = tk.Text(
            self,
            font=("Consolas", 12),
            bg=BG_TEXT,
            fg=FG_TEXT,
            insertbackground=ACCENT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=ACCENT_DIM,
            highlightcolor=ACCENT,
            height=8,
            wrap="none",
        )
        self.input_entry.pack(fill="x", padx=28, pady=(0, 10))
        self.input_entry.insert(
            "1.0",
            "int x = 5;\nint y = 2;\nint z = x + y * 3;\nprintf(z);\n"
            "if (z > 10) {\n  printf(z);\n} else {\n  z = z + 1;\n  printf(z);\n}\n"
            "while (y < 5) {\n  y = y + 1;\n  printf(y);\n}\n",
        )

        phases_frame = tk.Frame(self, bg=BG_APP)
        phases_frame.pack(fill="both", expand=True, padx=16, pady=(8, 12))
        phases_frame.grid_rowconfigure(0, weight=1)
        for c in range(5):
            phases_frame.grid_columnconfigure(c, weight=1, uniform="phase")

        self.phase_boxes: list[tuple[tk.Frame, tk.Label, tk.Text]] = []
        phase_titles = [
            "Phase 1 - Tokens",
            "Phase 2 - AST",
            "Phase 3 - Semantic",
            "Phase 4 - TAC",
            "Phase 5 - Optimized",
        ]

        for idx, title_text in enumerate(phase_titles):
            border = self._phase_border_idle[idx % len(self._phase_border_idle)]
            frame = tk.Frame(
                phases_frame,
                bg=BG_PANEL,
                highlightbackground=border,
                highlightthickness=2,
                bd=0,
            )
            frame.grid(row=0, column=idx, padx=6, pady=6, sticky="nsew")

            title_label = tk.Label(
                frame,
                text=title_text,
                font=("Segoe UI", 11, "bold"),
                fg="#ffffff",
                bg=BG_TITLE,
                anchor="center",
                pady=10,
                padx=6,
            )
            title_label.pack(fill="x")

            content = tk.Text(
                frame,
                font=("Consolas", 10),
                bg=BG_TEXT,
                fg=FG_TEXT,
                wrap="word",
                height=26,
                borderwidth=0,
                highlightthickness=0,
                padx=10,
                pady=10,
                state="disabled",
            )
            content.pack(fill="both", expand=True, padx=8, pady=(0, 10))

            self.phase_boxes.append((frame, title_label, content))

        self.status_label = tk.Label(
            self,
            text="Ready.",
            font=("Segoe UI", 10),
            fg=FG_MUTED,
            bg=BG_APP,
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=28, pady=(0, 14))

    def clear_boxes(self) -> None:
        for i, (frame, title, content) in enumerate(self.phase_boxes):
            border = self._phase_border_idle[i % len(self._phase_border_idle)]
            frame.configure(bg=BG_PANEL, highlightbackground=border, highlightthickness=2)
            title.configure(bg=BG_TITLE)
            content.configure(state="normal")
            content.delete("1.0", tk.END)
            content.configure(state="disabled")

    def highlight_box(self, index: int) -> None:
        for i, (frame, title, _) in enumerate(self.phase_boxes):
            if i == index:
                frame.configure(bg=HIGHLIGHT_PANEL, highlightbackground=HIGHLIGHT_BORDER, highlightthickness=3)
                title.configure(bg=HIGHLIGHT_TITLE)
            else:
                border = self._phase_border_idle[i % len(self._phase_border_idle)]
                frame.configure(bg=BG_PANEL, highlightbackground=border, highlightthickness=2)
                title.configure(bg=BG_TITLE)

    def set_box_content(self, index: int, text: str) -> None:
        _, _, content = self.phase_boxes[index]
        content.configure(state="normal")
        content.delete("1.0", tk.END)
        content.insert(tk.END, text)
        content.configure(state="disabled")

    def run_pipeline(self) -> None:
        source = self.input_entry.get("1.0", "end-1c").strip()
        if not source:
            messagebox.showwarning("No input", "Please enter source code first.")
            return

        try:
            self.clear_boxes()
            self.status_label.configure(text="Running pipeline...")

            tokens = lex(source)
            tokens_text = format_tokens(tokens)

            parser = Parser(tokens)
            ast = parser.parse()
            ast_text = format_ast(ast)

            semantic = SemanticAnalyzer().analyze(ast)
            sem_text = format_semantic(semantic)

            if semantic.ok:
                codegen = CodeGenerator()
                raw_instructions, _ = codegen.generate(ast)
                optimized_instructions = optimize_instructions(raw_instructions)
                code_text = format_codegen(raw_instructions)
                opt_text = format_optimized(raw_instructions, optimized_instructions)
            else:
                code_text = "PHASE 4: CODE GENERATION\n\nSkipped (fix Phase 3 errors first)."
                opt_text = "PHASE 5: OPTIMIZATION\n\nSkipped."

            steps = [
                (0, f"YOUR CODE:\n{source}\n\n{tokens_text}"),
                (1, ast_text),
                (2, sem_text),
                (3, code_text),
                (4, opt_text),
            ]

            delay_ms = 500

            def make_step_callback(idx: int, text: str):
                def _cb() -> None:
                    self.highlight_box(idx)
                    self.set_box_content(idx, text)
                    title_widget = self.phase_boxes[idx][1]
                    self.status_label.configure(text=f"Showing: {title_widget.cget('text')}")

                return _cb

            for i, (idx, text) in enumerate(steps):
                self.after(i * delay_ms, make_step_callback(idx, text))

            final = "Pipeline complete." if semantic.ok else "Stopped after semantic errors."
            self.after(len(steps) * delay_ms + 50, lambda: self.status_label.configure(text=final))

        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Error", f"An error occurred:\n{e}")
            self.status_label.configure(text="Error during pipeline.")


def main() -> None:
    app = CompilerFrontend()
    app.mainloop()


if __name__ == "__main__":
    main()
