import tkinter
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
from matplotlib import pyplot as plt

from src.matrix import Matrix


class Interface:
    def __init__(self, root: tkinter.Tk):
        self.root = root
        self.root.title("Оптимизация переработки")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f8ff")
        self.LABEL_FG = "#2e8b57"
        self.LABEL_BG = "#f0f8ff"
        self.LABEL_FG = "#2e8b57"
        self.ENTRY_BG = "white"
        self.ENTRY_FG = "#2e8b57"
        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg="#2e8b57", height=80)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="ОПТИМИЗАЦИЯ ПЕРЕРАБОТКИ САХАРНОЙ СВЕКЛЫ",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2e8b57",
        )
        title_label.pack(expand=True)

        main_container = tk.Frame(self.root, bg="#f0f8ff")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_frame = tk.LabelFrame(
            main_container,
            text="ПАРАМЕТРЫ ЭКСПЕРИМЕНТА",
            font=("Arial", 10, "bold"),
            bg="#f0f8ff",
            fg="#2e8b57",
            labelanchor="n",
        )
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        right_frame = tk.LabelFrame(
            main_container,
            text="РЕЗУЛЬТАТЫ",
            font=("Arial", 10, "bold"),
            bg="#f0f8ff",
            fg="#2e8b57",
            labelanchor="n",
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_parameters(left_frame)
        self.setup_results(right_frame)

    def setup_parameters(self, parent):
        tk.Label(
            parent,
            text="Количество партий свеклы:",
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            font=("Arial", 9),
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.n_var = tk.StringVar(value="15")
        n_entry = tk.Entry(
            parent,
            textvariable=self.n_var,
            width=10,
            font=("Arial", 9),
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_FG,
        )
        n_entry.grid(row=0, column=1, pady=5, padx=5)

        self.v_label = tk.Label(
            parent,
            text="Количество дней дозаривания:",
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            font=("Arial", 9),
        )
        self.v_var = tk.StringVar(value="7")
        self.v_entry = tk.Entry(
            parent,
            textvariable=self.v_var,
            width=10,
            font=("Arial", 9),
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_FG,
        )

        self.v_label.grid(row=1, column=0, sticky="w", pady=5)
        self.v_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(
            parent,
            text="Количество экспериментов:",
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            font=("Arial", 9),
        ).grid(row=2, column=0, sticky="w", pady=5)
        self.exp_var = tk.StringVar(value="50")
        exp_entry = tk.Entry(
            parent,
            textvariable=self.exp_var,
            width=10,
            font=("Arial", 9),
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_FG,
        )
        exp_entry.grid(row=2, column=1, pady=5, padx=5)

        sugar_frame = tk.LabelFrame(
            parent,
            text="Начальная сахаристость",
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            font=("Arial", 9),
        )
        sugar_frame.grid(row=3, column=0, columnspan=2, sticky="we", pady=10)

        tk.Label(
            sugar_frame,
            text="Минимум:",
            font=("Arial", 9),
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            width=10,
            anchor="w",
        ).grid(row=0, column=0, padx=5)
        self.a_min_var = tk.StringVar(value="0.12")
        tk.Entry(
            sugar_frame,
            textvariable=self.a_min_var,
            width=8,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_FG,
        ).grid(row=0, column=1, padx=5)

        tk.Label(
            sugar_frame,
            text="Максимум:",
            font=("Arial", 9),
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            width=10,
            anchor="w",
        ).grid(row=1, column=0, padx=5)
        self.a_max_var = tk.StringVar(value="0.22")
        tk.Entry(
            sugar_frame,
            textvariable=self.a_max_var,
            width=8,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_FG,
        ).grid(row=1, column=1, padx=5)

        deg_frame = tk.LabelFrame(
            parent,
            text="Коэффициенты деградации",
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            font=("Arial", 9),
        )
        deg_frame.grid(row=4, column=0, columnspan=2, sticky="we", pady=10)

        tk.Label(
            deg_frame,
            text="Минимум:",
            font=("Arial", 9),
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            width=10,
            anchor="w",
        ).grid(row=0, column=0, padx=5)
        self.b_1_var = tk.StringVar(value="0.85")
        tk.Entry(
            deg_frame,
            textvariable=self.b_1_var,
            width=8,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_FG,
        ).grid(row=0, column=1, padx=5)

        tk.Label(
            deg_frame,
            text="Максимум:",
            font=("Arial", 9),
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            width=10,
            anchor="w",
        ).grid(row=1, column=0, padx=5)
        self.b_2_var = tk.StringVar(value="1")
        tk.Entry(
            deg_frame,
            textvariable=self.b_2_var,
            width=8,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_FG,
        ).grid(row=1, column=1, padx=5)

        self.ripening_var = tk.BooleanVar()
        ripening_cb = tk.Checkbutton(
            parent,
            text="Учитывать процесс дозаривания",
            variable=self.ripening_var,
            command=self.toggle_v_field,
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            selectcolor=self.ENTRY_BG,
            font=("Arial", 9),
        )
        ripening_cb.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)
        self.toggle_v_field()

        self.sugar_loss_enabled_var = tk.BooleanVar()
        losses_cb = tk.Checkbutton(
            parent,
            text="Учитывать потери от неорганики",
            variable=self.sugar_loss_enabled_var,
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            selectcolor=self.ENTRY_BG,
            font=("Arial", 9),
        )
        losses_cb.grid(row=6, column=0, columnspan=2, sticky="w", pady=5)

        run_btn = tk.Button(
            parent,
            text="ЗАПУСТИТЬ ЭКСПЕРИМЕНТ",
            command=self.run_experiment,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            font=("Arial", 10, "bold"),
            height=2,
        )
        run_btn.grid(row=7, column=0, columnspan=2, pady=20, sticky="we")

    def validate_inputs(self):
        try:
            n = int(self.n_var.get())
            v = int(self.v_var.get())
            num_exp = int(self.exp_var.get())
            a_min = float(self.a_min_var.get())
            a_max = float(self.a_max_var.get())
            b1 = float(self.b_1_var.get())
            b2 = float(self.b_2_var.get())

            if not (0 < a_min < a_max < 1):
                raise ValueError("Некорректный диапазон сахаристости")
            if not (0 < b1 < b2 <= 1):
                raise ValueError("Некорректный диапазон деградации")
            if v >= n:
                if self.ripening_var.get():
                    msg = "Количество дней дозаривания должен быть меньше количества партий"
                else:
                    msg = "Количество этапов переключение должно быть меньше количества партий"
                raise ValueError(msg)
            if not 2 <= v <= n / 2:
                if self.ripening_var.get():
                    msg = "Количество дней дозаривания должно быть от 2 до (количество партий)/2"
                else:
                    msg = "Количество этапов переключение должн быть от 2 до (количество партий)/2"
                raise ValueError(msg)
            if not 20 <= num_exp <= 1000:
                raise ValueError("Количество экспериментов должно быть от 20 до 1000")
            if not 2 <= n <= 100:
                raise ValueError(
                    "Количество партий должно быть в диапазоне от 2 до 100"
                )

            return True
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте корректность данных:\n{e}")
            return False

    def run_experiment(self):
        if not self.validate_inputs():
            return

        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.recommendation_text.delete(1.0, tk.END)

        n = int(self.n_var.get())
        v = int(self.v_var.get())
        num_exp = int(self.exp_var.get())

        optimizer = Matrix()
        optimizer.n = n
        optimizer.v = v
        optimizer.a_min = float(self.a_min_var.get())
        optimizer.a_max = float(self.a_max_var.get())
        optimizer.b_1 = float(self.b_1_var.get())
        optimizer.b_2 = float(self.b_2_var.get())
        optimizer.num_experiments = num_exp
        optimizer.sugar_loss_enabled = self.sugar_loss_enabled_var.get()
        optimizer.ripening = self.ripening_var.get()

        avg_results, relative_losses, cumulative_results, all_results = (
            optimizer.run_algorithms()
        )

        for name, avg in avg_results.items():
            if name == "Максимальная":
                self.results_tree.insert(
                    "", "end", values=(name, f"{avg:.4f}", "0.00%")
                )
            else:
                loss = relative_losses[name]
                self.results_tree.insert(
                    "", "end", values=(name, f"{avg:.4f}", f"{loss:.2f}%")
                )

        best_strategy = min(
            [
                (name, loss)
                for name, loss in relative_losses.items()
                if name != "Максимальная"
            ],
            key=lambda x: x[1],
        )

        recommendation = "РЕКОМЕНДАЦИЯ ДЛЯ СЛЕДУЮЩЕГО СЕЗОНА:\n\n"
        recommendation += f"Лучшая стратегия: {best_strategy[0]}\n"
        recommendation += f"Относительные потери: {best_strategy[1]:.2f}%\n"
        recommendation += f"Средний выход сахара: {avg_results[best_strategy[0]]:.4f}\n"
        recommendation += (
            f"Максимально возможный выход: {avg_results['Максимальная']:.4f}\n\n"
        )

        if best_strategy[1] < 2:
            recommendation += "СТРОГО РЕКОМЕНДУЕТСЯ к применению"
        elif best_strategy[1] < 5:
            recommendation += "РЕКОМЕНДУЕТСЯ к применению"
        else:
            recommendation += "МОЖЕТ БЫТЬ РАССМОТРЕНА"

        self.recommendation_text.insert(1.0, recommendation)

        self.plot_results(
            cumulative_results, relative_losses, avg_results, all_results, n
        )

    def save_plots(self):
        try:
            import os
            from datetime import datetime

            plots_dir = "plots"
            if not os.path.exists(plots_dir):
                os.makedirs(plots_dir)

            if hasattr(self, "current_figure") and self.current_figure:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sugar_beet_results_{timestamp}.png"
                filepath = os.path.join(plots_dir, filename)

                self.current_figure.savefig(filepath, dpi=300, bbox_inches="tight")
                messagebox.showinfo(
                    "Сохранено", f"График сохранен в:\n{os.path.abspath(filepath)}"
                )
            else:
                messagebox.showwarning("Нет графика", "Сначала запустите эксперимент")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def setup_results(self, parent):
        columns = ("Стратегия", "Выход сахара", "Потери (%)")
        self.results_tree = ttk.Treeview(
            parent, columns=columns, show="headings", height=8
        )

        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120)

        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=(2, 5))

        self.recommendation_text = tk.Text(
            parent,
            height=18,
            font=("Arial", 13),
            bg=self.LABEL_BG,
            fg=self.LABEL_FG,
            wrap=tk.WORD,
        )
        self.recommendation_text.pack(fill=tk.BOTH, pady=(0, 5))
        self.recommendation_text.config(padx=2, pady=2)

        save_btn = tk.Button(
            parent,
            text="Сохранить графики",
            command=self.save_plots,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            font=("Arial", 9),
        )
        save_btn.pack(pady=5)

    def toggle_v_field(self):
        if self.ripening_var.get():
            self.v_label.config(text="Количество дней дозаривания")
        else:
            self.v_label.config(text="Количество этапов до переключения")

    def plot_results(
        self, cumulative_results, relative_losses, avg_results, all_results, n
    ):
        fig, axs = plt.subplots(2, 2, figsize=(16, 10))

        strategy_colors = {
            "Максимальная": "red",
            "Жадная": "blue",
            "Бережливая": "green",
            "Жадная/Бережливая": "orange",
            "Бережливая/Жадная": "purple",
        }

        # Добавляем информацию о флагах в заголовок всей фигуры
        flags_info = (
            f"Дозаривание: {'ВКЛЮЧЕНО' if self.ripening_var.get() else 'выключено'} | Потери от неорганики: "
            f"{'ВКЛЮЧЕНО' if self.sugar_loss_enabled_var.get() else 'выключено'}\nЭтапов {self.n_var.get()} | "
            f"{'Дней дозаривания' if self.ripening_var.get() else 'Этапов до переключения'} {self.v_var.get()} "
            f"| Экспериментов {self.exp_var.get()} "
        )
        fig.suptitle(
            f"Результаты моделирования: {flags_info}",
            fontsize=12,
            fontweight="bold",
            y=0.995,
        )

        ax1 = axs[0, 0]
        for name, values in cumulative_results.items():
            ax1.plot(
                range(1, n + 1),
                values,
                label=name,
                linewidth=2,
                color=strategy_colors[name],
            )
        ax1.set_xlabel("Этап переработки")
        ax1.set_ylabel("Накопленный выход сахара")
        ax1.set_title("Динамика накопленного выхода сахара")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2 = axs[0, 1]
        strategy_names = list(relative_losses.keys())
        strategy_values = [avg_results[name] for name in strategy_names]
        bars = ax2.bar(
            strategy_names,
            strategy_values,
            color=[strategy_colors[name] for name in strategy_names],
        )
        ax2.set_xlabel("Стратегия")
        ax2.set_ylabel("Средний выход сахара")
        ax2.set_title("Средний выход сахара для всех стратегий")
        ax2.set_xticks(range(len(strategy_names)))
        ax2.set_xticklabels(strategy_names, rotation=20, ha="right")
        for bar, value in zip(bars, strategy_values):
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontweight="bold",
            )

        ax3 = axs[1, 0]
        max_cumulative = cumulative_results["Максимальная"]
        for name, cum in cumulative_results.items():
            if name != "Максимальная":
                loss_percent = (max_cumulative - cum) / max_cumulative * 100
                ax3.plot(
                    range(1, n + 1),
                    loss_percent,
                    label=name,
                    linewidth=2,
                    color=strategy_colors[name],
                )
        ax3.set_xlabel("Этап переработки")
        ax3.set_ylabel("Отставание от максимальной (%)")
        ax3.set_title("Отставание стратегий от максимальной")
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        ax4 = axs[1, 1]

        heatmap_data = []
        heatmap_strategies = []

        for name in strategy_names:
            if name in cumulative_results:
                heatmap_data.append(cumulative_results[name])
                heatmap_strategies.append(name)

        if heatmap_data:
            heatmap_data = np.array(heatmap_data)

            if n > 50:
                step = max(1, n // 15)
                xticks = list(range(0, n, step))
                xticklabels = [str(i + 1) for i in range(0, n, step)]
            elif n > 30:
                step = max(1, n // 10)
                xticks = list(range(0, n, step))
                xticklabels = [str(i + 1) for i in range(0, n, step)]
            else:
                xticks = list(range(n))
                xticklabels = [str(i + 1) for i in range(n)]

            im = ax4.imshow(
                heatmap_data, aspect="auto", cmap="YlOrRd", interpolation="nearest"
            )

            ax4.set_xticks(xticks)
            ax4.set_xticklabels(xticklabels, fontsize=8)
            ax4.set_yticks(range(len(heatmap_strategies)))
            ax4.set_yticklabels(heatmap_strategies, fontsize=9)

            if n <= 30:
                for i in range(len(heatmap_strategies)):
                    for j in range(n):
                        if n <= 15 or (n > 15 and j % max(1, n // 10) == 0):
                            value = heatmap_data[i, j]
                            color = (
                                "white" if value > heatmap_data.max() * 0.5 else "black"
                            )
                            ax4.text(
                                j,
                                i,
                                f"{value:.2f}",
                                ha="center",
                                va="center",
                                color=color,
                                fontsize=7 if n <= 20 else 6,
                                fontweight="bold",
                            )

            cbar = plt.colorbar(im, ax=ax4, fraction=0.046, pad=0.04)
            cbar.set_label("Накопленный выход сахара", fontsize=9)

            ax4.set_xlabel(f"Этап переработки (всего {n} этапов)")
            ax4.set_title(f"Тепловая карта эффективности стратегий (n={n})")

            if n <= 50:
                ax4.set_xticks(np.arange(-0.5, n, 1), minor=True)
                ax4.set_yticks(np.arange(-0.5, len(heatmap_strategies), 1), minor=True)
                ax4.grid(
                    which="minor", color="gray", linestyle="-", linewidth=0.2, alpha=0.3
                )
                ax4.tick_params(which="minor", size=0)

        plt.tight_layout()
        self.current_figure = fig
        plt.show()
