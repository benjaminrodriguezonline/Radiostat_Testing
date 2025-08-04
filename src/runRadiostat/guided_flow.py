import tkinter as tk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
import json
import os
from runRadiostat.analyze_cv import analyze_cv_file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from runRadiostat.beaker_test import run_beaker_test

class Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

class GuidedFlowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beaker Cell Activity")
        self.geometry("800x600")
        # Set default font size globally
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=16)
        self.option_add("*Font", default_font)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.pages = {}
        self.responses = {}

        # Order: IntroPage, DemoTestPage, RunTestPage, ExplainPage, AnalyzePage, CERPage, ConclusionPage
        for PageClass in (IntroPage, DemoTestPage, RunTestPage, ExplainPage, AnalyzePage, CERPage, ConclusionPage):
            page = PageClass(parent=container, controller=self)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("IntroPage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

    def save_responses(self):
        os.makedirs("output", exist_ok=True)
        with open("output/student_responses.json", "w") as f:
            json.dump(self.responses, f, indent=2)

class IntroPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        title = tk.Label(self, text="Welcome to the Beaker Cell Lab", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        instructions = (
            "Over the next several steps, you'll take part in a real research simulation inspired by work "
            "done in university battery labs. You'll explore how different electrolytes affect battery rechargeability. and answer the question\n\nWhich Electrolyte Makes the Most Efficient Battery?\n\n"
            "In this activity, you will:\n"
            "- Choose electrolytes to test\n"
            "- Run a real electrochemical experiment\n"
            "- Analyze your data\n"
            "- Write a scientific conclusion\n\n"
            "First, take a moment to reflect..."
        )
        body = tk.Label(self, text=instructions, justify="left", wraplength=550)
        body.pack(pady=10)

        prompt = tk.Label(self, text="💭 Why do you think rechargeable batteries work?\nWhat do you think happens inside them?")
        prompt.pack(pady=(20, 5))

        self.response_box = tk.Text(self, height=5, width=70)
        self.response_box.pack()

        next_btn = tk.Button(self, text="Next →", command=lambda: [self.save_response(), controller.save_responses(), controller.show_page("DemoTestPage")])
        next_btn.pack(pady=15)

    def save_response(self):
        response = self.response_box.get("1.0", tk.END).strip()
        self.controller.responses["intro_reflection"] = response


# --- DemoTestPage replacement for TestPage ---
class DemoTestPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.controller = controller

        tk.Label(self, text="Teacher Demonstration", font=("Helvetica", 16, "bold")).pack(pady=10)

        instructions = (
            "Watch carefully as your teacher runs a real electrochemical test using a beaker cell.\n"
            "Focus on the black circular working electrode during the test. You may see something happening!\n\n"
            "After the test runs, you’ll see two graphs and be asked to describe what you observed."
        )
        tk.Label(self, text=instructions, justify="left", wraplength=560).pack(pady=10)

        buttonInfo = (
            "Let your teacher press this button"
        )

        tk.Label(self, text=buttonInfo, justify="center", wraplength=560).pack(pady=10)

        self.run_btn = tk.Button(self, text="▶️ Run Demo Test", command=self.run_demo_test)
        self.run_btn.pack(pady=10)

        self.status_label = tk.Label(self, text="", font=("Helvetica", 12), fg="green")
        self.status_label.pack()

        self.canvas1 = None
        self.canvas2 = None

        tk.Label(self, text="👀 What did you observe at the working electrode?", anchor="w").pack(pady=(20, 5))
        self.observation_box = tk.Text(self, height=5, width=70)
        self.observation_box.pack()

        back_btn = tk.Button(self, text="← Back", command=lambda: controller.show_page("IntroPage"))
        back_btn.pack(pady=5)

        next_btn = tk.Button(self, text="Next →", command=lambda: [self.save_response(), controller.save_responses(), controller.show_page("RunTestPage")])
        next_btn.pack(pady=15)

    def run_demo_test(self):
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import numpy as np
        import os
        import glob
        import pandas as pd

        try:
            run_beaker_test()
            self.status_label.config(text="Demo test completed successfully!", fg="green")

            files = sorted(glob.glob("output/cv_data_*.txt"), key=os.path.getmtime)
            latest = files[-1]
            df = pd.read_csv(latest, sep="\t")

            t = df["Time (s)"]
            v = df["Voltage (V)"]
            c = df["Current (uA)"] / 1000  # mA

            if self.canvas1:
                self.canvas1.get_tk_widget().destroy()
            if self.canvas2:
                self.canvas2.get_tk_widget().destroy()

            fig1, ax1 = plt.subplots(figsize=(8.5, 2.5))
            ax1.plot(t, v)
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Voltage (V)")
            ax1.set_title("Voltage vs Time – Demo Test")
            ax1.grid(True)
            fig1.tight_layout()
            self.canvas1 = FigureCanvasTkAgg(fig1, master=self)
            self.canvas1.draw()
            self.canvas1.get_tk_widget().pack(pady=5)

            fig2, ax2 = plt.subplots(figsize=(8.5, 2.5))
            ax2.plot(v, c)
            ax2.set_xlabel("Voltage (V)")
            ax2.set_ylabel("Current (mA)")
            ax2.set_title("Current vs Voltage – Demo Test")
            ax2.grid(True)
            fig2.tight_layout()
            self.canvas2 = FigureCanvasTkAgg(fig2, master=self)
            self.canvas2.draw()
            self.canvas2.get_tk_widget().pack(pady=5)

        except Exception as e:
            self.status_label.config(text=f"Test failed: {e}", fg="red")

    def save_response(self):
        observation = self.observation_box.get("1.0", tk.END).strip()
        self.controller.responses["demo_observation"] = observation

class RunTestPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Only one <Configure> binding: update window width to match canvas width
        self.window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(self.window_id, width=e.width))
        # Update scrollregion when scrollable_frame changes size
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="Run Test Phase", font=("Helvetica", 16, "bold")).pack(fill="x", expand=True, pady=10)

        info_text = (
            "Now it's time to run the electrochemical experiment with the electrolytes you've chosen.\n\n"
            "Follow the instructions on the potentiostat device and observe the results.\n\n"
            "When you're ready, proceed to the explanation phase to analyze your observations."
        )
        tk.Label(scrollable_frame, text=info_text, justify="left", wraplength=560).pack(fill="x", expand=True, pady=10)

        setup_frame = tk.LabelFrame(scrollable_frame, text="🛠 Beaker Cell Setup Instructions", padx=10, pady=5)
        setup_frame.pack(fill="x", expand=True, pady=10)

        setup_steps = (
            "1. Rinse all electrodes thoroughly with deionized (DI) water.\n"
            "2. Empty the beaker back into an electrolyte holding vial."
            "3. Rinse the beaker thoroughly with deionized (DI) water."
            "4. Wipe dry or allow beaker and electrodes to air dry before reuse.\n"
            "5. Add 20 mL of your chosen zinc-based electrolyte into a clean 50 mL beaker.\n"
            "6. Insert the three electrodes into the solution:\n"
            "   • Working electrode (black circular) can touch the bottom.\n"
            "   • Counter and reference electrodes should be suspended and not touching each other.\n"
            "   • Try to position working and counter electrodes on either side of the reference electrode.\n"
            "7. Secure electrodes using a ring stand or holder.\n"
            "8. Connect the potentiostat wires:\n"
            "   • Red → Working\n"
            "   • Yellow → Counter\n"
            "   • Green → Reference\n"
            "9. Double-check that electrodes are not touching and are submerged properly.\n"
            "10. You're ready to run your test!"
        )

        tk.Label(setup_frame, text=setup_steps, justify="left", anchor="w", wraplength=550).pack()

        self.test_canvases = [None, None, None]
        self.annotation_boxes = []

        for i in range(3):
            test_label = tk.Label(scrollable_frame, text=f"Test {i+1}", font=("Helvetica", 14, "bold"))
            test_label.pack(fill="x", expand=True, pady=(15, 5))

            run_btn = tk.Button(scrollable_frame, text=f"Run Beaker Test {i+1}", command=lambda i=i: self.run_test(i))
            run_btn.pack(fill="x", expand=True, pady=5)

            setattr(self, f"status_label_{i}", tk.Label(scrollable_frame, text="", font=("Helvetica", 12), fg="green"))
            getattr(self, f"status_label_{i}").pack(fill="x", expand=True, pady=2)

            annotation_label = tk.Label(scrollable_frame, text="📝 Annotate this graph:\nWhat did you observe in this run?", justify="left", wraplength=560)
            annotation_label.pack(fill="x", expand=True, pady=(10, 2))

            annotation_box = tk.Text(scrollable_frame, height=5, width=70)
            annotation_box.pack(fill="x", expand=True, pady=5)
            self.annotation_boxes.append(annotation_box)

        back_btn = tk.Button(scrollable_frame, text="← Back", command=lambda: controller.show_page("TestPage"))
        back_btn.pack(fill="x", expand=True, pady=5)

        next_btn = tk.Button(scrollable_frame, text="Next →", command=lambda: [self.save_response(), controller.save_responses(), controller.show_page("ExplainPage")])
        next_btn.pack(fill="x", expand=True, pady=15)

        self.scrollable_frame = scrollable_frame
        self.canvas = canvas

    def run_test(self, test_index):
        try:
            run_beaker_test()
            status_label = getattr(self, f"status_label_{test_index}")
            status_label.config(text=f"Test {test_index + 1} completed successfully!", fg="green")
        except Exception as e:
            status_label = getattr(self, f"status_label_{test_index}")
            status_label.config(text=f"Test failed: {e}", fg="red")
            return

        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import numpy as np
        import os
        import glob
        import pandas as pd

        try:
            files = sorted(glob.glob("output/cv_data_*.txt"), key=os.path.getmtime)
            latest = files[-1]
            df = pd.read_csv(latest, sep="\t")

            t = df["Time (s)"]
            v = df["Voltage (V)"]
            c = df["Current (uA)"] / 1000  # mA

            # Remove previous canvases if they exist for this test
            if self.test_canvases[test_index] is not None:
                for canvas in self.test_canvases[test_index]:
                    canvas.get_tk_widget().destroy()

            fig1, ax1 = plt.subplots(figsize=(8.5, 2.5))
            ax1.plot(t, v)
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Voltage (V)")
            ax1.set_title(f"Voltage vs Time - Test {test_index + 1}")
            ax1.grid(True)
            fig1.tight_layout()
            canvas1 = FigureCanvasTkAgg(fig1, master=self.scrollable_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(pady=5)

            fig2, ax2 = plt.subplots(figsize=(8.5, 2.5))
            ax2.plot(v, c)
            ax2.set_xlabel("Voltage (V)")
            ax2.set_ylabel("Current (mA)")
            ax2.set_title(f"Current vs Voltage - Test {test_index + 1}")
            ax2.grid(True)
            fig2.tight_layout()
            canvas2 = FigureCanvasTkAgg(fig2, master=self.scrollable_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(pady=5)

            self.test_canvases[test_index] = (canvas1, canvas2)

        except Exception as e:
            status_label.config(text=f"Plotting failed: {e}", fg="orange")

    def save_response(self):
        for i, box in enumerate(self.annotation_boxes):
            annotation = box.get("1.0", tk.END).strip()
            self.controller.responses[f"test{i+1}_graph_annotation"] = annotation
        self.controller.save_responses()

class ExplainPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self, text="Explain Phase – Build Your Scientific Understanding", font=("Helvetica", 16, "bold")).pack(pady=10)

        intro_text = (
            "Welcome to the Explain Phase of your battery experiment.\n\n"
            "Here, you'll build a deeper understanding of what you've observed through your CV scans. "
            "This is your chance to learn the science that powers your results.\n\n"
            "🔑 Key Concepts:\n"
            "• **Redox** – A reaction where electrons are transferred. Reduction is gain of electrons, oxidation is loss.\n"
            "• **Plating** – Metal ions in the electrolyte gain electrons and become solid metal on the electrode.\n"
            "• **Stripping** – Solid metal on the electrode loses electrons and dissolves back into the electrolyte.\n"
            "• **Coulombic Efficiency** – A measure of how effectively charge is recovered compared to what was input.\n\n"
            "📈 In your experiment:\n"
            "• During plating, current flows in one direction (negative).\n"
            "• During stripping, it flows in the opposite direction (positive).\n"
            "• The area under the current vs time curve represents the charge for each process.\n\n"
            "💡 You'll use this understanding to calculate how efficient each electrolyte was.\n"
            "Proceed to the next step to analyze your results."
        )
        tk.Label(self, text=intro_text, justify="left", wraplength=560).pack(pady=10)

        tk.Label(self, text="🧪 Recalling what you observed during the initial demonstration and your own measurements, attempt to describe your observations again using at least three of the academic vocabulary listed in this lesson.", anchor="w").pack(anchor="w", padx=15)
        self.vocab_response = tk.Text(self, height=4, width=70)
        self.vocab_response.pack(pady=5)

        back_btn = tk.Button(self, text="← Back", command=lambda: controller.show_page("RunTestPage"))
        back_btn.pack(pady=5)

        next_btn = tk.Button(self, text="Next →", command=lambda: [self.save_response(), controller.save_responses(), controller.show_page("AnalyzePage")])
        next_btn.pack(pady=15)

    def save_response(self):
        vocab = self.vocab_response.get("1.0", tk.END).strip()
        self.controller.responses["vocab_terms"] = vocab

class CERPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self, text="Make Your Scientific Argument", font=("Helvetica", 16, "bold")).pack(pady=10)

        intro = (
            "Use the Claim–Evidence–Reasoning framework to summarize your findings about the electrolytes you tested.\n\n"
            "👉 *Claim:* What electrolyte performed best?\n"
            "👉 *Evidence:* What did you observe in the CV scan(s)?\n"
            "👉 *Reasoning:* Why do you think it behaved this way, based on your new understanding?"
        )
        tk.Label(self, text=intro, justify="left", wraplength=560).pack(pady=10)

        tk.Label(self, text="✍️ Write your CER response below:").pack(anchor="w", padx=15)
        self.cer_response = tk.Text(self, height=10, width=70)
        self.cer_response.pack(pady=10)

        back_btn = tk.Button(self, text="← Back", command=lambda: controller.show_page("AnalyzePage"))
        back_btn.pack(pady=5)

        next_btn = tk.Button(self, text="Next →", command=lambda: [self.save_response(), controller.save_responses(), controller.show_page("ConclusionPage")])
        next_btn.pack(pady=15)

    def save_response(self):
        cer = self.cer_response.get("1.0", tk.END).strip()
        self.controller.responses["cer_argument"] = cer

