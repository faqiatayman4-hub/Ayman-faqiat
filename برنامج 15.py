import sys
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("خطأ في المكتبات", f"المكتبات المطلوبة غير مثبتة بشكل صحيح:\n{e}\n\nيرجى فتح CMD وتثبيتها بالأمر:\npip install numpy matplotlib")
    sys.exit(1)

class ComprehensiveTransformationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامج تحويلات الاقترانات الاحترافي - المبرمج ايمن فقيات")
        
        window_width = 1500
        window_height = 1010
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        self.large_font = ("Arial", 16, "bold")
        self.med_font = ("Arial", 14, "bold")
        
        # التقسيم الرئيسي
        self.left_frame = tk.Frame(root, bg="white")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = tk.LabelFrame(root, text=" لوحة التحكم والخصائص ", font=self.large_font, fg="black")
        right_frame.pack(side="right", fill="y", padx=10, pady=10, ipadx=10)
        
        # اليسار: الرسم والرسام
        title_label = tk.Label(self.left_frame, text="دراسة تحويلات الاقترانات الرياضية والمستوى الديكارتي", font=self.med_font, fg="#2c3e50", bg="white")
        title_label.pack(pady=2)
        
        self.fig, self.ax = plt.subplots(figsize=(11.5, 8.4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)
        
        footer_label = tk.Label(self.left_frame, text="تصميم وتبرمج: المبرمج ايمن فقيات", font=self.med_font, fg="#7f8c8d", bg="white")
        footer_label.pack(pady=2)
        
        # اليمين: عناصر التحكم
        tk.Label(right_frame, text="اختر الاقتران الأساسي:", font=self.large_font, fg="#2980b9").pack(anchor="e", padx=5, pady=2)
        self.func_choices = [
            "بدون اقتران (مستوى فارغ)",
            "جذر س ( √س )",
            "الجذر التكعيبي لـ س ( ∛س )",
            "س تربيع ( س² )",
            "س تكعيب ( س³ )",
            "القيمة المطلقة لـ س ( |س| )",
            "الاقتران الخطي ( س )",
            "الاقتران الثابت ( الثابت ١ )"
        ]
        self.selected_func_var = tk.StringVar(value=self.func_choices[0])
        self.func_combo = ttk.Combobox(right_frame, values=self.func_choices, textvariable=self.selected_func_var, state="readonly", width=24, font=self.med_font)
        self.func_combo.pack(anchor="e", padx=5, pady=2)
        self.func_combo.bind("<<ComboboxSelected>>", lambda e: self.safe_update_plot())
        
        # --- تخصيص ألوان المحاور وحجم خط الأعداد ---
        axis_config_frame = ttk.LabelFrame(right_frame, text=" إعدادات المحاور والشبكة ")
        axis_config_frame.pack(fill="x", padx=5, pady=2)
        
        ac_row = tk.Frame(axis_config_frame)
        ac_row.pack(fill="x", padx=3, pady=2)
        tk.Label(ac_row, text="لون المحاور:", font=("Arial", 12)).pack(side="right", padx=2)
        self.axis_color_var = tk.StringVar(value="أسود")
        axis_colors = ["أسود", "أزرق", "أحمر", "أخضر", "رمادي"]
        axis_combo = ttk.Combobox(ac_row, values=axis_colors, textvariable=self.axis_color_var, state="readonly", width=8, font=("Arial", 11))
        axis_combo.pack(side="right", padx=2)
        axis_combo.bind("<<ComboboxSelected>>", lambda e: self.safe_update_plot())
        
        tk.Label(ac_row, text="حجم خط الأعداد:", font=("Arial", 12)).pack(side="right", padx=2)
        self.font_size_var = tk.IntVar(value=14)
        font_sizes = list(range(8, 19))
        font_combo = ttk.Combobox(ac_row, values=font_sizes, textvariable=self.font_size_var, state="readonly", width=4, font=("Arial", 11))
        font_combo.pack(side="right", padx=2)
        font_combo.bind("<<ComboboxSelected>>", lambda e: self.safe_update_plot())

        # --- مجال الدالة وتحديث مباشر لأشكال الأطراف ---
        domain_frame = ttk.LabelFrame(right_frame, text=" مجال الدالة وأشكال أطراف المنحنى ")
        domain_frame.pack(fill="x", padx=5, pady=2)
        
        # أشكال الأطراف المتنوعة
        self.end_choices = [
            "بدون", 
            "رأس سهم", 
            "سهم مزدوج", 
            "دائرة مغلقة", 
            "دائرة مفتوحة", 
            "مربع مغلق", 
            "معين"
        ]
        
        # الحد الأدنى
        d_min_row = tk.Frame(domain_frame)
        d_min_row.pack(fill="x", padx=3, pady=2)
        tk.Label(d_min_row, text="الحد الأدنى:", font=self.med_font).pack(side="right", padx=2)
        self.x_min_var = tk.DoubleVar(value=-10.0)
        tk.Entry(d_min_row, textvariable=self.x_min_var, width=5, font=self.med_font).pack(side="right", padx=2)
        
        tk.Label(d_min_row, text="طرفه:", font=("Arial", 12)).pack(side="right", padx=2)
        self.min_end_var = tk.StringVar(value=self.end_choices[0])
        min_combo = ttk.Combobox(d_min_row, values=self.end_choices, textvariable=self.min_end_var, state="readonly", width=12, font=("Arial", 11))
        min_combo.pack(side="right", padx=2)
        min_combo.bind("<<ComboboxSelected>>", lambda e: self.safe_update_plot())
        
        # الحد الأعلى
        d_max_row = tk.Frame(domain_frame)
        d_max_row.pack(fill="x", padx=3, pady=2)
        tk.Label(d_max_row, text="الحد الأعلى:", font=self.med_font).pack(side="right", padx=2)
        self.x_max_var = tk.DoubleVar(value=10.0)
        tk.Entry(d_max_row, textvariable=self.x_max_var, width=5, font=self.med_font).pack(side="right", padx=2)
        
        tk.Label(d_max_row, text="طرفه:", font=("Arial", 12)).pack(side="right", padx=2)
        self.max_end_var = tk.StringVar(value=self.end_choices[0])
        max_combo = ttk.Combobox(d_max_row, values=self.end_choices, textvariable=self.max_end_var, state="readonly", width=12, font=("Arial", 11))
        max_combo.pack(side="right", padx=2)
        max_combo.bind("<<ComboboxSelected>>", lambda e: self.safe_update_plot())

        # المعاملات والمنزلقات
        self.a_var = tk.DoubleVar(value=1.0)
        self.b_var = tk.DoubleVar(value=1.0)
        self.h_var = tk.DoubleVar(value=0.0)
        self.k_var = tk.DoubleVar(value=0.0)
        self.color_var = tk.StringVar(value="أحمر (#e74c3c)")
        
        self.create_slider(right_frame, "التمدد/الانعكاس الرأسي (أ):", self.a_var, -5.0, 5.0)
        self.create_slider(right_frame, "التمدد/الانعكاس الأفقي (ب):", self.b_var, -5.0, 5.0)
        self.create_slider(right_frame, "الإزاحة الأفقية (هـ):", self.h_var, -10.0, 10.0)
        self.create_slider(right_frame, "الإزاحة الرأسية (ك):", self.k_var, -10.0, 10.0)
        
        # --- تعيين النقاط (س، ص) ---
        point_frame = ttk.LabelFrame(right_frame, text=" تعيين نقاط (س، ص) ")
        point_frame.pack(fill="x", padx=5, pady=2)
        
        p_row = tk.Frame(point_frame)
        p_row.pack(fill="x", padx=3, pady=2)
        tk.Label(p_row, text="ص:", font=self.med_font).pack(side="right", padx=2)
        self.y_point_var = tk.DoubleVar(value=0.0)
        tk.Entry(p_row, textvariable=self.y_point_var, width=5, font=self.med_font).pack(side="right", padx=2)
        
        tk.Label(p_row, text="س:", font=self.med_font).pack(side="right", padx=2)
        self.x_point_var = tk.DoubleVar(value=0.0)
        tk.Entry(p_row, textvariable=self.x_point_var, width=5, font=self.med_font).pack(side="right", padx=2)
        
        p_row2 = tk.Frame(point_frame)
        p_row2.pack(fill="x", padx=3, pady=2)
        tk.Label(p_row2, text="اللون:", font=self.med_font).pack(side="right", padx=2)
        self.point_color_var = tk.StringVar(value="أسود")
        point_colors = ["أسود", "أحمر", "أزرق", "أخضر"]
        self.point_color_combo = ttk.Combobox(p_row2, values=point_colors, textvariable=self.point_color_var, state="readonly", width=8, font=self.med_font)
        self.point_color_combo.pack(side="right", padx=2)
        
        self.show_coords_var = tk.BooleanVar(value=False)
        tk.Checkbutton(point_frame, text="إظهار الإحداثيات بجانب النقطة", variable=self.show_coords_var, font=("Arial", 11)).pack(anchor="e", padx=3, pady=2)
        
        tk.Button(point_frame, text="📌 إضافة نقطة (×)", command=self.add_point, font=self.med_font, bg="#2980b9", fg="white").pack(fill="x", padx=3, pady=2)
        tk.Button(point_frame, text="🧹 مسح النقاط", command=self.clear_points, font=self.med_font, bg="#e67e22", fg="white").pack(fill="x", padx=3, pady=2)

        # خيارات الألوان والقلم الحر
        tk.Label(right_frame, text="لون المنحنى:", font=self.large_font).pack(anchor="e", padx=5, pady=2)
        color_choices = ["أحمر (#e74c3c)", "أزرق (#2980b9)", "أخضر (#27ae60)", "بنفسجي (#8e44ad)"]
        self.color_combo = ttk.Combobox(right_frame, values=color_choices, textvariable=self.color_var, state="readonly", width=18, font=self.med_font)
        self.color_combo.pack(anchor="e", padx=5, pady=2)
        self.color_combo.bind("<<ComboboxSelected>>", lambda e: self.safe_update_plot())
        
        self.draw_mode_var = tk.BooleanVar(value=False)
        self.draw_check = tk.Checkbutton(right_frame, text="✏️ تفعيل القلم الحر", variable=self.draw_mode_var, font=self.large_font)
        self.draw_check.pack(anchor="e", padx=5, pady=2)
        
        pen_colors = ["أحمر", "أسود", "أزرق", "أخضر"]
        self.pen_color_var = tk.StringVar(value="أحمر")
        self.pen_combo = ttk.Combobox(right_frame, values=pen_colors, textvariable=self.pen_color_var, state="readonly", width=10, font=self.med_font)
        self.pen_combo.pack(anchor="e", padx=5, pady=2)

        # الأزرار العامة
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(fill="x", padx=5, pady=4)
        
        tk.Button(btn_frame, text="🧹 مسح خط يدوي", command=self.erase_last_stroke, font=self.med_font, bg="#f39c12", fg="white").pack(fill="x", pady=2)
        tk.Button(btn_frame, text="🗑️ مسح الكل", command=self.clear_all_strokes, font=self.med_font, bg="#c0392b", fg="white").pack(fill="x", pady=2)
        tk.Button(btn_frame, text="💾 حفظ الرسمة", command=self.save_plot_image, font=self.med_font, bg="#27ae60", fg="white").pack(fill="x", pady=2)
        tk.Button(btn_frame, text="🔄 إعادة ضبط", command=self.reset_values, font=self.med_font, bg="#7f8c8d", fg="white").pack(fill="x", pady=2)

        # المتغيرات للقلم الحر والنقاط
        self.drawing = False
        self.user_strokes = []
        self.custom_points = []
        
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        self.safe_update_plot()

    def create_slider(self, parent, label_text, var, from_, to):
        tk.Label(parent, text=label_text, font=self.med_font).pack(anchor="e", padx=5, pady=1)
        slider = ttk.Scale(parent, from_=from_, to=to, variable=var, orient="horizontal", command=lambda e: self.safe_update_plot())
        slider.pack(fill="x", padx=5, pady=1)
        val_label = tk.Label(parent, textvariable=var, font=self.med_font, fg="#2980b9")
        val_label.pack(anchor="e", padx=5, pady=1)

    def add_point(self):
        try:
            x_val = self.x_point_var.get()
            y_val = self.y_point_var.get()
            color_map_name = {"أحمر": "red", "أسود": "black", "أزرق": "blue", "أخضر": "green"}
            p_color = color_map_name.get(self.point_color_var.get(), "black")
            self.custom_points.append({'x': x_val, 'y': y_val, 'color': p_color})
            self.safe_update_plot()
        except Exception as e:
            messagebox.showerror("خطأ", f"قيم الإحداثيات غير صحيحة: {e}")

    def clear_points(self):
        self.custom_points.clear()
        self.safe_update_plot()

    def reset_values(self):
        self.a_var.set(1.0)
        self.b_var.set(1.0)
        self.h_var.set(0.0)
        self.k_var.set(1.0)
        self.x_min_var.set(-10.0)
        self.x_max_var.set(10.0)
        self.user_strokes.clear()
        self.custom_points.clear()
        self.color_var.set("أحمر (#e74c3c)")
        self.safe_update_plot()

    def erase_last_stroke(self):
        if self.user_strokes:
            self.user_strokes.pop()
            self.safe_update_plot()

    def clear_all_strokes(self):
        self.user_strokes.clear()
        self.safe_update_plot()

    def save_plot_image(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")])
            if file_path:
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("تم الحفظ", f"تم حفظ صورة الرسم البياني بنجاح في:\n{file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ الصورة: {e}")

    def format_arabic_num(self, val):
        rounded = round(val, 1)
        if abs(rounded) < 1e-5:
            return "٠"
        if rounded.is_integer() or abs(rounded - int(rounded)) < 1e-5:
            num_str = str(int(rounded))
        else:
            num_str = f"{rounded:.1f}"
        indic_str = num_str.translate(str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫"))
        if val < 0:
            indic_str = indic_str.replace("-", "") + "-"
        return indic_str

    def to_arabic_indic_axis(self, value):
        val_int = int(value)
        if val_int == 0:
            return ""
        pos_str = str(abs(val_int)).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
        if val_int < 0:
            return pos_str + "-"
        return pos_str

    def evaluate_function(self, func_type, inner_vals):
        if func_type == "بدون اقتران (مستوى فارغ)":
            return None
        elif func_type == "جذر س ( √س )":
            y = np.full_like(inner_vals, np.nan, dtype=float)
            valid = inner_vals >= 0
            y[valid] = np.sqrt(inner_vals[valid])
            return y
        elif func_type == "الجذر التكعيبي لـ س ( ∛س )":
            return np.cbrt(inner_vals)
        elif func_type == "س تربيع ( س² )":
            return inner_vals ** 2
        elif func_type == "س تكعيب ( س³ )":
            return inner_vals ** 3
        elif func_type == "القيمة المطلقة لـ س ( |س| )":
            return np.abs(inner_vals)
        elif func_type == "الاقتران الخطي ( س )":
            return inner_vals
        elif func_type == "الاقتران الثابت ( الثابت ١ )":
            return np.ones_like(inner_vals)
        return inner_vals

    def on_press(self, event):
        if not self.draw_mode_var.get() or event.inaxes != self.ax:
            return
        self.drawing = True
        color_map_name = {"أحمر": "red", "أسود": "black", "أزرق": "blue", "أخضر": "green"}
        self.current_pen_color = color_map_name.get(self.pen_color_var.get(), "red")
        self.current_stroke = {'color': self.current_pen_color, 'x': [event.xdata], 'y': [event.ydata]}

    def on_motion(self, event):
        if not self.drawing or event.inaxes != self.ax:
            return
        self.current_stroke['x'].append(event.xdata)
        self.current_stroke['y'].append(event.ydata)
        self.safe_update_plot(redraw_strokes_only=True)

    def on_release(self, event):
        if self.drawing:
            self.drawing = False
            if len(self.current_stroke['x']) > 1:
                self.user_strokes.append(self.current_stroke)
            self.current_stroke = []
            self.safe_update_plot()

    def safe_update_plot(self, redraw_strokes_only=False):
        try:
            self.update_plot(redraw_strokes_only)
        except Exception as e:
            err_msg = traceback.format_exc()
            messagebox.showerror("خطأ في الرسم", f"حدث خطأ أثناء تحديث الرسم البياني:\n{err_msg}")

    def update_plot(self, redraw_strokes_only=False):
        if not redraw_strokes_only:
            a = self.a_var.get()
            b = self.b_var.get()
            h = self.h_var.get()
            k = self.k_var.get()
            selected_func = self.selected_func_var.get()
            min_style = self.min_end_var.get()
            max_style = self.max_end_var.get()
            
            # قراءة لون المحاور وحجم خط الأعداد
            axis_color_map = {"أسود": "black", "أزرق": "#2980b9", "أحمر": "#c0392b", "أخضر": "#27ae60", "رمادي": "#7f8c8d"}
            chosen_axis_color = axis_color_map.get(self.axis_color_var.get(), "black")
            chosen_font_size = self.font_size_var.get()
            
            try:
                x_min = self.x_min_var.get()
                x_max = self.x_max_var.get()
            except:
                x_min, x_max = -10.0, 10.0
            
            self.ax.clear()
            self.ax.set_facecolor('white')
            self.fig.patch.set_facecolor('white')
            
            x = np.linspace(x_min, x_max, 1000)
            
            if selected_func != "بدون اقتران (مستوى فارغ)":
                y_orig = self.evaluate_function(selected_func, x)
                inner = b * (x - h)
                base_transformed = self.evaluate_function(selected_func, inner)
                y = a * base_transformed + k
                
                symbols_map = {
                    "جذر س ( √س )": ("√", "س"),
                    "الجذر التكعيبي لـ س ( ∛س )": ("∛", "س"),
                    "س تربيع ( س² )": ("(..)²", "س"),
                    "س تكعيب ( س³ )": ("(..)³", "س"),
                    "القيمة المطلقة لـ س ( |س| )": ("|...|", "س"),
                    "الاقتران الخطي ( س )": ("", "س"),
                    "الاقتران الثابت ( الثابت ١ )": ("", "١")
                }
                sym, var_name = symbols_map.get(selected_func, ("√", "س"))
                
                color_map = {
                    "أحمر (#e74c3c)": "#e74c3c",
                    "أزرق (#2980b9)": "#2980b9",
                    "أخضر (#27ae60)": "#27ae60",
                    "بنفسجي (#8e44ad)": "#8e44ad"
                }
                curve_color = color_map.get(self.color_var.get(), "#e74c3c")
                
                orig_label_map = {
                    "جذر س ( √س )": "ق(س) = √س",
                    "الجذر التكعيبي لـ س ( ∛س )": "ق(س) = ∛س",
                    "س تربيع ( س² )": "ق(س) = س²",
                    "س تكعيب ( س³ )": "ق(س) = س³",
                    "القيمة المطلقة لـ س ( |س| )": "ق(س) = |س|",
                    "الاقتران الخطي ( س )": "ق(س) = س",
                    "الاقتران الثابت ( الثابت ١ )": "ق(س) = ١"
                }
                if y_orig is not None:
                    self.ax.plot(x, y_orig, label=orig_label_map.get(selected_func, ""), color="gray", linestyle="--", alpha=0.5, linewidth=1.5)
                
                a_s = self.format_arabic_num(a)
                b_s = self.format_arabic_num(b)
                h_s = self.format_arabic_num(h)
                k_s = self.format_arabic_num(k)
                
                if selected_func in ["جذر س ( √س )", "الجذر التكعيبي لـ س ( ∛س )"]:
                    eq_str = f"ق(س) = {a_s} × {sym}( {b_s}({var_name} - {h_s}) ) + {k_s}"
                elif selected_func in ["س تربيع ( س² )"]:
                    eq_str = f"ق(س) = {a_s} × ( {b_s}({var_name} - {h_s}) )² + {k_s}"
                elif selected_func in ["س تكعيب ( س³ )"]:
                    eq_str = f"ق(س) = {a_s} × ( {b_s}({var_name} - {h_s}) )³ + {k_s}"
                elif selected_func in ["القيمة المطلقة لـ س ( |س| )"]:
                    eq_str = f"ق(س) = {a_s} × | {b_s}({var_name} - {h_s}) | + {k_s}"
                elif selected_func in ["الاقتران الخطي ( س )"]:
                    eq_str = f"ق(س) = {a_s} × ( {b_s}({var_name} - {h_s}) ) + {k_s}"
                else:
                    eq_str = f"ق(س) = {a_s} × (١) + {k_s}"
                    
                if y is not None:
                    valid_idx = ~np.isnan(y)
                    if np.any(valid_idx):
                        self.ax.plot(x[valid_idx], y[valid_idx], label=eq_str, color=curve_color, linewidth=2.8)
                        xv, yv = x[valid_idx], y[valid_idx]
                        if len(xv) > 0:
                            x_start, y_start = xv[0], yv[0]
                            x_end, y_end = xv[-1], yv[-1]
                            
                            def draw_curve_end(x_pos, y_pos, style, is_end=True):
                                if style == "رأس سهم":
                                    m = '>' if is_end else '<'
                                    self.ax.plot(x_pos, y_pos, marker=m, color=curve_color, markersize=9, markeredgewidth=2)
                                elif style == "سهم مزدوج":
                                    m = 'x' if is_end else '+'
                                    self.ax.plot(x_pos, y_pos, marker=m, color=curve_color, markersize=8, markeredgewidth=2)
                                elif style == "دائرة مغلقة":
                                    self.ax.plot(x_pos, y_pos, marker='o', color=curve_color, markersize=8, markerfacecolor=curve_color)
                                elif style == "دائرة مفتوحة":
                                    self.ax.plot(x_pos, y_pos, marker='o', color=curve_color, markersize=8, markerfacecolor='white', markeredgewidth=2)
                                elif style == "مربع مغلق":
                                    self.ax.plot(x_pos, y_pos, marker='s', color=curve_color, markersize=8, markerfacecolor=curve_color)
                                elif style == "معين":
                                    self.ax.plot(x_pos, y_pos, marker='d', color=curve_color, markersize=8, markerfacecolor=curve_color)

                            draw_curve_end(x_start, y_start, min_style, is_end=False)
                            draw_curve_end(x_end, y_end, max_style, is_end=True)
                                
                self.ax.legend(loc="upper left", fontsize=11)
            
            # تكبير نطاق المستوى الديكارتي لأقصى حد ومربعات شبكة أوسع
            self.ax.set_xlim(-14.0, 14.0)
            self.ax.set_ylim(-14.0, 14.0)
            self.ax.set_aspect('equal', adjustable='box')
            
            self.ax.spines['left'].set_position(('data', 0))
            self.ax.spines['bottom'].set_position(('data', 0))
            self.ax.spines['right'].set_color('none')
            self.ax.spines['top'].set_color('none')
            
            self.ax.spines['left'].set_color(chosen_axis_color)
            self.ax.spines['left'].set_linewidth(2)
            self.ax.spines['bottom'].set_color(chosen_axis_color)
            self.ax.spines['bottom'].set_linewidth(2)
            
            # كتابة (س) يمين محور السينات و (ص) أعلى محور الصادات بالألوان المختارة
            self.ax.text(13.2, -0.8, "س", fontsize=16, fontweight="bold", color=chosen_axis_color)
            self.ax.text(0.5, 13.2, "ص", fontsize=16, fontweight="bold", color=chosen_axis_color)
            
            # رؤوس أسهم المحاور ثابتة
            self.ax.annotate('', xy=(0, 13.2), xytext=(0, 12.0), arrowprops=dict(arrowstyle="->", lw=3.0, color=chosen_axis_color, mutation_scale=25))
            self.ax.annotate('', xy=(13.2, 0), xytext=(12.0, 0), arrowprops=dict(arrowstyle="->", lw=3.0, color=chosen_axis_color, mutation_scale=25))
            self.ax.annotate('', xy=(-13.2, 0), xytext=(-12.0, 0), arrowprops=dict(arrowstyle="->", lw=3.0, color=chosen_axis_color, mutation_scale=25))
            self.ax.annotate('', xy=(0, -13.2), xytext=(0, -12.0), arrowprops=dict(arrowstyle="->", lw=3.0, color=chosen_axis_color, mutation_scale=25))

            ticks = np.arange(-10, 11, 1)
            self.ax.set_xticks(ticks)
            self.ax.set_yticks(ticks)
            
            xtick_labels = [self.to_arabic_indic_axis(t) for t in ticks]
            ytick_labels = [self.to_arabic_indic_axis(t) for t in ticks]
            
            # حجم خط أعداد المحاور اختياري من القائمة
            self.ax.set_xticklabels(xtick_labels, fontsize=chosen_font_size, fontweight="bold")
            self.ax.set_yticklabels(ytick_labels, fontsize=chosen_font_size, fontweight="bold")
            
            # شبكة مربعات واسعة وواضحة جداً
            self.ax.grid(True, which='both', color='#5499c7', linestyle='-', linewidth=1.2, alpha=0.6)
            self.ax.set_title("المستوى الديكارتي واسع المدى وتحويلات الاقترانات", fontsize=14, fontweight="bold", pad=15)

        # رسم النقاط المحددة
        for p in self.custom_points:
            px, py, p_color = p['x'], p['y'], p['color']
            self.ax.plot(px, py, marker='x', color=p_color, markersize=10, markeredgewidth=3)
            if self.show_coords_var.get():
                self.ax.text(px + 0.3, py + 0.3, f"({self.format_arabic_num(px)}, {self.format_arabic_num(py)})", fontsize=11, fontweight="bold", color=p_color)

        # رسم اليدوي الحر
        for stroke in self.user_strokes:
            self.ax.plot(stroke['x'], stroke['y'], color=stroke['color'], linewidth=3, alpha=0.9)
            
        if self.drawing and self.current_stroke:
            self.ax.plot(self.current_stroke['x'], self.current_stroke['y'], color=self.current_stroke['color'], linewidth=3, alpha=0.9)
            
        self.canvas.draw()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ComprehensiveTransformationApp(root)
        root.mainloop()
    except Exception as e:
        err_msg = traceback.format_exc()
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("خطأ فادح في التشغيل", f"حدث خطأ أدى لتوقف البرنامج:\n{err_msg}")
        except:
            print(err_msg)
