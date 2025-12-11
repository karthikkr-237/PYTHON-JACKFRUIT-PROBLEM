import wx

# Create the application
app = wx.App()

# Create the main window
frame = wx.Frame(None, title="BMI Calculator", size=(600, 700))

# Create a panel to hold widgets
panel = wx.Panel(frame)

# Create fonts
title_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
result_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
tip_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
label_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

# Title
title = wx.StaticText(panel, label="BMI Calculator")
title.SetFont(title_font)
title.SetForegroundColour(wx.Colour(0, 70, 140))

# Unit system selection
unit_label = wx.StaticText(panel, label="Unit System:")
unit_label.SetFont(label_font)
unit_choice = wx.Choice(panel, choices=["Metric (kg, cm)", "Imperial (lbs, inches)"])
unit_choice.SetSelection(0)

# Input fields with better labels
height_label = wx.StaticText(panel, label="Height:")
height_label.SetFont(label_font)
height_input = wx.TextCtrl(panel, size=(120, -1))

weight_label = wx.StaticText(panel, label="Weight:")
weight_label.SetFont(label_font)
weight_input = wx.TextCtrl(panel, size=(120, -1))

# Unit labels that will update
height_unit = wx.StaticText(panel, label="cm")
height_unit.SetFont(label_font)
weight_unit = wx.StaticText(panel, label="kg")
weight_unit.SetFont(label_font)

# Buttons with icons
calculate_btn = wx.Button(panel, label="  Calculate BMI  ", size=(120, 35))
clear_btn = wx.Button(panel, label="  Clear All  ", size=(120, 35))

# Result display
result_label = wx.StaticText(panel, label="Your BMI:")
result_label.SetFont(label_font)
result_display = wx.StaticText(panel, label="")
result_display.SetFont(result_font)

# Category display
category_label = wx.StaticText(panel, label="Category:")
category_label.SetFont(label_font)
category_display = wx.StaticText(panel, label="")
category_display.SetFont(result_font)

# Health Tips display
tips_label = wx.StaticText(panel, label="Health Tips:")
tips_label.SetFont(label_font)
tips_label.SetForegroundColour(wx.Colour(0, 100, 0))
tips_display = wx.StaticText(panel, label="")
tips_display.SetFont(tip_font)
tips_display.SetForegroundColour(wx.Colour(50, 50, 50))
tips_display.Wrap(400)  # Wrap text at 400 pixels

# BMI Categories reference with better formatting
categories_label = wx.StaticText(panel, label="")
categories_label.SetFont(label_font)

# Create a panel for categories with color coding
categories_panel = wx.Panel(panel)
categories_panel.SetBackgroundColour(wx.Colour(245, 245, 245))

# Create category items with colors
category_items = [
    ("Category", "BMI Range", "Health Tips"),
    ("Underweight", "< 18.5", "Consider consulting a nutritionist\nfor healthy weight gain tips"),
    ("Normal weight", "18.5 - 24.9", "Maintain your healthy lifestyle!\nKeep exercising and eating balanced meals"),
    ("Overweight", "25 - 29.9", "Regular exercise and portion control\ncan help achieve healthy weight"),
    ("Obesity", "≥ 30", "Consult healthcare professional\nfor personalized weight management plan")
]

# Create a GridSizer for the main layout
main_grid = wx.GridBagSizer(10, 15)

# Title row
main_grid.Add(title, pos=(0, 0), span=(1, 4), flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)