import tkinter.filedialog as fd
import numpy as np
import csv

class AnalyzePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # 1. Wrap content in a scrollable canvas
        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        self.window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(self.window_id, width=e.width))
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = scrollable_frame

        # 2. Replace previous widgets with a loop to create 3 upload sections
        self.result_labels = []
        self.canvases = []
        self.ce_entries = []

        tk.Label(scrollable_frame, text="Quantitative Analysis: Coulombic Efficiency", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Label(
            scrollable_frame,
            text="Upload your potentiostat `.txt` output files below to analyze the area under your CV curves.",
            wraplength=560
        ).pack(pady=10)

        for i in range(3):
            tk.Label(
                scrollable_frame,
                text=f"Test {i+1}",
                font=("Helvetica", 14, "bold")
            ).pack(pady=(15, 5))

            upload_btn = tk.Button(
                scrollable_frame,
                text=f"📂 Upload CV Data File for Test {i+1} (Current vs Time - Charge Integration)",
                command=lambda i=i: self.load_and_analyze(i)
            )
            upload_btn.pack(pady=5)

            result_label = tk.Label(
                scrollable_frame,
                text="",
                font=("Helvetica", 12),
                wraplength=560,
                justify="left"
            )
            result_label.pack(pady=10)
            self.result_labels.append(result_label)

            # Add CE entry prompt and entry box after each result label
            tk.Label(
                scrollable_frame,
                text="💬 Enter your calculated Coulombic Efficiency (%):"
            ).pack(pady=(5, 2))
            ce_entry = tk.Entry(scrollable_frame)
            ce_entry.pack(pady=(0, 10))
            self.ce_entries.append(ce_entry)

            self.canvases.append(None)

        back_btn = tk.Button(scrollable_frame, text="← Back", command=lambda: controller.show_page("ExplainPage"))
        back_btn.pack(pady=5)

        next_btn = tk.Button(
            scrollable_frame,
            text="Next →",
            command=lambda: [self.save_response(), controller.save_responses(), controller.show_page("CERPage")]
        )
        next_btn.pack(pady=10)

    # 3. Update load_and_analyze to accept a test index
    def load_and_analyze(self, index):
        filepath = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        try:
            charge_ox, charge_red, ce, time, current, current_ox, current_red = analyze_cv_file(filepath)
            result_text = (
                f"Stripping Charge: {charge_ox:.4f} mC\n"
                f"Plating Charge: {charge_red:.4f} mC\n\n"
                f"⚠️ Use the formula below to calculate Coulombic Efficiency:\n"
                f"CE (%) = (Smaller Charge ÷ Larger Charge) × 100"
            )
            self.result_labels[index].config(text=result_text)

            if self.canvases[index] is not None:
                self.canvases[index].get_tk_widget().destroy()
                self.canvases[index] = None

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(time, current, label='Current (mA)', color='black')
            ax.fill_between(time, 0, current_ox, color='red', alpha=0.3, label='Stripping Area')
            ax.fill_between(time, 0, current_red, color='blue', alpha=0.3, label='Plating Area')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Current (mA)')
            ax.set_title(f'Current vs Time with Integrated Areas – Test {index+1}')
            ax.legend()
            fig.tight_layout()

            self.canvases[index] = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            self.canvases[index].draw()
            self.canvases[index].get_tk_widget().pack(pady=10)

        except Exception as e:
            self.result_labels[index].config(text=f"Error processing file: {e}")

    def save_response(self):
        for i, entry in enumerate(self.ce_entries):
            ce_value = entry.get().strip()
            self.controller.responses[f"test{i+1}_calculated_ce"] = ce_value
        self.controller.save_responses()

class ConclusionPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self, text="Final Reflection & Conclusion", font=("Helvetica", 16, "bold")).pack(pady=10)

        intro = (
            "You're at the end of your investigation!\n\n"
            "Reflect on what you discovered during this experiment:\n"
            "• What was your original hypothesis or question?\n"
            "• How did the data (CV curves and efficiency) support or contradict your expectations?\n"
            "• Which electrolyte performed best, and why?\n"
            "• What challenges or surprises came up during the process?\n\n"
            "Write your final conclusion below:"
        )
        tk.Label(self, text=intro, justify="left", wraplength=560).pack(pady=10)

        self.conclusion_box = tk.Text(self, height=12, width=70)
        self.conclusion_box.pack(pady=10)

        back_btn = tk.Button(self, text="← Back", command=lambda: controller.show_page("AnalyzePage"))
        back_btn.pack(pady=5)

        tk.Button(self, text="Submit", command=self.submit).pack(pady=5)

        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.pack()

        next_btn = tk.Button(self, text="Next →", command=lambda: [self.save_response(), controller.save_responses(), controller.show_page("IntroPage")])
        next_btn.pack_forget()

    def save_response(self):
        conclusion = self.conclusion_box.get("1.0", tk.END).strip()
        self.controller.responses["final_conclusion"] = conclusion

    def submit(self):
        conclusion = self.conclusion_box.get("1.0", tk.END).strip()
        if conclusion:
            self.controller.responses["final_conclusion"] = conclusion
            self.controller.save_responses()
            self.status_label.config(text="Conclusion submitted successfully!", fg="green")
        else:
            self.status_label.config(text="Please write something before submitting.", fg="red")