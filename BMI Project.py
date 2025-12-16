import wx
import wx.grid
import wx.lib.scrolledpanel as scrolled
import wx.adv
import csv
import math
from datetime import datetime
from collections import defaultdict
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
        super().__init__(None, title="BMI Health Assistant", size=(1280, 720))  # 16:9 ratio
        self.SetMinSize(wx.Size(1024, 576))  # Minimum 16:9 ratio
        
        self.dark_mode = False
        self.history = []
        self.person_history = defaultdict(list)  # Store history per person
        self.current_unit = "Metric"  # Track current unit system
        
        # Set application icon
        self.SetIcon(self.create_icon())
        
        self.init_ui()
        self.apply_theme()
        
    def create_icon(self):
        """Create a simple BMI calculator icon"""
        icon = wx.Icon()
        icon.CopyFromBitmap(self.create_bitmap_icon())
        return icon
    
    def create_bitmap_icon(self):
        """Create a bitmap for the icon"""
        bmp = wx.Bitmap(32, 32)
        dc = wx.MemoryDC(bmp)
        dc.SetBackground(wx.Brush(wx.Colour(70, 130, 180)))
        dc.Clear()
        
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        dc.SetPen(wx.Pen(wx.Colour(255, 255, 255), 2))
        
        # Draw a simple scale/balance icon
        dc.DrawLine(16, 8, 16, 24)
        dc.DrawLine(8, 24, 24, 24)
        dc.DrawLine(8, 24, 12, 28)
        dc.DrawLine(24, 24, 20, 28)
        
        dc.SelectObject(wx.NullBitmap)
        return bmp
    
    def init_ui(self):
        # Create menu bar
        menubar = wx.MenuBar()
        
        # File menu
        file_menu = wx.Menu()
        export_csv = file_menu.Append(wx.ID_SAVE, "&Export to CSV\tCtrl+S", "Export history to CSV")
        export_pdf = file_menu.Append(wx.ID_SAVEAS, "&Export to PDF\tCtrl+P", "Export history to PDF")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "&Exit\tCtrl+Q", "Exit application")
        
        # View menu
        view_menu = wx.Menu()
        self.dark_mode_item = view_menu.Append(wx.ID_ANY, "&Dark Mode\tCtrl+D", "Toggle dark mode", kind=wx.ITEM_CHECK)
        
        # Units menu
        units_menu = wx.Menu()
        metric_item = units_menu.AppendRadioItem(wx.ID_ANY, "&Metric Units\tCtrl+M", "Use metric units (kg, cm)")
        imperial_item = units_menu.AppendRadioItem(wx.ID_ANY, "&Imperial Units\tCtrl+I", "Use imperial units (lbs, ft/in)")
        units_menu.Check(metric_item.GetId(), True)  # Default to metric
        
        # Help menu
        help_menu = wx.Menu()
        tips_item = help_menu.Append(wx.ID_HELP, "&Health Tips", "Show detailed health tips")
        about_item = help_menu.Append(wx.ID_ABOUT, "&About", "About BMI Calculator")
        
        menubar.Append(file_menu, "&File")
        menubar.Append(view_menu, "&View")
        menubar.Append(units_menu, "&Units")
        menubar.Append(help_menu, "&Help")
        self.SetMenuBar(menubar)
        
        # Bind menu events
        self.Bind(wx.EVT_MENU, self.on_export_csv, export_csv)
        self.Bind(wx.EVT_MENU, self.on_export_pdf, export_pdf)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.toggle_dark_mode, self.dark_mode_item)
        self.Bind(wx.EVT_MENU, lambda e: self.change_units("Metric"), metric_item)
        self.Bind(wx.EVT_MENU, lambda e: self.change_units("Imperial"), imperial_item)
        self.Bind(wx.EVT_MENU, self.show_health_tips, tips_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        
        # Create main panel with sizer
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Left panel for input (40% width)
        left_panel = wx.Panel(main_panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(left_panel, label="BMI Health Assistant")
        title_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        left_sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        
        # Input section
        input_box = wx.StaticBox(left_panel, label="Personal Information")
        input_sizer = wx.StaticBoxSizer(input_box, wx.VERTICAL)
        
        # Name input
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_sizer.Add(wx.StaticText(left_panel, label="Full Name:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.name_ctrl = wx.TextCtrl(left_panel, style=wx.TE_PROCESS_ENTER)
        name_sizer.Add(self.name_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(name_sizer, 0, wx.EXPAND)
        
        # Age and Gender
        age_gender_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Age
        age_sizer = wx.BoxSizer(wx.HORIZONTAL)
        age_sizer.Add(wx.StaticText(left_panel, label="Age:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.age_ctrl = wx.SpinCtrl(left_panel, min=1, max=120)
        self.age_ctrl.SetValue("")  # No default value
        age_sizer.Add(self.age_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        age_gender_sizer.Add(age_sizer, 1, wx.EXPAND)
        
        # Gender
        gender_sizer = wx.BoxSizer(wx.HORIZONTAL)
        gender_sizer.Add(wx.StaticText(left_panel, label="Gender:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.gender_choice = wx.Choice(left_panel, choices=["Select Gender", "Male", "Female", "Other"])
        self.gender_choice.SetSelection(0)
        gender_sizer.Add(self.gender_choice, 1, wx.EXPAND | wx.ALL, 5)
        age_gender_sizer.Add(gender_sizer, 1, wx.EXPAND)
        
        input_sizer.Add(age_gender_sizer, 0, wx.EXPAND)
        
        # Activity Level
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
        
        # Unit selection
        unit_sizer = wx.BoxSizer(wx.HORIZONTAL)
        unit_sizer.Add(wx.StaticText(left_panel, label="Units:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.unit_choice = wx.Choice(left_panel, choices=["Metric (kg, cm)", "Imperial (lbs, ft/in)"])
        self.unit_choice.SetSelection(0)
        self.unit_choice.Bind(wx.EVT_CHOICE, self.on_unit_change)
        unit_sizer.Add(self.unit_choice, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(unit_sizer, 0, wx.EXPAND)
        
        # Height input - Metric (default)
        self.height_metric_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.height_metric_sizer.Add(wx.StaticText(left_panel, label="Height (cm):"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.height_cm_ctrl = wx.SpinCtrlDouble(left_panel, min=50, max=250, inc=0.1)
        self.height_cm_ctrl.SetDigits(1)
        self.height_cm_ctrl.SetValue("")  # No default value
        self.height_metric_sizer.Add(self.height_cm_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(self.height_metric_sizer, 0, wx.EXPAND)
        
        # Height input - Imperial (hidden by default)
        self.height_imperial_sizer = wx.BoxSizer(wx.HORIZONTAL)
        height_imperial_main = wx.BoxSizer(wx.HORIZONTAL)
        
        # Feet
        feet_sizer = wx.BoxSizer(wx.HORIZONTAL)
        feet_sizer.Add(wx.StaticText(left_panel, label="Feet:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.height_ft_ctrl = wx.SpinCtrl(left_panel, min=3, max=8)
        self.height_ft_ctrl.SetValue("")  # No default value
        feet_sizer.Add(self.height_ft_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        height_imperial_main.Add(feet_sizer, 1, wx.EXPAND)
        
        # Inches
        inches_sizer = wx.BoxSizer(wx.HORIZONTAL)
        inches_sizer.Add(wx.StaticText(left_panel, label="Inches:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.height_in_ctrl = wx.SpinCtrlDouble(left_panel, min=0, max=11.9, inc=0.1)
        self.height_in_ctrl.SetDigits(1)
        self.height_in_ctrl.SetValue("")  # No default value
        inches_sizer.Add(self.height_in_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        height_imperial_main.Add(inches_sizer, 1, wx.EXPAND)
        
        self.height_imperial_sizer.Add(height_imperial_main, 1, wx.EXPAND)
        self.height_imperial_sizer.ShowItems(False)
        input_sizer.Add(self.height_imperial_sizer, 0, wx.EXPAND)
        
        # Weight input - Metric
        self.weight_metric_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.weight_metric_sizer.Add(wx.StaticText(left_panel, label="Weight (kg):"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.weight_kg_ctrl = wx.SpinCtrlDouble(left_panel, min=10, max=300, inc=0.1)
        self.weight_kg_ctrl.SetDigits(1)
        self.weight_kg_ctrl.SetValue("")  # No default value
        self.weight_metric_sizer.Add(self.weight_kg_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        input_sizer.Add(self.weight_metric_sizer, 0, wx.EXPAND)
        
        # Weight input - Imperial
        self.weight_imperial_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.weight_imperial_sizer.Add(wx.StaticText(left_panel, label="Weight (lbs):"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.weight_lbs_ctrl = wx.SpinCtrlDouble(left_panel, min=20, max=660, inc=0.1)
        self.weight_lbs_ctrl.SetDigits(1)
        self.weight_lbs_ctrl.SetValue("")  # No default value
        self.weight_imperial_sizer.Add(self.weight_lbs_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        self.weight_imperial_sizer.ShowItems(False)
        input_sizer.Add(self.weight_imperial_sizer, 0, wx.EXPAND)
        
        left_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Button panel
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
        
        # Results display
        results_box = wx.StaticBox(left_panel, label="BMI Results")
        results_sizer = wx.StaticBoxSizer(results_box, wx.VERTICAL)
        
        results_grid = wx.GridBagSizer(5, 5)
        
        self.bmi_result = wx.StaticText(left_panel, label="--")
        self.bmi_result.SetFont(wx.Font(28, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        results_grid.Add(self.bmi_result, pos=(0, 0), span=(1, 2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        
        self.category_result = wx.StaticText(left_panel, label="Category: --")
        self.category_result.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        results_grid.Add(self.category_result, pos=(1, 0), span=(1, 2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        
        # Ideal weight range
        self.ideal_weight_label = wx.StaticText(left_panel, label="Ideal Weight Range: --")
        self.ideal_weight_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        results_grid.Add(self.ideal_weight_label, pos=(2, 0), span=(1, 2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        
        # Unit display
        self.unit_display = wx.StaticText(left_panel, label="Units: Metric")
        self.unit_display.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        results_grid.Add(self.unit_display, pos=(3, 0), span=(1, 2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        
        results_sizer.Add(results_grid, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        left_sizer.Add(results_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # Health Tips Section (with scroll)
        tips_box = wx.StaticBox(left_panel, label="Health Tips & Recommendations")
        tips_sizer = wx.StaticBoxSizer(tips_box, wx.VERTICAL)
        
        # Create scrolled panel for tips
        self.tips_panel = scrolled.ScrolledPanel(left_panel, size=(-1, 250))
        self.tips_panel.SetupScrolling(scroll_x=False, scroll_y=True)
        tips_content_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.tips_text = wx.StaticText(self.tips_panel, label="Enter your information to see personalized health tips and recommendations.")
        self.tips_text.Wrap(380)
        tips_content_sizer.Add(self.tips_text, 0, wx.EXPAND | wx.ALL, 10)
        
        self.tips_panel.SetSizer(tips_content_sizer)
        tips_sizer.Add(self.tips_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        left_sizer.Add(tips_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        left_panel.SetSizer(left_sizer)
        
        # Right panel for history and charts (60% width)
        right_panel = wx.Panel(main_panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Person selector for charts
        person_box = wx.StaticBox(right_panel, label="Select Person for Charts")
        person_sizer = wx.StaticBoxSizer(person_box, wx.HORIZONTAL)
        
        person_sizer.Add(wx.StaticText(right_panel, label="Person:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.person_choice = wx.Choice(right_panel, choices=["All Persons"])
        self.person_choice.SetSelection(0)
        self.person_choice.Bind(wx.EVT_CHOICE, self.on_person_selected)
        person_sizer.Add(self.person_choice, 1, wx.EXPAND | wx.ALL, 5)
        
        right_sizer.Add(person_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Chart panel
        if MATPLOTLIB_AVAILABLE:
            chart_box = wx.StaticBox(right_panel, label="Personal BMI Trend")
            chart_sizer = wx.StaticBoxSizer(chart_box, wx.VERTICAL)
            
            self.figure = Figure(figsize=(10, 4))
            self.axes = self.figure.add_subplot(111)
            self.canvas = FigureCanvas(right_panel, -1, self.figure)
            
            chart_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
            right_sizer.Add(chart_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        else:
            no_chart_label = wx.StaticText(right_panel, label="Install matplotlib for charts\nRun: pip install matplotlib")
            no_chart_label.SetForegroundColour(wx.Colour(255, 0, 0))
            right_sizer.Add(no_chart_label, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        
        # History grid
        history_box = wx.StaticBox(right_panel, label="Calculation History")
        history_sizer = wx.StaticBoxSizer(history_box, wx.VERTICAL)
        
        self.history_grid = wx.grid.Grid(right_panel)
        self.history_grid.CreateGrid(0, 8)
        self.history_grid.SetColLabelValue(0, "Date")
        self.history_grid.SetColLabelValue(1, "Name")
        self.history_grid.SetColLabelValue(2, "Age")
        self.history_grid.SetColLabelValue(3, "Gender")
        self.history_grid.SetColLabelValue(4, "Activity")
        self.history_grid.SetColLabelValue(5, "BMI")
        self.history_grid.SetColLabelValue(6, "Category")
        self.history_grid.SetColLabelValue(7, "Units")
        
        # Set column widths
        self.history_grid.AutoSizeColumns()
        history_sizer.Add(self.history_grid, 1, wx.EXPAND | wx.ALL, 5)
        
        # History control buttons
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
        
        # Add panels to main sizer with 40:60 ratio
        main_sizer.Add(left_panel, 4, wx.EXPAND | wx.ALL, 5)  # 40%
        main_sizer.Add(right_panel, 6, wx.EXPAND | wx.ALL, 5)  # 60%
        
        main_panel.SetSizer(main_sizer)
        
        # Status bar
        self.CreateStatusBar()
        self.SetStatusText("Enter your personal information and click Calculate BMI")
        
        # Initialize chart
        if MATPLOTLIB_AVAILABLE:
            self.update_chart()
    
    def on_unit_change(self, event):
        """Handle unit system change"""
        unit = self.unit_choice.GetStringSelection()
        if "Metric" in unit:
            self.current_unit = "Metric"
            self.height_metric_sizer.ShowItems(True)
            self.weight_metric_sizer.ShowItems(True)
            self.height_imperial_sizer.ShowItems(False)
            self.weight_imperial_sizer.ShowItems(False)
            self.unit_display.SetLabel("Units: Metric")
        else:
            self.current_unit = "Imperial"
            self.height_metric_sizer.ShowItems(False)
            self.weight_metric_sizer.ShowItems(False)
            self.height_imperial_sizer.ShowItems(True)
            self.weight_imperial_sizer.ShowItems(True)
            self.unit_display.SetLabel("Units: Imperial")
        
        # Refresh layout
        self.Layout()
    
    def change_units(self, unit_system):
        """Change unit system from menu"""
        if unit_system == "Metric":
            self.unit_choice.SetSelection(0)
        else:
            self.unit_choice.SetSelection(1)
        self.on_unit_change(None)
    
    def on_calculate(self, event):
        """Calculate BMI and update results"""
        try:
            # Get input values
            name = self.name_ctrl.GetValue().strip()
            age_str = self.age_ctrl.GetValue()
            gender = self.gender_choice.GetStringSelection()
            activity = self.activity_choice.GetStringSelection()
            
            # Get height and weight based on units
            height_m = 0
            weight_kg = 0
            height_display = ""
            weight_display = ""
            
            if self.current_unit == "Metric":
                height_cm = self.height_cm_ctrl.GetValue()
                weight_kg_val = self.weight_kg_ctrl.GetValue()
                
                validation_error = self.validate_inputs(name, age_str, gender, activity, 
                                                       height_cm, weight_kg_val, "Metric")
                if validation_error:
                    wx.MessageBox(validation_error, "Input Error", wx.OK | wx.ICON_WARNING)
                    return
                
                height_m = float(height_cm) / 100  # Convert to meters
                weight_kg = float(weight_kg_val)
                height_display = f"{height_cm} cm"
                weight_display = f"{weight_kg_val} kg"
            else:
                # Imperial units
                feet = self.height_ft_ctrl.GetValue()
                inches = self.height_in_ctrl.GetValue()
                weight_lbs = self.weight_lbs_ctrl.GetValue()
                
                validation_error = self.validate_inputs(name, age_str, gender, activity, 
                                                       f"{feet}'{inches}\"", weight_lbs, "Imperial")
                if validation_error:
                    wx.MessageBox(validation_error, "Input Error", wx.OK | wx.ICON_WARNING)
                    return
                
                # Convert feet and inches to meters
                total_inches = float(feet) * 12 + float(inches)
                height_m = total_inches * 0.0254
                
                # Convert pounds to kg for BMI calculation
                weight_kg = float(weight_lbs) * 0.453592
                height_display = f"{feet}' {inches}\""
                weight_display = f"{weight_lbs} lbs"
            
            # Convert values
            age = int(age_str)
            
            # Calculate BMI
            bmi = weight_kg / (height_m * height_m)
            
            # Determine category
            category = self.get_bmi_category(bmi, age)
            
            # Calculate ideal weight range
            ideal_min_kg = 18.5 * (height_m * height_m)
            ideal_max_kg = 24.9 * (height_m * height_m)
            
            # Convert ideal weight to current unit system for display
            if self.current_unit == "Imperial":
                ideal_min = ideal_min_kg / 0.453592
                ideal_max = ideal_max_kg / 0.453592
                ideal_range = f"{ideal_min:.1f} - {ideal_max:.1f} lbs"
            else:
                ideal_range = f"{ideal_min_kg:.1f} - {ideal_max_kg:.1f} kg"
            
            # Update results
            self.bmi_result.SetLabel(f"{bmi:.1f}")
            self.bmi_result.SetForegroundColour(self.get_bmi_color(bmi))
            self.category_result.SetLabel(f"Category: {category}")
            self.ideal_weight_label.SetLabel(f"Ideal Weight Range: {ideal_range}")
            self.unit_display.SetLabel(f"Units: {self.current_unit} | Height: {height_display} | Weight: {weight_display}")
            
            # Generate personalized tips
            tips = self.get_personalized_tips(bmi, category, age, gender, activity, weight_kg, height_m)
            self.update_tips_display(tips)
            
            # Add to history
            history_entry = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'name': name,
                'age': age,
                'gender': gender,
                'activity': activity,
                'bmi': round(bmi, 1),
                'category': category,
                'height': height_m * 100,  # Store in cm for consistency
                'weight': weight_kg,  # Store in kg for consistency
                'unit': self.current_unit,
                'height_display': height_display,
                'weight_display': weight_display
            }
            
            self.history.append(history_entry)
            self.person_history[name].append(history_entry)
            
            # Update person list
            self.update_person_list()
            
            # Update displays
            self.update_history_grid()
            self.update_chart()
            
            # Update status
            self.SetStatusText(f"BMI calculated: {bmi:.1f} ({category}) for {name} using {self.current_unit} units")
            
        except ValueError as e:
            wx.MessageBox(f"Please enter valid numeric values.\nError: {str(e)}", "Input Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Error calculating BMI: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
    
    def validate_inputs(self, name, age_str, gender, activity, height_val, weight_val, unit_system):
        """Validate all input fields based on unit system"""
        if not name:
            self.name_ctrl.SetFocus()
            return "Please enter your name."
        
        if not age_str:
            self.age_ctrl.SetFocus()
            return "Please enter your age."
        
        try:
            age = int(age_str)
            if age < 1 or age > 120:
                self.age_ctrl.SetFocus()
                return "Please enter a valid age (1-120 years)."
        except ValueError:
            self.age_ctrl.SetFocus()
            return "Please enter a valid age."
        
        if gender == "Select Gender":
            self.gender_choice.SetFocus()
            return "Please select your gender."
        
        if activity == "Select Activity Level":
            self.activity_choice.SetFocus()
            return "Please select your activity level."
        
        if unit_system == "Metric":
            if not height_val:
                self.height_cm_ctrl.SetFocus()
                return "Please enter your height."
            
            try:
                height = float(height_val)
                if height < 50 or height > 250:
                    self.height_cm_ctrl.SetFocus()
                    return "Please enter a valid height (50-250 cm)."
            except ValueError:
                self.height_cm_ctrl.SetFocus()
                return "Please enter a valid height."
            
            if not weight_val:
                self.weight_kg_ctrl.SetFocus()
                return "Please enter your weight."
            
            try:
                weight = float(weight_val)
                if weight < 10 or weight > 300:
                    self.weight_kg_ctrl.SetFocus()
                    return "Please enter a valid weight (10-300 kg)."
            except ValueError:
                self.weight_kg_ctrl.SetFocus()
                return "Please enter a valid weight."
                
        else:  # Imperial
            # Height validation
            if isinstance(height_val, str) and "'" in height_val:
                # Parse feet and inches from string
                parts = height_val.replace('"', '').split("'")
                if len(parts) != 2:
                    self.height_ft_ctrl.SetFocus()
                    return "Please enter height in feet and inches."
                
                feet_str, inches_str = parts
                if not feet_str or not inches_str:
                    self.height_ft_ctrl.SetFocus()
                    return "Please enter both feet and inches."
                
                try:
                    feet = int(feet_str)
                    inches = float(inches_str)
                    if feet < 3 or feet > 8:
                        self.height_ft_ctrl.SetFocus()
                        return "Please enter valid feet (3-8)."
                    if inches < 0 or inches >= 12:
                        self.height_in_ctrl.SetFocus()
                        return "Please enter valid inches (0-11.9)."
                except ValueError:
                    self.height_ft_ctrl.SetFocus()
                    return "Please enter valid height values."
            
            # Weight validation
            if not weight_val:
                self.weight_lbs_ctrl.SetFocus()
                return "Please enter your weight."
            
            try:
                weight = float(weight_val)
                if weight < 20 or weight > 660:
                    self.weight_lbs_ctrl.SetFocus()
                    return "Please enter a valid weight (20-660 lbs)."
            except ValueError:
                self.weight_lbs_ctrl.SetFocus()
                return "Please enter a valid weight."
        
        return None
    
    def get_bmi_color(self, bmi):
        """Get color based on BMI value"""
        if bmi < 18.5:
            return wx.Colour(0, 0, 255)  # Blue for underweight
        elif bmi < 25:
            return wx.Colour(0, 128, 0)  # Green for normal
        elif bmi < 30:
            return wx.Colour(255, 165, 0)  # Orange for overweight
        else:
            return wx.Colour(255, 0, 0)  # Red for obese
    
    def get_bmi_category(self, bmi, age):
        """Get BMI category based on age"""
        # For adults (18+)
        if age >= 18:
            if bmi < 16:
                return "Severely Underweight"
            elif bmi < 18.5:
                return "Underweight"
            elif bmi < 25:
                return "Normal Weight"
            elif bmi < 30:
                return "Overweight"
            elif bmi < 35:
                return "Obesity Class I"
            elif bmi < 40:
                return "Obesity Class II"
            else:
                return "Obesity Class III"
        else:
            # For children (simplified)
            if bmi < 5:
                return "Underweight (Child)"
            elif bmi < 85:
                return "Healthy Weight (Child)"
            elif bmi < 95:
                return "Overweight (Child)"
            else:
                return "Obese (Child)"
    
    def get_personalized_tips(self, bmi, category, age, gender, activity, weight_kg, height_m):
        """Generate personalized health tips"""
        tips = []
        
        # Unit-specific measurements
        if self.current_unit == "Metric":
            height_unit = "cm"
            weight_unit = "kg"
            current_height = height_m * 100
            current_weight = weight_kg
        else:
            height_unit = "ft/in"
            weight_unit = "lbs"
            current_height = height_m / 0.0254  # in inches
            current_weight = weight_kg / 0.453592  # in pounds
        
        # BMI-specific tips
        if "Underweight" in category:
            tips.append("📈 **Weight Gain Tips:**")
            tips.append("• Eat 5-6 small meals throughout the day")
            tips.append("• Include healthy fats (avocado, nuts, olive oil)")
            tips.append("• Add protein shakes or smoothies between meals")
            tips.append("• Strength training 2-3 times per week")
            tips.append("• Monitor weight weekly, aim for gradual gain")
            
        elif "Normal" in category:
            tips.append("✅ **Maintenance Tips:**")
            tips.append("• Continue balanced diet with all food groups")
            tips.append("• Regular exercise (150 min/week moderate intensity)")
            tips.append("• Monitor weight monthly to maintain range")
            tips.append("• Stay hydrated (8-10 glasses of water daily)")
            tips.append("• Get 7-9 hours of quality sleep")
            
        elif "Overweight" in category or "Obese" in category:
            tips.append("📉 **Weight Loss Tips:**")
            tips.append("• Aim to lose 0.5-1 kg per week safely")
            tips.append("• Reduce processed foods and sugary drinks")
            tips.append("• Increase vegetable and fiber intake")
            tips.append("• 30 minutes of exercise most days")
            tips.append("• Portion control - use smaller plates")
            tips.append("• Keep a food diary to track eating patterns")
        
        # Activity level tips
        if "Sedentary" in activity:
            tips.append("\n🏃 **Activity Improvement:**")
            tips.append("• Start with 10-minute walks, 3 times daily")
            tips.append("• Take stairs instead of elevator")
            tips.append("• Stand up and stretch every hour")
            tips.append("• Gradually increase to 30 minutes daily")
        elif "Lightly Active" in activity:
            tips.append("\n🏃 **Activity Maintenance:**")
            tips.append("• Continue your current routine")
            tips.append("• Consider adding strength training")
            tips.append("• Try new activities like swimming or cycling")
        else:
            tips.append("\n🏃 **Activity Maintenance:**")
            tips.append("• Great job staying active!")
            tips.append("• Ensure proper rest and recovery")
            tips.append("• Vary your workouts to prevent boredom")
        
        # Age-specific tips
        if age < 18:
            tips.append("\n👶 **For Younger Individuals:**")
            tips.append("• Focus on healthy growth, not weight loss")
            tips.append("• Include calcium-rich foods for bone health")
            tips.append("• Limit screen time to 2 hours/day")
            tips.append("• 60 minutes of physical activity daily")
        elif age > 50:
            tips.append("\n👵 **For Older Adults:**")
            tips.append("• Include weight-bearing exercises for bone density")
            tips.append("• Ensure adequate protein for muscle preservation")
            tips.append("• Regular health check-ups")
            tips.append("• Focus on balance and flexibility exercises")
        
        # Gender-specific tips
        if gender == "Female":
            tips.append("\n👩 **Women's Health:**")
            tips.append("• Ensure adequate iron and calcium intake")
            tips.append("• Women naturally have higher body fat percentage")
            tips.append("• Consider bone density screening after menopause")
        elif gender == "Male":
            tips.append("\n👨 **Men's Health:**")
            tips.append("• Monitor heart health and cholesterol")
            tips.append("• Men typically carry more weight as muscle")
            tips.append("• Regular prostate screening after age 50")
        
        # Unit conversion note
        tips.append(f"\n📏 **Current Measurements:**")
        if self.current_unit == "Metric":
            tips.append(f"• Height: {height_m*100:.1f} cm")
            tips.append(f"• Weight: {weight_kg:.1f} kg")
        else:
            tips.append(f"• Height: {height_m/0.0254:.1f} inches")
            tips.append(f"• Weight: {weight_kg/0.453592:.1f} lbs")
        
        # General health tips
        tips.append("\n💡 **General Health Advice:**")
        tips.append("• Drink plenty of water throughout the day")
        tips.append("• Manage stress through meditation or hobbies")
        tips.append("• Avoid smoking and limit alcohol")
        tips.append("• Eat a rainbow of fruits and vegetables")
        tips.append("• Practice mindful eating")
        
        return "\n".join(tips)
    
    def update_tips_display(self, tips):
        """Update the tips display with formatted text"""
        # Clear existing content
        self.tips_panel.DestroyChildren()
        
        tips_content_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create a text control for better formatting
        tips_text = wx.TextCtrl(self.tips_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH | wx.TE_WORDWRAP)
        tips_text.SetValue(tips)
        
        # Apply some basic formatting
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        tips_text.SetFont(font)
        tips_text.SetBackgroundColour(self.tips_panel.GetBackgroundColour())
        
        tips_content_sizer.Add(tips_text, 1, wx.EXPAND | wx.ALL, 10)
        self.tips_panel.SetSizer(tips_content_sizer)
        self.tips_panel.SetupScrolling(scroll_x=False, scroll_y=True)
        self.tips_panel.Layout()
    
    def update_person_list(self):
        """Update the person selection dropdown"""
        persons = ["All Persons"] + sorted(list(self.person_history.keys()))
        self.person_choice.SetItems(persons)
        self.person_choice.SetSelection(0)
    
    def on_person_selected(self, event):
        """Handle person selection for charts"""
        self.update_chart()
    
    def update_history_grid(self):
        """Update the history grid with current data"""
        self.history_grid.ClearGrid()
        
        if self.history_grid.GetNumberRows() > 0:
            self.history_grid.DeleteRows(0, self.history_grid.GetNumberRows())
        
        for i, entry in enumerate(self.history[-50:]):  # Show last 50 entries
            self.history_grid.AppendRows(1)
            self.history_grid.SetCellValue(i, 0, entry['date'])
            self.history_grid.SetCellValue(i, 1, entry['name'])
            self.history_grid.SetCellValue(i, 2, str(entry['age']))
            self.history_grid.SetCellValue(i, 3, entry['gender'])
            # Shorten activity description
            activity_short = entry['activity'].split('(')[0].strip()
            self.history_grid.SetCellValue(i, 4, activity_short)
            self.history_grid.SetCellValue(i, 5, str(entry['bmi']))
            self.history_grid.SetCellValue(i, 6, entry['category'])
            self.history_grid.SetCellValue(i, 7, entry['unit'])
            
            # Color code based on BMI
            bmi = entry['bmi']
            if bmi < 18.5:
                color = wx.Colour(135, 206, 250)  # Light blue
            elif bmi < 25:
                color = wx.Colour(144, 238, 144)  # Light green
            elif bmi < 30:
                color = wx.Colour(255, 215, 0)    # Gold
            else:
                color = wx.Colour(255, 165, 0)    # Orange
            
            self.history_grid.SetCellBackgroundColour(i, 6, color)
            self.history_grid.SetCellTextColour(i, 6, wx.BLACK if bmi < 30 else wx.WHITE)
        
        self.history_grid.AutoSizeColumns()
    
    def update_chart(self):
        """Update the trend chart for selected person"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        self.axes.clear()
        
        selected_person = self.person_choice.GetStringSelection()
        
        if selected_person == "All Persons" or selected_person not in self.person_history:
            # Show all data
            data_to_plot = self.history
            title = "BMI Trend - All Persons"
        else:
            # Show data for selected person
            data_to_plot = self.person_history[selected_person]
            title = f"BMI Trend - {selected_person}"
        
        if len(data_to_plot) < 1:
            # No data to plot
            self.axes.text(0.5, 0.5, 'No data available\nCalculate BMI to see chart', 
                          horizontalalignment='center', verticalalignment='center',
                          transform=self.axes.transAxes, fontsize=12)
            self.axes.set_xlim(0, 1)
            self.axes.set_ylim(0, 1)
            self.axes.set_xticks([])
            self.axes.set_yticks([])
        else:
            # Prepare data for chart
            dates = [datetime.strptime(entry['date'], "%Y-%m-%d %H:%M") for entry in data_to_plot]
            bmis = [entry['bmi'] for entry in data_to_plot]
            names = [entry['name'] for entry in data_to_plot]
            units = [entry.get('unit', 'Metric') for entry in data_to_plot]
            
            # Plot BMI trend with different markers for different people
            if selected_person == "All Persons":
                # Group by person for different colors
                person_colors = {}
                unique_names = list(set(names))
                colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray']
                
                for i, name in enumerate(unique_names):
                    person_colors[name] = colors[i % len(colors)]
                    person_data = [entry for entry in data_to_plot if entry['name'] == name]
                    person_dates = [datetime.strptime(entry['date'], "%Y-%m-%d %H:%M") for entry in person_data]
                    person_bmis = [entry['bmi'] for entry in person_data]
                    
                    self.axes.plot(person_dates, person_bmis, 'o-', linewidth=2, markersize=6, 
                                  color=person_colors[name], label=name)
                
                self.axes.legend(loc='best')
            else:
                # Single person
                self.axes.plot(dates, bmis, 'b-o', linewidth=2, markersize=6, label='BMI Trend')
            
            # Add category zones
            self.axes.axhspan(0, 18.5, alpha=0.1, color='blue', label='Underweight')
            self.axes.axhspan(18.5, 25, alpha=0.1, color='green', label='Normal')
            self.axes.axhspan(25, 30, alpha=0.1, color='yellow', label='Overweight')
            self.axes.axhspan(30, 50, alpha=0.1, color='red', label='Obese')
            
            self.axes.set_xlabel('Date')
            self.axes.set_ylabel('BMI')
            self.axes.set_title(title)
            self.axes.grid(True, alpha=0.3)
            
            # Set y-axis limits
            if bmis:
                y_min = max(0, min(bmis) - 5)
                y_max = max(bmis) + 5
                self.axes.set_ylim(y_min, y_max)
            
            # Format x-axis dates
            self.figure.autofmt_xdate()
        
        self.canvas.draw()
    
    def on_reset(self, event):
        """Reset all input fields"""
        self.name_ctrl.Clear()
        self.age_ctrl.SetValue("")
        self.gender_choice.SetSelection(0)
        self.activity_choice.SetSelection(0)
        
        # Reset based on current unit
        if self.current_unit == "Metric":
            self.height_cm_ctrl.SetValue("")
            self.weight_kg_ctrl.SetValue("")
        else:
            self.height_ft_ctrl.SetValue("")
            self.height_in_ctrl.SetValue("")
            self.weight_lbs_ctrl.SetValue("")
        
        self.bmi_result.SetLabel("--")
        self.bmi_result.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.category_result.SetLabel("Category: --")
        self.ideal_weight_label.SetLabel("Ideal Weight Range: --")
        self.unit_display.SetLabel(f"Units: {self.current_unit}")
        
        # Reset tips display
        self.update_tips_display("Enter your information to see personalized health tips and recommendations.")
        
        self.name_ctrl.SetFocus()
        self.SetStatusText("All fields reset. Enter new information.")
    
    def on_export_csv(self, event):
        """Export history to CSV file"""
        if not self.history:
            wx.MessageBox("No data to export.", "Export", wx.OK | wx.ICON_WARNING)
            return
        
        with wx.FileDialog(self, "Save CSV file", wildcard="CSV files (*.csv)|*.csv",
                          style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            
            filename = dialog.GetPath()
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['date', 'name', 'age', 'gender', 'activity', 'height_cm', 'weight_kg', 
                                 'bmi', 'category', 'unit', 'height_display', 'weight_display']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for entry in self.history:
                        writer.writerow({
                            'date': entry['date'],
                            'name': entry['name'],
                            'age': entry['age'],
                            'gender': entry['gender'],
                            'activity': entry['activity'],
                            'height_cm': entry['height'],
                            'weight_kg': entry['weight'],
                            'bmi': entry['bmi'],
                            'category': entry['category'],
                            'unit': entry.get('unit', 'Metric'),
                            'height_display': entry.get('height_display', ''),
                            'weight_display': entry.get('weight_display', '')
                        })
                
                wx.MessageBox(f"Data exported to {filename}", "Export Successful", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error exporting data: {str(e)}", "Export Error", wx.OK | wx.ICON_ERROR)
    
    def on_export_pdf(self, event):
        """Export history to PDF (simplified - using text report)"""
        if not self.history:
            wx.MessageBox("No data to export.", "Export", wx.OK | wx.ICON_WARNING)
            return
        
        with wx.FileDialog(self, "Save Report", wildcard="Text files (*.txt)|*.txt",
                          style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            
            filename = dialog.GetPath()
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("BMI Health Assistant Report\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Total Records: {len(self.history)}\n")
                    f.write(f"Unique Persons: {len(self.person_history)}\n\n")
                    
                    # Summary by person
                    f.write("Summary by Person:\n")
                    f.write("-" * 60 + "\n")
                    for person, records in self.person_history.items():
                        latest = records[-1]
                        f.write(f"\n{person}:\n")
                        f.write(f"  Latest BMI: {latest['bmi']} ({latest['category']})\n")
                        f.write(f"  Age: {latest['age']}, Gender: {latest['gender']}\n")
                        f.write(f"  Activity Level: {latest['activity'].split('(')[0].strip()}\n")
                        f.write(f"  Units: {latest.get('unit', 'Metric')}\n")
                        f.write(f"  Total Records: {len(records)}\n")
                    
                    # Detailed history
                    f.write("\n\nDetailed History:\n")
                    f.write("-" * 60 + "\n")
                    for entry in self.history:
                        f.write(f"\nDate: {entry['date']}\n")
                        f.write(f"Name: {entry['name']}, Age: {entry['age']}, Gender: {entry['gender']}\n")
                        f.write(f"Activity: {entry['activity']}\n")
                        f.write(f"Units: {entry.get('unit', 'Metric')}\n")
                        if 'height_display' in entry and 'weight_display' in entry:
                            f.write(f"Height: {entry['height_display']}, Weight: {entry['weight_display']}\n")
                        f.write(f"BMI: {entry['bmi']}, Category: {entry['category']}\n")
                        f.write("-" * 40 + "\n")
                
                wx.MessageBox(f"Report exported to {filename}", "Export Successful", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error exporting report: {str(e)}", "Export Error", wx.OK | wx.ICON_ERROR)
    
    def on_clear_history(self, event):
        """Clear the history"""
        if wx.MessageBox("Are you sure you want to clear all history?", "Confirm Clear",
                        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
            self.history.clear()
            self.person_history.clear()
            self.update_history_grid()
            self.update_person_list()
            if MATPLOTLIB_AVAILABLE:
                self.update_chart()
            self.SetStatusText("History cleared")
    
    def show_health_tips(self, event):
        """Show comprehensive health tips dialog"""
        tips_dialog = wx.Dialog(self, title="Comprehensive Health Tips", size=(700, 500))
        
        notebook = wx.Notebook(tips_dialog)
        
        # Nutrition Tips
        nutrition_panel = wx.Panel(notebook)
        nutrition_text = wx.TextCtrl(nutrition_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH | wx.TE_WORDWRAP)
        nutrition_text.SetValue(
            "🍎 **Nutrition Guidelines:**\n\n"
            "• Eat a variety of fruits and vegetables daily\n"
            "• Choose whole grains over refined grains\n"
            "• Include lean proteins (chicken, fish, beans, lentils)\n"
            "• Limit saturated and trans fats\n"
            "• Reduce sodium intake\n"
            "• Limit added sugars\n"
            "• Stay hydrated with water\n"
            "• Practice portion control\n\n"
            
            "🥗 **Healthy Eating Patterns:**\n"
            "• Mediterranean diet\n"
            "• DASH diet (for blood pressure)\n"
            "• Plant-based diets\n"
            "• Mindful eating practices\n"
        )
        
        nutrition_sizer = wx.BoxSizer(wx.VERTICAL)
        nutrition_sizer.Add(nutrition_text, 1, wx.EXPAND | wx.ALL, 10)
        nutrition_panel.SetSizer(nutrition_sizer)
        
        # Exercise Tips
        exercise_panel = wx.Panel(notebook)
        exercise_text = wx.TextCtrl(exercise_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH | wx.TE_WORDWRAP)
        exercise_text.SetValue(
            "🏋️ **Exercise Recommendations:**\n\n"
            "• 150 minutes moderate or 75 minutes vigorous exercise weekly\n"
            "• Strength training 2-3 times per week\n"
            "• Flexibility exercises daily\n"
            "• Balance exercises for older adults\n\n"
            
            "🚶 **Activity Ideas:**\n"
            "• Brisk walking\n"
            "• Swimming or cycling\n"
            "• Dancing\n"
            "• Yoga or Pilates\n"
            "• Team sports\n"
            "• Gardening\n\n"
            
            "💪 **Strength Training:**\n"
            "• Bodyweight exercises (push-ups, squats)\n"
            "• Resistance bands\n"
            "• Free weights\n"
            "• Weight machines\n"
        )
        
        exercise_sizer = wx.BoxSizer(wx.VERTICAL)
        exercise_sizer.Add(exercise_text, 1, wx.EXPAND | wx.ALL, 10)
        exercise_panel.SetSizer(exercise_sizer)
        
        # Unit Conversion Tips
        conversion_panel = wx.Panel(notebook)
        conversion_text = wx.TextCtrl(conversion_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH | wx.TE_WORDWRAP)
        conversion_text.SetValue(
            "📏 **Unit Conversions:**\n\n"
            "Metric to Imperial:\n"
            "• 1 cm = 0.3937 inches\n"
            "• 1 meter = 3.2808 feet\n"
            "• 1 kg = 2.2046 pounds\n\n"
            
            "Imperial to Metric:\n"
            "• 1 inch = 2.54 cm\n"
            "• 1 foot = 30.48 cm\n"
            "• 1 pound = 0.4536 kg\n\n"
            
            "BMI Formula:\n"
            "• Metric: weight(kg) / [height(m)]²\n"
            "• Imperial: [weight(lbs) / height(inches)²] × 703\n\n"
            
            "Height Conversions:\n"
            "• 5'0\" = 152.4 cm\n"
            "• 5'5\" = 165.1 cm\n"
            "• 6'0\" = 182.9 cm\n"
            "• 6'5\" = 195.6 cm\n\n"
            
            "Weight Conversions:\n"
            "• 110 lbs = 49.9 kg\n"
            "• 150 lbs = 68.0 kg\n"
            "• 200 lbs = 90.7 kg\n"
            "• 250 lbs = 113.4 kg\n"
        )
        
        conversion_sizer = wx.BoxSizer(wx.VERTICAL)
        conversion_sizer.Add(conversion_text, 1, wx.EXPAND | wx.ALL, 10)
        conversion_panel.SetSizer(conversion_sizer)
        
        notebook.AddPage(nutrition_panel, "Nutrition")
        notebook.AddPage(exercise_panel, "Exercise")
        notebook.AddPage(conversion_panel, "Unit Conversions")
        
        # OK button
        ok_btn = wx.Button(tips_dialog, wx.ID_OK, "Close")
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(ok_btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        tips_dialog.SetSizer(main_sizer)
        tips_dialog.ShowModal()
    
    def toggle_dark_mode(self, event):
        """Toggle dark mode on/off"""
        self.dark_mode = not self.dark_mode
        self.dark_mode_item.Check(self.dark_mode)
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme (light/dark)"""
        if self.dark_mode:
            # Dark theme colors
            bg_color = wx.Colour(30, 30, 30)
            fg_color = wx.Colour(220, 220, 220)
            panel_color = wx.Colour(50, 50, 50)
            text_bg = wx.Colour(40, 40, 40)
            button_color = wx.Colour(70, 70, 70)
        else:
            # Light theme colors
            bg_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            fg_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
            panel_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
            text_bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            button_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        
        # Apply colors to all windows
        self.SetBackgroundColour(bg_color)
        self.SetForegroundColour(fg_color)
        
        # Refresh all children
        self.RefreshAll(self, bg_color, fg_color, panel_color, text_bg, button_color)
    
    def RefreshAll(self, parent, bg_color, fg_color, panel_color, text_bg, button_color):
        """Recursively refresh all child controls"""
        for child in parent.GetChildren():
            if isinstance(child, (wx.Panel, wx.StaticBox)):
                child.SetBackgroundColour(panel_color)
                child.SetForegroundColour(fg_color)
                child.Refresh()
            elif isinstance(child, (wx.Button)):
                child.SetBackgroundColour(button_color)
                child.SetForegroundColour(fg_color)
                child.Refresh()
            elif isinstance(child, (wx.TextCtrl, wx.SpinCtrl, wx.SpinCtrlDouble, wx.Choice)):
                child.SetBackgroundColour(text_bg)
                child.SetForegroundColour(fg_color)
                child.Refresh()
            elif isinstance(child, wx.StaticText):
                child.SetBackgroundColour(panel_color)
                child.SetForegroundColour(fg_color)
                child.Refresh()
            
            if isinstance(child, wx.grid.Grid):
                child.SetDefaultCellBackgroundColour(text_bg)
                child.SetDefaultCellTextColour(fg_color)
                child.SetLabelBackgroundColour(panel_color)
                child.SetLabelTextColour(fg_color)
                child.Refresh()
            
            # Recursively process children
            self.RefreshAll(child, bg_color, fg_color, panel_color, text_bg, button_color)
    
    def on_about(self, event):
        """Show about dialog"""
        info = wx.adv.AboutDialogInfo()
        info.SetName("Report")
        info.SetVersion("2.0")
        info.SetDescription("A comprehensive BMI calculator with metric/imperial unit support,\npersonalized health tips, activity tracking, and individual trend analysis.")
        info.SetCopyright("(@) 2025")
        info.SetWebSite("README.md")
        
        wx.adv.AboutBox(info)
    
    def on_exit(self, event):
        """Exit the application"""
        self.Close()

def main():
    app = wx.App(False)
    frame = BMICalculator()
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()