# Unit selection row
main_grid.Add(unit_label, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
main_grid.Add(unit_choice, pos=(1, 1), span=(1, 2), flag=wx.EXPAND)

# Input fields
main_grid.Add(height_label, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
main_grid.Add(height_input, pos=(2, 1), flag=wx.EXPAND)
main_grid.Add(height_unit, pos=(2, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)

main_grid.Add(weight_label, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
main_grid.Add(weight_input, pos=(3, 1), flag=wx.EXPAND)
main_grid.Add(weight_unit, pos=(3, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)

# Buttons row
button_sizer = wx.BoxSizer(wx.HORIZONTAL)
button_sizer.Add(calculate_btn, 0, wx.RIGHT, 10)
button_sizer.Add(clear_btn, 0)
main_grid.Add(button_sizer, pos=(4, 1), span=(1, 2), flag=wx.TOP, border=20)

# Results section
main_grid.Add(result_label, pos=(5, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
main_grid.Add(result_display, pos=(5, 1), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)

main_grid.Add(category_label, pos=(6, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
main_grid.Add(category_display, pos=(6, 1), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)

# Tips section
main_grid.Add(tips_label, pos=(7, 0), flag=wx.TOP | wx.LEFT, border=20)
main_grid.Add(tips_display, pos=(8, 0), span=(1, 4), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

# Categories reference
main_grid.Add(categories_label, pos=(9, 0), span=(1, 4), flag=wx.TOP | wx.LEFT, border=20)

# Create a GridSizer for categories
categories_sizer = wx.GridBagSizer(5, 10)

# Add category items
for i, (category, bmi_range, tip) in enumerate(category_items):
    # Category label with color
    cat_label = wx.StaticText(categories_panel, label=category)
    cat_label.SetFont(label_font)
    
    # BMI range
    range_label = wx.StaticText(categories_panel, label=bmi_range)
    range_label.SetFont(tip_font)
    
    # Add to grid
    categories_sizer.Add(cat_label, pos=(i, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
    categories_sizer.Add(range_label, pos=(i, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)

# Set categories panel sizer
categories_panel.SetSizer(categories_sizer)
main_grid.Add(categories_panel, pos=(10, 0), span=(1, 4), flag=wx.EXPAND | wx.ALL, border=20)

# Configure column proportions
main_grid.AddGrowableCol(1)
main_grid.AddGrowableCol(3)

# Create a main sizer for the panel
main_sizer = wx.BoxSizer(wx.VERTICAL)
main_sizer.Add(main_grid, 1, wx.EXPAND | wx.ALL, 10)

# Set the sizer for the panel
panel.SetSizer(main_sizer)

# Function to update unit labels
def update_units(event):
    selection = unit_choice.GetSelection()
    if selection == 0:  # Metric
        height_unit.SetLabel("cm")
        weight_unit.SetLabel("kg")
        # Update placeholders
        height_input.SetHint("Enter height in cm")
        weight_input.SetHint("Enter weight in kg")
    else:  # Imperial
        height_unit.SetLabel("inches")
        weight_unit.SetLabel("lbs")
        height_input.SetHint("Enter height in inches")
        weight_input.SetHint("Enter weight in lbs")

# Function to get health tips based on BMI category
def get_health_tips(bmi_category):
    tips = {
        "Underweight": [
            "* Eat more frequent, nutrient-dense meals",
            "* Include healthy fats (avocado, nuts, olive oil)",
            "* Consider strength training to build muscle",
            "* Consult a doctor if unintentional weight loss occurs"
        ],
        "Normal weight": [
            "* Maintain balanced diet with variety of foods",
            "* Engage in 150 minutes of moderate exercise weekly",
            "* Get regular health check-ups",
            "* Stay hydrated and get adequate sleep"
        ],
        "Overweight": [
            "* Start with 30 minutes of daily walking",
            "* Reduce sugary drinks and processed foods",
            "* Practice portion control",
            "* Aim for gradual weight loss (1-2 lbs per week)"
        ],
        "Obesity": [
            "* Consult healthcare professional for guidance",
            "* Consider dietary counseling",
            "* Start with low-impact exercises (swimming, cycling)",
            "* Focus on sustainable lifestyle changes"
        ]
    }
    
    return tips.get(bmi_category, ["Maintain a healthy lifestyle"])

# Function to calculate BMI
def calculate_bmi(event):
    is_metric = (unit_choice.GetSelection() == 0)
    
    height_str = height_input.GetValue()
    weight_str = weight_input.GetValue()
    
    if not height_str or not weight_str:
        # Show error in separate frame
        error_frame = wx.Frame(None, title="Error", size=(400, 150))
        error_panel = wx.Panel(error_frame)
        error_sizer = wx.BoxSizer(wx.VERTICAL)
        
        error_msg = wx.StaticText(error_panel, label="Please enter both height and weight values!")
        error_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        error_msg.SetFont(error_font)
        error_msg.SetForegroundColour(wx.Colour(255, 0, 0))
        
        error_sizer.Add(error_msg, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        
        ok_btn = wx.Button(error_panel, label="OK")
        ok_btn.Bind(wx.EVT_BUTTON, lambda e: error_frame.Close())
        error_sizer.Add(ok_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        error_panel.SetSizer(error_sizer)
        error_frame.Show()
        return
    
    try:
        height = float(height_str)
        weight = float(weight_str)
        
        if height <= 0 or weight <= 0:
            # Show error in separate frame
            error_frame = wx.Frame(None, title="Invalid Input Error", size=(400, 200))
            error_panel = wx.Panel(error_frame)
            error_sizer = wx.BoxSizer(wx.VERTICAL)
            
            error_msg = wx.StaticText(error_panel, label="Values must be positive numbers!")
            error_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            error_msg.SetFont(error_font)
            error_msg.SetForegroundColour(wx.Colour(255, 0, 0))
            
            error_sizer.Add(error_msg, 0, wx.ALL | wx.ALIGN_CENTER, 20)
            
            ok_btn = wx.Button(error_panel, label="OK")
            ok_btn.Bind(wx.EVT_BUTTON, lambda e: error_frame.Close())
            error_sizer.Add(ok_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
            
            error_panel.SetSizer(error_sizer)
            error_frame.Show()
            return
        
        if is_metric and height > 300:  # Sanity check for cm
            # Show error in separate frame
            error_frame = wx.Frame(None, title="Invalid Height Error", size=(400, 250))
            error_panel = wx.Panel(error_frame)
            error_sizer = wx.BoxSizer(wx.VERTICAL)
            
            error_msg = wx.StaticText(error_panel, label="Height seems too high!\nFor metric, height should be in centimeters (e.g., 175)")
            error_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            error_msg.SetFont(error_font)
            error_msg.SetForegroundColour(wx.Colour(255, 0, 0))
            error_msg.Wrap(350)
            
            error_sizer.Add(error_msg, 0, wx.ALL | wx.ALIGN_CENTER, 20)
            
            ok_btn = wx.Button(error_panel, label="OK")
            ok_btn.Bind(wx.EVT_BUTTON, lambda e: error_frame.Close())
            error_sizer.Add(ok_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
            
            error_panel.SetSizer(error_sizer)
            error_frame.Show()
            return
            
        if not is_metric and height > 120:  # Sanity check for inches
            # Show error in separate frame
            error_frame = wx.Frame(None, title="Invalid Height Error", size=(400, 250))
            error_panel = wx.Panel(error_frame)
            error_sizer = wx.BoxSizer(wx.VERTICAL)
            
            error_msg = wx.StaticText(error_panel, label="Height seems too high!\nFor imperial, height should be in inches (e.g., 68)")
            error_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            error_msg.SetFont(error_font)
            error_msg.SetForegroundColour(wx.Colour(255, 0, 0))
            error_msg.Wrap(350)
            
            error_sizer.Add(error_msg, 0, wx.ALL | wx.ALIGN_CENTER, 20)
            
            ok_btn = wx.Button(error_panel, label="OK")
            ok_btn.Bind(wx.EVT_BUTTON, lambda e: error_frame.Close())
            error_sizer.Add(ok_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
            
            error_panel.SetSizer(error_sizer)
            error_frame.Show()
            return
            
    except ValueError:
        # Show error in separate frame
        error_frame = wx.Frame(None, title="Invalid Format Error", size=(400, 200))
        error_panel = wx.Panel(error_frame)
        error_sizer = wx.BoxSizer(wx.VERTICAL)
        
        error_msg = wx.StaticText(error_panel, label="Please enter numerical values only!")
        error_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        error_msg.SetFont(error_font)
        error_msg.SetForegroundColour(wx.Colour(255, 0, 0))
        
        error_sizer.Add(error_msg, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        
        ok_btn = wx.Button(error_panel, label="OK")
        ok_btn.Bind(wx.EVT_BUTTON, lambda e: error_frame.Close())
        error_sizer.Add(ok_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        error_panel.SetSizer(error_sizer)
        error_frame.Show()
        return
    
    # Calculate BMI
    if is_metric:
        height_meters = height / 100
        bmi = weight / (height_meters ** 2)
    else:
        bmi = (weight * 703) / (height ** 2)
    
    bmi = round(bmi, 1)
    
    # Display result
    result_display.SetLabel(f"{bmi}")
    
    # Determine category and color
    if bmi < 16:
        category = "Severe Underweight"
        color = wx.Colour(100, 150, 255)  # Light Blue
        cat_simple = "Underweight"
    elif bmi < 18.5:
        category = "Underweight"
        color = wx.Colour(0, 150, 255)  # Blue
        cat_simple = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
        color = wx.Colour(0, 200, 0)  # Green
        cat_simple = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
        color = wx.Colour(255, 165, 0)  # Orange
        cat_simple = "Overweight"
    elif bmi < 35:
        category = "Obesity Class I"
        color = wx.Colour(255, 100, 0)  # Dark Orange
        cat_simple = "Obesity"
    elif bmi < 40:
        category = "Obesity Class II"
        color = wx.Colour(255, 50, 0)  # Red-Orange
        cat_simple = "Obesity"
    else:
        category = "Obesity Class III"
        color = wx.Colour(255, 0, 0)  # Red
        cat_simple = "Obesity"
    
    # Set colors and labels
    result_display.SetForegroundColour(color)
    category_display.SetLabel(category)
    category_display.SetForegroundColour(color)
    
    # Display health tips
    tips = get_health_tips(cat_simple)
    tips_text = "\n".join(tips)
    tips_display.SetLabel(tips_text)

# Function to clear inputs and results
def clear_inputs(event):
    height_input.SetValue("")
    weight_input.SetValue("")
    result_display.SetLabel("")
    category_display.SetLabel("")
    tips_display.SetLabel("")
    result_display.SetForegroundColour(wx.Colour(0, 0, 0))
    category_display.SetForegroundColour(wx.Colour(0, 0, 0))

# Bind events
unit_choice.Bind(wx.EVT_CHOICE, update_units)
calculate_btn.Bind(wx.EVT_BUTTON, calculate_bmi)
clear_btn.Bind(wx.EVT_BUTTON, clear_inputs)

# Initialize with metric units
update_units(None)

# Set window background color
panel.SetBackgroundColour(wx.Colour(245, 250, 255))

# Make the frame visible
frame.Show()

# Start the event loop
app.MainLoop()
