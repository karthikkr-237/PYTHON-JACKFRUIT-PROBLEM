import wx
import wx.grid
import wx.lib.scrolledpanel as scrolled
import wx.adv
import csv
import math
from datetime import datetime
from collections import defaultdict
import io

try:
    import matplotlib
    matplotlib.use('WXAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class BMICalculator(wx.Frame):
    def __init__(self):
        super().__init__(None, title="BMI Health Assistant", size=(1280, 720))
        self.SetMinSize(wx.Size(1024, 576))
        
        self.dark_mode = False
        self.history = []
        self.person_history = defaultdict(list)
        self.is_metric = True  # Track current unit system
        
        self.SetIcon(self.create_icon())
        self.init_ui()
        self.apply_theme()
        
    def create_icon(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(self.create_bitmap_icon())
        return icon
    
    def create_bitmap_icon(self):
        bmp = wx.Bitmap(32, 32)
        dc = wx.MemoryDC(bmp)
        dc.SetBackground(wx.Brush(wx.Colour(70, 130, 180)))
        dc.Clear()
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        dc.SetPen(wx.Pen(wx.Colour(255, 255, 255), 2))
        dc.DrawLine(16, 8, 16, 24)
        dc.DrawLine(8, 24, 24, 24)
        dc.DrawLine(8, 24, 12, 28)
        dc.DrawLine(24, 24, 20, 28)
        dc.SelectObject(wx.NullBitmap)
        return bmp
    
    def init_ui(self):
        menubar = wx.MenuBar()
        
        file_menu = wx.Menu()
        export_csv = file_menu.Append(wx.ID_SAVE, "&Export to CSV\tCtrl+S", "Export history to CSV")
        export_pdf = file_menu.Append(wx.ID_SAVEAS, "&Export to PDF\tCtrl+P", "Export history to PDF")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "&Exit\tCtrl+Q", "Exit application")
        
        view_menu = wx.Menu()
        self.dark_mode_item = view_menu.Append(wx.ID_ANY, "&Dark Mode\tCtrl+D", "Toggle dark mode", kind=wx.ITEM_CHECK)
        
        help_menu = wx.Menu()
        tips_item = help_menu.Append(wx.ID_HELP, "&Health Tips", "Show detailed health tips")
        about_item = help_menu.Append(wx.ID_ABOUT, "&About", "About BMI Calculator")
        
        menubar.Append(file_menu, "&File")
        menubar.Append(view_menu, "&View")
        menubar.Append(help_menu, "&Help")
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.on_export_csv, export_csv)
        self.Bind(wx.EVT_MENU, self.on_export_pdf, export_pdf)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.toggle_dark_mode, self.dark_mode_item)
        self.Bind(wx.EVT_MENU, self.show_health_tips, tips_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # --- LEFT PANEL ---
        left_panel = wx.Panel(main_panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        input_box = wx.StaticBox(left_panel, label="Personal Information")
        input_sizer = wx.StaticBoxSizer(input_box, wx.VERTICAL)
        
        # Unit Selection
        unit_sizer = wx.BoxSizer(wx.HORIZONTAL)
        unit_sizer.Add(wx.StaticText(left_panel, label="Units:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.unit_choice = wx.RadioBox(left_panel, choices=["Metric (kg/cm)", "Imperial (lbs/ft/in)"], 
                                      style=wx.RA_SPECIFY_ROWS)
        self.unit_choice.Bind(wx.EVT_RADIOBOX, self.on_unit_change)
        unit_sizer.Add(self.unit_choice, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(unit_sizer, 0, wx.EXPAND)

        # Name
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_sizer.Add(wx.StaticText(left_panel, label="Full Name:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.name_ctrl = wx.TextCtrl(left_panel, style=wx.TE_PROCESS_ENTER)
        name_sizer.Add(self.name_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(name_sizer, 0, wx.EXPAND)
        
        # Age and Gender
        age_gender_sizer = wx.BoxSizer(wx.HORIZONTAL)
        age_sizer = wx.BoxSizer(wx.HORIZONTAL)
        age_sizer.Add(wx.StaticText(left_panel, label="Age:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.age_ctrl = wx.SpinCtrl(left_panel, min=1, max=120)
        self.age_ctrl.SetValue("")
        age_sizer.Add(self.age_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        age_gender_sizer.Add(age_sizer, 1, wx.EXPAND)
        
        gender_sizer = wx.BoxSizer(wx.HORIZONTAL)
        gender_sizer.Add(wx.StaticText(left_panel, label="Gender:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.gender_choice = wx.Choice(left_panel, choices=["Select Gender", "Male", "Female", "Other"])
        self.gender_choice.SetSelection(0)
        gender_sizer.Add(self.gender_choice, 1, wx.EXPAND | wx.ALL, 5)
        age_gender_sizer.Add(gender_sizer, 1, wx.EXPAND)
        input_sizer.Add(age_gender_sizer, 0, wx.EXPAND)
        
        # Activity
        activity_sizer = wx.BoxSizer(wx.HORIZONTAL)
        activity_sizer.Add(wx.StaticText(left_panel, label="Activity Level:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.activity_choice = wx.Choice(left_panel, choices=[
            "Select Activity Level",
            "Sedentary (little or no exercise)",
            "Lightly Active (light exercise 1-3 days/week)",
            "Moderately Active (moderate exercise 3-5 days/week)",
            "Very Active (hard exercise 6-7 days/week)",
            "Extra Active (very hard exercise & physical job)"
        ])
        self.activity_choice.SetSelection(0)
        activity_sizer.Add(self.activity_choice, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(activity_sizer, 0, wx.EXPAND)
        
        # --- HEIGHT INPUT (Metric vs Imperial) ---
        height_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.height_label = wx.StaticText(left_panel, label="Height (cm):")
        height_sizer.Add(self.height_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        # Metric Height Control
        self.height_cm_ctrl = wx.SpinCtrlDouble(left_panel, min=50, max=250, inc=0.1)
        self.height_cm_ctrl.SetDigits(1)
        self.height_cm_ctrl.SetValue("")
        height_sizer.Add(self.height_cm_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        # Imperial Height Controls (Feet & Inches) - Hidden by default
        self.height_ft_ctrl = wx.SpinCtrl(left_panel, min=1, max=8)
        self.height_ft_ctrl.SetValue("")
        self.height_ft_label = wx.StaticText(left_panel, label="ft")
        
        self.height_in_ctrl = wx.SpinCtrlDouble(left_panel, min=0, max=11.9, inc=0.5)
        self.height_in_ctrl.SetDigits(1)
        self.height_in_ctrl.SetValue("")
        self.height_in_label = wx.StaticText(left_panel, label="in")

        height_sizer.Add(self.height_ft_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        height_sizer.Add(self.height_ft_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        height_sizer.Add(self.height_in_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        height_sizer.Add(self.height_in_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        
        input_sizer.Add(height_sizer, 0, wx.EXPAND)
        
        # --- WEIGHT INPUT ---
        weight_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.weight_label = wx.StaticText(left_panel, label="Weight (kg):")
        weight_sizer.Add(self.weight_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.weight_ctrl = wx.SpinCtrlDouble(left_panel, min=10, max=300, inc=0.1)
        self.weight_ctrl.SetDigits(1)
        self.weight_ctrl.SetValue("")
        weight_sizer.Add(self.weight_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(weight_sizer, 0, wx.EXPAND)
        
        left_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Buttons
        button_panel = wx.Panel(left_panel)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.calculate_btn = wx.Button(button_panel, label="Calculate BMI")
        self.calculate_btn.Bind(wx.EVT_BUTTON, self.on_calculate)
        button_sizer.Add(self.calculate_btn, 1, wx.EXPAND | wx.RIGHT, 5)
        self.reset_btn = wx.Button(button_panel, label="Reset All")
        self.reset_btn.Bind(wx.EVT_BUTTON, self.on_reset)
        button_sizer.Add(self.reset_btn, 1, wx.EXPAND)
        button_panel.SetSizer(button_sizer)
        left_sizer.Add(button_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # Results
        results_box = wx.StaticBox(left_panel, label="BMI Results")
        results_sizer = wx.StaticBoxSizer(results_box, wx.VERTICAL)
        results_grid = wx.GridBagSizer(5, 5)
        self.bmi_result = wx.StaticText(left_panel, label="--")
        self.bmi_result.SetFont(wx.Font(28, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        results_grid.Add(self.bmi_result, pos=(0, 0), span=(1, 2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.category_result = wx.StaticText(left_panel, label="Category: --")
        self.category_result.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        results_grid.Add(self.category_result, pos=(1, 0), span=(1, 2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.ideal_weight_label = wx.StaticText(left_panel, label="Ideal Weight Range: --")
        self.ideal_weight_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        results_grid.Add(self.ideal_weight_label, pos=(2, 0), span=(1, 2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        results_sizer.Add(results_grid, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        left_sizer.Add(results_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # Tips
        tips_box = wx.StaticBox(left_panel, label="Health Tips & Recommendations")
        tips_sizer = wx.StaticBoxSizer(tips_box, wx.VERTICAL)
        self.tips_panel = scrolled.ScrolledPanel(left_panel, size=(-1, 250))
        self.tips_panel.SetupScrolling(scroll_x=False, scroll_y=True)
        tips_content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.tips_text = wx.StaticText(self.tips_panel, label="Enter your information to see personalized health tips.")
        self.tips_text.Wrap(380)
        tips_content_sizer.Add(self.tips_text, 0, wx.EXPAND | wx.ALL, 10)
        self.tips_panel.SetSizer(tips_content_sizer)
        tips_sizer.Add(self.tips_panel, 1, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(tips_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        left_panel.SetSizer(left_sizer)
        
        # --- RIGHT PANEL (Charts/History) ---
        right_panel = wx.Panel(main_panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        person_box = wx.StaticBox(right_panel, label="Select Person for Charts")
        person_sizer = wx.StaticBoxSizer(person_box, wx.HORIZONTAL)
        person_sizer.Add(wx.StaticText(right_panel, label="Person:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.person_choice = wx.Choice(right_panel, choices=["All Persons"])
        self.person_choice.SetSelection(0)
        self.person_choice.Bind(wx.EVT_CHOICE, self.on_person_selected)
        person_sizer.Add(self.person_choice, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(person_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        if MATPLOTLIB_AVAILABLE:
            chart_box = wx.StaticBox(right_panel, label="Personal BMI Trend")
            chart_sizer = wx.StaticBoxSizer(chart_box, wx.VERTICAL)
            self.figure = Figure(figsize=(10, 4))
            self.axes = self.figure.add_subplot(111)
            self.canvas = FigureCanvas(right_panel, -1, self.figure)
            chart_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
            right_sizer.Add(chart_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        else:
            no_chart_label = wx.StaticText(right_panel, label="Install matplotlib for charts")
            right_sizer.Add(no_chart_label, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        
        history_box = wx.StaticBox(right_panel, label="Calculation History (Stored in Metric)")
        history_sizer = wx.StaticBoxSizer(history_box, wx.VERTICAL)
        self.history_grid = wx.grid.Grid(right_panel)
        self.history_grid.CreateGrid(0, 7)
        self.history_grid.SetColLabelValue(0, "Date")
        self.history_grid.SetColLabelValue(1, "Name")
        self.history_grid.SetColLabelValue(2, "Age")
        self.history_grid.SetColLabelValue(3, "Gender")
        self.history_grid.SetColLabelValue(4, "Activity")
        self.history_grid.SetColLabelValue(5, "BMI")
        self.history_grid.SetColLabelValue(6, "Category")
        self.history_grid.AutoSizeColumns()
        history_sizer.Add(self.history_grid, 1, wx.EXPAND | wx.ALL, 5)
        
        history_btn_panel = wx.Panel(right_panel)
        history_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        clear_btn = wx.Button(history_btn_panel, label="Clear History")
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear_history)
        history_btn_sizer.Add(clear_btn, 0, wx.RIGHT, 5)
        export_btn = wx.Button(history_btn_panel, label="Export History")
        export_btn.Bind(wx.EVT_BUTTON, self.on_export_csv)
        history_btn_sizer.Add(export_btn, 0)
        history_btn_panel.SetSizer(history_btn_sizer)
        history_sizer.Add(history_btn_panel, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        right_sizer.Add(history_sizer, 1, wx.EXPAND | wx.ALL, 10)
        right_panel.SetSizer(right_sizer)
        
        main_sizer.Add(left_panel, 4, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(right_panel, 6, wx.EXPAND | wx.ALL, 5)
        main_panel.SetSizer(main_sizer)
        
        self.CreateStatusBar()
        self.SetStatusText("Enter your personal information and click Calculate BMI")
        
        # Initialize visibility based on default metric selection
        self.update_unit_ui()
        
        if MATPLOTLIB_AVAILABLE:
            self.update_chart()

    def on_unit_change(self, event):
        """Handle unit system switch"""
        self.is_metric = (self.unit_choice.GetSelection() == 0)
        self.update_unit_ui()
        self.Layout()
        
    def update_unit_ui(self):
        """Show/Hide controls based on selected unit system"""
        if self.is_metric:
            # Show Metric controls
            self.height_label.SetLabel("Height (cm):")
            self.height_cm_ctrl.Show()
            self.height_ft_ctrl.Hide()
            self.height_ft_label.Hide()
            self.height_in_ctrl.Hide()
            self.height_in_label.Hide()
            
            self.weight_label.SetLabel("Weight (kg):")
            self.weight_ctrl.SetRange(10, 300)
        else:
            # Show Imperial controls
            self.height_label.SetLabel("Height:")
            self.height_cm_ctrl.Hide()
            self.height_ft_ctrl.Show()
            self.height_ft_label.Show()
            self.height_in_ctrl.Show()
            self.height_in_label.Show()
            
            self.weight_label.SetLabel("Weight (lbs):")
            self.weight_ctrl.SetRange(20, 660) # Approx 300kg in lbs
            
    def on_calculate(self, event):
        """Calculate BMI and update results"""
        try:
            # Get input values
            name = self.name_ctrl.GetValue().strip()
            age_str = self.age_ctrl.GetValue()
            gender = self.gender_choice.GetStringSelection()
            activity = self.activity_choice.GetStringSelection()
            
            # --- VALIDATION ---
            if not name:
                self.name_ctrl.SetFocus()
                raise ValueError("Please enter your name.")
            if not age_str:
                self.age_ctrl.SetFocus()
                raise ValueError("Please enter your age.")
            if gender == "Select Gender":
                self.gender_choice.SetFocus()
                raise ValueError("Please select your gender.")
            if activity == "Select Activity Level":
                self.activity_choice.SetFocus()
                raise ValueError("Please select your activity level.")

            # --- CONVERSION AND CALCULATION ---
            height_m = 0.0
            weight_kg = 0.0
            
            if self.is_metric:
                # Metric Input
                height_cm = self.height_cm_ctrl.GetValue()
                weight_val = self.weight_ctrl.GetValue()
                
                if height_cm < 50: raise ValueError("Height must be at least 50cm")
                if weight_val < 10: raise ValueError("Weight must be at least 10kg")
                
                height_m = height_cm / 100.0
                weight_kg = weight_val
                
            else:
                # Imperial Input
                ft = self.height_ft_ctrl.GetValue()
                inches = self.height_in_ctrl.GetValue()
                weight_lbs = self.weight_ctrl.GetValue()
                
                total_inches = (ft * 12) + inches
                if total_inches < 20: raise ValueError("Height too low")
                if weight_lbs < 20: raise ValueError("Weight must be at least 20lbs")
                
                # Convert to Metric for consistent history storage and calculation
                height_m = total_inches * 0.0254
                weight_kg = weight_lbs * 0.453592
            
            age = int(age_str)
            
            # Calculate BMI (Standard Formula: kg / m^2)
            bmi = weight_kg / (height_m * height_m)
            
            # Determine category
            category = self.get_bmi_category(bmi, age)
            
            # Calculate ideal weight range (Metric)
            ideal_min_kg = 18.5 * (height_m * height_m)
            ideal_max_kg = 24.9 * (height_m * height_m)
            
            # Update results UI
            self.bmi_result.SetLabel(f"{bmi:.1f}")
            self.bmi_result.SetForegroundColour(self.get_bmi_color(bmi))
            self.category_result.SetLabel(f"Category: {category}")
            
            # Display ideal weight in user's preferred unit
            if self.is_metric:
                self.ideal_weight_label.SetLabel(f"Ideal Weight Range: {ideal_min_kg:.1f} - {ideal_max_kg:.1f} kg")
            else:
                ideal_min_lbs = ideal_min_kg * 2.20462
                ideal_max_lbs = ideal_max_kg * 2.20462
                self.ideal_weight_label.SetLabel(f"Ideal Weight Range: {ideal_min_lbs:.1f} - {ideal_max_lbs:.1f} lbs")
            
            # Generate personalized tips
            tips = self.get_personalized_tips(bmi, category, age, gender, activity, weight_kg, height_m * 100)
            self.update_tips_display(tips)
            
            # Add to history (Storing as Metric for consistency in database/charts)
            history_entry = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'name': name,
                'age': age,
                'gender': gender,
                'activity': activity,
                'bmi': round(bmi, 1),
                'category': category,
                'height': round(height_m * 100, 1), # stored as cm
                'weight': round(weight_kg, 1)       # stored as kg
            }
            
            self.history.append(history_entry)
            self.person_history[name].append(history_entry)
            
            self.update_person_list()
            self.update_history_grid()
            self.update_chart()
            
            self.SetStatusText(f"BMI calculated: {bmi:.1f} ({category}) for {name}")
            
        except ValueError as e:
            wx.MessageBox(str(e), "Input Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Error calculating BMI: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def get_bmi_color(self, bmi):
        if bmi < 18.5: return wx.Colour(0, 0, 255)
        elif bmi < 25: return wx.Colour(0, 128, 0)
        elif bmi < 30: return wx.Colour(255, 165, 0)
        else: return wx.Colour(255, 0, 0)

    def get_bmi_category(self, bmi, age):
        if age >= 18:
            if bmi < 16: return "Severely Underweight"
            elif bmi < 18.5: return "Underweight"
            elif bmi < 25: return "Normal Weight"
            elif bmi < 30: return "Overweight"
            elif bmi < 35: return "Obesity Class I"
            elif bmi < 40: return "Obesity Class II"
            else: return "Obesity Class III"
        else:
            if bmi < 5: return "Underweight (Child)"
            elif bmi < 85: return "Healthy Weight (Child)"
            elif bmi < 95: return "Overweight (Child)"
            else: return "Obese (Child)"

    def get_personalized_tips(self, bmi, category, age, gender, activity, weight, height):
        tips = []
        if "Underweight" in category:
            tips.append("📈 **Weight Gain Tips:**\n• Eat 5-6 small meals\n• Add healthy fats & protein\n• Strength train")
        elif "Normal" in category:
            tips.append("✅ **Maintenance:**\n• Maintain balanced diet\n• Regular exercise\n• Hydration")
        elif "Overweight" in category or "Obese" in category:
            tips.append("📉 **Weight Loss Tips:**\n• Caloric deficit\n• Increase veggies & fiber\n• Cardio & weights")
        
        tips.append("\n💡 **General:**\n• Drink water\n• Sleep 7-9 hours\n• Manage stress")
        return "\n".join(tips)

    def update_tips_display(self, tips):
        self.tips_panel.DestroyChildren()
        tips_content_sizer = wx.BoxSizer(wx.VERTICAL)
        tips_text = wx.TextCtrl(self.tips_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        tips_text.SetValue(tips)
        tips_content_sizer.Add(tips_text, 1, wx.EXPAND | wx.ALL, 10)
        self.tips_panel.SetSizer(tips_content_sizer)
        self.tips_panel.SetupScrolling(scroll_x=False, scroll_y=True)
        self.tips_panel.Layout()

    def update_person_list(self):
        persons = ["All Persons"] + sorted(list(self.person_history.keys()))
        self.person_choice.SetItems(persons)
        self.person_choice.SetSelection(0)

    def on_person_selected(self, event):
        self.update_chart()

    def update_history_grid(self):
        self.history_grid.ClearGrid()
        if self.history_grid.GetNumberRows() > 0:
            self.history_grid.DeleteRows(0, self.history_grid.GetNumberRows())
        
        for i, entry in enumerate(self.history[-50:]):
            self.history_grid.AppendRows(1)
            self.history_grid.SetCellValue(i, 0, entry['date'])
            self.history_grid.SetCellValue(i, 1, entry['name'])
            self.history_grid.SetCellValue(i, 2, str(entry['age']))
            self.history_grid.SetCellValue(i, 3, entry['gender'])
            self.history_grid.SetCellValue(i, 4, entry['activity'].split('(')[0].strip())
            self.history_grid.SetCellValue(i, 5, str(entry['bmi']))
            self.history_grid.SetCellValue(i, 6, entry['category'])
            
            bmi = entry['bmi']
            color = wx.Colour(144, 238, 144) if bmi < 25 and bmi >= 18.5 else wx.Colour(255, 165, 0)
            if bmi < 18.5: color = wx.Colour(135, 206, 250)
            if bmi >= 30: color = wx.Colour(255, 0, 0)
            
            self.history_grid.SetCellBackgroundColour(i, 6, color)
            self.history_grid.SetCellTextColour(i, 6, wx.BLACK if bmi < 30 else wx.WHITE)
        self.history_grid.AutoSizeColumns()

    def update_chart(self):
        if not MATPLOTLIB_AVAILABLE: return
        self.axes.clear()
        selected_person = self.person_choice.GetStringSelection()
        
        if selected_person == "All Persons" or selected_person not in self.person_history:
            data_to_plot = self.history
            title = "BMI Trend - All Persons"
        else:
            data_to_plot = self.person_history[selected_person]
            title = f"BMI Trend - {selected_person}"
        
        if len(data_to_plot) < 1:
            self.axes.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center')
        else:
            dates = [datetime.strptime(entry['date'], "%Y-%m-%d %H:%M") for entry in data_to_plot]
            bmis = [entry['bmi'] for entry in data_to_plot]
            
            self.axes.plot(dates, bmis, 'o-', linewidth=2, markersize=6)
            self.axes.axhspan(18.5, 25, alpha=0.1, color='green', label='Normal')
            self.axes.axhspan(25, 30, alpha=0.1, color='yellow', label='Overweight')
            self.axes.axhspan(30, 50, alpha=0.1, color='red', label='Obese')
            self.axes.set_title(title)
            self.figure.autofmt_xdate()
        self.canvas.draw()

    def on_reset(self, event):
        self.name_ctrl.Clear()
        self.age_ctrl.SetValue("")
        self.gender_choice.SetSelection(0)
        self.activity_choice.SetSelection(0)
        self.height_cm_ctrl.SetValue("")
        self.height_ft_ctrl.SetValue("")
        self.height_in_ctrl.SetValue("")
        self.weight_ctrl.SetValue("")
        self.bmi_result.SetLabel("--")
        self.category_result.SetLabel("Category: --")
        self.ideal_weight_label.SetLabel("Ideal Weight Range: --")
        self.update_tips_display("Enter your information to see personalized health tips.")

    def on_export_csv(self, event):
        if not self.history:
            wx.MessageBox("No data to export.", "Export", wx.OK | wx.ICON_WARNING)
            return
        with wx.FileDialog(self, "Save CSV file", wildcard="CSV files (*.csv)|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL: return
            try:
                with open(dialog.GetPath(), 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['date', 'name', 'age', 'gender', 'activity', 'height_cm', 'weight_kg', 'bmi', 'category']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for entry in self.history:
                        writer.writerow({k: entry[k] for k in fieldnames if k in entry})
                wx.MessageBox("Export Successful", "Success", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(str(e), "Export Error", wx.OK | wx.ICON_ERROR)

    def on_export_pdf(self, event):
        self.on_export_csv(event) # Reusing CSV logic for simplicity in this example

    def on_clear_history(self, event):
        if wx.MessageBox("Clear history?", "Confirm", wx.YES_NO) == wx.YES:
            self.history.clear()
            self.person_history.clear()
            self.update_history_grid()
            self.update_person_list()
            if MATPLOTLIB_AVAILABLE: self.update_chart()

    def show_health_tips(self, event):
        wx.MessageBox("Detailed health tips are available in the main window after calculation.", "Health Tips")

    def toggle_dark_mode(self, event):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            bg_color = wx.Colour(75, 75, 75)
            fg_color = wx.Colour(250, 250, 250)
        else:
            bg_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            fg_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        self.SetBackgroundColour(bg_color)
        self.SetForegroundColour(fg_color)
        self.Refresh()

    def on_about(self, event):
        """Show about dialog"""
        info = wx.adv.AboutDialogInfo()
        info.SetName("BMI Health Assistant")
        info.SetVersion("2.0")
        info.SetDescription("A comprehensive BMI calculator with metric/imperial unit support,\npersonalized health tips, activity tracking, and individual trend analysis.")
        info.SetCopyright("@ 2025")
        info.SetWebSite("https://github.com/karthikkr-237/PYTHON-JACKFRUIT-PROBLEM/blob/main/README.md")
        wx.adv.AboutBox(info)

    def on_exit(self, event):
        self.Close()

def main():
    app = wx.App(False)
    frame = BMICalculator()
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
