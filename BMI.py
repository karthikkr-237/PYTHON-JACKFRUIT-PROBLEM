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
title = wx.StaticText(panel, label="BMI Calculator", pos=(150, 20))
title.SetFont(title_font)

# Unit system selection
unit_label = wx.StaticText(panel, label="Select Unit System:", pos=(50, 70))
unit_choice = wx.Choice(panel, choices=["Metric (kg, cm)", "Imperial (lbs, inches)"], pos=(200, 65))
unit_choice.SetSelection(0)  # Default to metric

# Input fields - FIXED: Correct positions
height_label = wx.StaticText(panel, label="Height:", pos=(50, 120))
height_input = wx.TextCtrl(panel, pos=(200, 115), size=(100, -1))  # Changed from 155 to 115

weight_label = wx.StaticText(panel, label="Weight:", pos=(50, 160))
weight_input = wx.TextCtrl(panel, pos=(200, 155), size=(100, -1))  # Changed from 115 to 155

# Unit labels that will update based on selection
height_unit = wx.StaticText(panel, label="cm", pos=(310, 120))
weight_unit = wx.StaticText(panel, label="kg", pos=(310, 160))

# Calculate button
calculate_btn = wx.Button(panel, label="Calculate BMI", pos=(180, 210))

# Result display
result_label = wx.StaticText(panel, label="Your BMI:", pos=(50, 270))
result_display = wx.StaticText(panel, label="", pos=(200, 270))
result_display.SetFont(result_font)

# Category display
category_label = wx.StaticText(panel, label="Category:", pos=(50, 310))
category_display = wx.StaticText(panel, label="", pos=(200, 310))
category_display.SetFont(result_font)

# BMI Categories reference
categories_label = wx.StaticText(panel, label="BMI Categories:", pos=(50, 370))
categories_text = wx.StaticText(panel, label="Underweight: < 18.5\nNormal weight: 18.5 - 24.9\nOverweight: 25 - 29.9\nObesity: ≥ 30", pos=(50, 400))

# Function to update unit labels
def update_units(event):
    selection = unit_choice.GetSelection()
    if selection == 0:  # Metric
        height_unit.SetLabel("cm")
        weight_unit.SetLabel("kg")
    else:  # Imperial
        height_unit.SetLabel("inches")
        weight_unit.SetLabel("lbs")

# Function to calculate BMI - FIXED: Correct metric calculation
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
    
    
    try:
        height = float(height_str)
        weight = float(weight_str)
        
        if height <= 0 or weight <= 0:
            result_display.SetLabel("Values must be positive")
            result_display.SetForegroundColour(wx.Colour(255, 0, 0))  # Red for error
            category_display.SetLabel("")
    
    except ValueError:
        result_display.SetLabel("Invalid number format")
        result_display.SetForegroundColour(wx.Colour(255, 0, 0))  # Red for error
        category_display.SetLabel("")

    
    # Calculate BMI based on unit system - FIXED: Correct metric formula
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

# Clear button
clear_btn = wx.Button(panel, label="Clear", pos=(300, 210))

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