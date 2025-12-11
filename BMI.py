import wx
import math

# Create the application
app = wx.App()

# Create the main window
frame = wx.Frame(None, title="BMI Calculator", size=(500, 500))

# Create a panel to hold widgets
panel = wx.Panel(frame)

# Create font for title
title_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

# Create font for results
result_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

# Title
title = wx.StaticText(panel, label="BMI Calculator")
title.SetFont(title_font)

# Unit system selection
unit_label = wx.StaticText(panel, label="Select Unit System:")
unit_choice = wx.Choice(panel, choices=["Metric (kg, cm)", "Imperial (lbs, inches)"])
unit_choice.SetSelection(0)  # Default to metric

# Input fields
height_label = wx.StaticText(panel, label="Height:")
height_input = wx.TextCtrl(panel, size=(100, -1))

weight_label = wx.StaticText(panel, label="Weight:")
weight_input = wx.TextCtrl(panel, size=(100, -1))

# Unit labels that will update based on selection
height_unit = wx.StaticText(panel, label="cm")
weight_unit = wx.StaticText(panel, label="kg")

# Calculate button
calculate_btn = wx.Button(panel, label="Calculate BMI")

# Clear button
clear_btn = wx.Button(panel, label="Clear")

# Result display
result_label = wx.StaticText(panel, label="Your BMI:")
result_display = wx.StaticText(panel, label="")
result_display.SetFont(result_font)

# Category display
category_label = wx.StaticText(panel, label="Category:")
category_display = wx.StaticText(panel, label="")
category_display.SetFont(result_font)

# BMI Categories reference
categories_label = wx.StaticText(panel, label="BMI Categories:")
categories_text = wx.StaticText(panel, label="Underweight: < 18.5\nNormal weight: 18.5 - 24.9\nOverweight: 25 - 29.9\nObesity: ≥ 30")

# Create a GridSizer for better layout
grid_sizer = wx.GridBagSizer(10, 15)  # Vertical and horizontal gaps

# Add widgets to the GridSizer
grid_sizer.Add(title, pos=(0, 0), span=(1, 4), flag=wx.ALIGN_CENTER | wx.TOP, border=20)
grid_sizer.Add(unit_label, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
grid_sizer.Add(unit_choice, pos=(1, 1), span=(1, 2), flag=wx.EXPAND)

grid_sizer.Add(height_label, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
grid_sizer.Add(height_input, pos=(2, 1), flag=wx.EXPAND)
grid_sizer.Add(height_unit, pos=(2, 2), flag=wx.ALIGN_CENTER_VERTICAL)

grid_sizer.Add(weight_label, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
grid_sizer.Add(weight_input, pos=(3, 1), flag=wx.EXPAND)
grid_sizer.Add(weight_unit, pos=(3, 2), flag=wx.ALIGN_CENTER_VERTICAL)

# Button row
grid_sizer.Add(calculate_btn, pos=(4, 1), flag=wx.EXPAND | wx.TOP, border=15)
grid_sizer.Add(clear_btn, pos=(4, 2), flag=wx.EXPAND | wx.TOP, border=15)

# Results
grid_sizer.Add(result_label, pos=(5, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
grid_sizer.Add(result_display, pos=(5, 1), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)

grid_sizer.Add(category_label, pos=(6, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=20)
grid_sizer.Add(category_display, pos=(6, 1), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)

# Categories reference
grid_sizer.Add(categories_label, pos=(7, 0), flag=wx.TOP, border=30)
grid_sizer.Add(categories_text, pos=(8, 0), span=(1, 3), flag=wx.LEFT, border=20)

# Configure column proportions
grid_sizer.AddGrowableCol(1)

# Create a main sizer for the panel
main_sizer = wx.BoxSizer(wx.VERTICAL)
main_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)

# Set the sizer for the panel
panel.SetSizer(main_sizer)

# Function to update unit labels
def update_units(event):
    selection = unit_choice.GetSelection()
    if selection == 0:  # Metric
        height_unit.SetLabel("cm")
        weight_unit.SetLabel("kg")
    else:  # Imperial
        height_unit.SetLabel("inches")
        weight_unit.SetLabel("lbs")

# Function to calculate BMI
def calculate_bmi(event):
    # Get selected unit system
    is_metric = (unit_choice.GetSelection() == 0)
    
    # Get input values
    height_str = height_input.GetValue()
    weight_str = weight_input.GetValue()
    
    # Validate inputs
    if not height_str or not weight_str:
        result_display.SetLabel("Please enter both values")
        result_display.SetForegroundColour(wx.Colour(255, 0, 0))  # Red for error
        category_display.SetLabel("")
        return
    
    try:
        height = float(height_str)
        weight = float(weight_str)
        
        if height <= 0 or weight <= 0:
            result_display.SetLabel("Values must be positive")
            result_display.SetForegroundColour(wx.Colour(255, 0, 0))  # Red for error
            category_display.SetLabel("")
            return
    
    except ValueError:
        result_display.SetLabel("Invalid number format")
        result_display.SetForegroundColour(wx.Colour(255, 0, 0))  # Red for error
        category_display.SetLabel("")
        return
    
    # Calculate BMI based on unit system
    if is_metric:
        # Metric: BMI = weight(kg) / (height(m))^2
        # Convert cm to meters: height in cm / 100
        height_meters = height / 100
        bmi = weight / (height_meters ** 2)
    else:
        # Imperial: BMI = (weight(lbs) * 703) / (height(in))^2
        bmi = (weight * 703) / (height ** 2)
    
    # Round to 1 decimal place
    bmi = round(bmi, 1)
    
    # Display result with appropriate color
    result_display.SetLabel(f"{bmi}")
    
    # Determine category and color
    if bmi < 18.5:
        category = "Underweight"
        color = wx.Colour(0, 150, 255)  # Blue
    elif bmi < 25:
        category = "Normal weight"
        color = wx.Colour(0, 250, 0)  # Green
    elif bmi < 30:
        category = "Overweight"
        color = wx.Colour(255, 165, 0)  # Orange
    else:
        category = "Obesity"
        color = wx.Colour(255, 0, 0)  # Red
    
    # Set the color for both displays
    result_display.SetForegroundColour(color)
    category_display.SetLabel(category)
    category_display.SetForegroundColour(color)

# Function to clear inputs and results
def clear_inputs(event):
    height_input.SetValue("")
    weight_input.SetValue("")
    result_display.SetLabel("")
    category_display.SetLabel("")

# Bind events
unit_choice.Bind(wx.EVT_CHOICE, update_units)
calculate_btn.Bind(wx.EVT_BUTTON, calculate_bmi)
clear_btn.Bind(wx.EVT_BUTTON, clear_inputs)

# Set window background color
panel.SetBackgroundColour(wx.Colour(240, 250, 255))

# Make the frame visible
frame.Show()

# Start the event loop
app.MainLoop()
