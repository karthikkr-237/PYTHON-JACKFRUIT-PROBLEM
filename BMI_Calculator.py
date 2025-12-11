import wx

# ---------- Pure logic functions ----------

def compute_bmi(height_cm, weight_kg):
    """Return BMI given height in cm and weight in kg."""
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m * height_m)
    return bmi

def get_bmi_category(bmi):
    """Return BMI category string based on BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_bmi_tip(category):
    """Return a short health tip/message for the given category."""
    if category == "Underweight":
        return "You are below the usual range. Consider increasing healthy calories and building strength."
    elif category == "Normal weight":
        return "You are in the recommended range. Maintain it with a balanced diet and regular activity."
    elif category == "Overweight":
        return "You are above the usual range. Small, steady changes in food and movement can help."
    else:  # "Obese"
        return "You are well above the usual range. Talk to a doctor for a safe, personal health plan."

def get_category_colour(category):
    """Return a strong, high-contrast colour based on BMI category."""
    if category == "Underweight":
        return wx.Colour(0, 180, 255)      # Bright Cyan
    elif category == "Normal weight":
        return wx.Colour(0, 230, 0)        # Neon Green
    elif category == "Overweight":
        return wx.Colour(255, 170, 0)      # Amber / Orange
    else:
        return wx.Colour(255, 60, 60)      # Strong Red

def save_result_to_file(height_str, weight_str, unit_mode, bmi, category):
    """Append one line of result to bmi_history.txt."""
    try:
        with open("bmi_history.txt", "a", encoding="utf-8") as f:
            f.write(f"{height_str},{weight_str},{unit_mode},{bmi:.1f},{category}\n")
    except Exception:
        # Do not crash app if file write fails
        pass


# ---------- Event handlers (GUI + logic connection) ----------

def on_units_change(event):
    """Update labels when unit selection changes."""
    selection = units_box.GetSelection()
    if selection == 0:  # Metric
        height_label.SetLabel("Height (cm):")
        weight_label.SetLabel("Weight (kg):")
    else:  # Imperial
        height_label.SetLabel("Height (inch):")
        weight_label.SetLabel("Weight (lb):")

    # Clear previous result
    bmi_label.SetLabel("BMI = --")
    category_title_label.SetLabel("Category:")
    category_value_label.SetLabel("--")
    tip_label.SetLabel("")
    history_info_label.SetLabel("")


def on_reset(event):
    """Clear all inputs and outputs."""
    height_input.SetValue("")
    weight_input.SetValue("")

    bmi_label.SetLabel("BMI = --")
    category_title_label.SetLabel("Category:")
    category_value_label.SetLabel("--")
    tip_label.SetLabel("")
    history_info_label.SetLabel("")

    # Reset colours back to default
    default_text = wx.Colour(0, 0, 0)   # black text (since your bg is light)
    bmi_label.SetForegroundColour(default_text)
    category_title_label.SetForegroundColour(default_text)
    category_value_label.SetForegroundColour(default_text)
    tip_label.SetForegroundColour(wx.Colour(80, 80, 80))


def on_calculate(event):
    """Read inputs, compute BMI, show category and tip, save history."""
    height_text = height_input.GetValue().strip()
    weight_text = weight_input.GetValue().strip()

    if height_text == "" or weight_text == "":
        wx.MessageBox("Please enter both height and weight.", "Missing Input",
                      wx.OK | wx.ICON_WARNING)
        return

    # Convert text to numbers safely
    try:
        height_value = float(height_text)
        weight_value = float(weight_text)
    except ValueError:
        wx.MessageBox("Height and weight must be numbers.", "Invalid Input",
                      wx.OK | wx.ICON_ERROR)
        return

    if height_value <= 0 or weight_value <= 0:
        wx.MessageBox("Height and weight must be positive values.", "Invalid Input",
                      wx.OK | wx.ICON_ERROR)
        return

    # Check unit mode (0 = Metric, 1 = Imperial)
    selection = units_box.GetSelection()

    if selection == 0:
        unit_mode = "Metric"
        height_cm = height_value             # already in cm
        weight_kg = weight_value             # already in kg
    else:
        unit_mode = "Imperial"
        # Convert inches and pounds to cm and kg
        height_cm = height_value * 2.54      # 1 inch = 2.54 cm
        weight_kg = weight_value * 0.453592  # 1 lb   = 0.453592 kg

    # Now use pure functions
    bmi = compute_bmi(height_cm, weight_kg)
    bmi = round(bmi, 1)  # round to 1 decimal
    category = get_bmi_category(bmi)
    tip = get_bmi_tip(category)

    # Show result text
    bmi_label.SetLabel(f"BMI : {bmi:.1f}")
    category_title_label.SetLabel("Category:")
    category_value_label.SetLabel(category)

    # Colour based on category
    colour = get_category_colour(category)
    bmi_label.SetForegroundColour(colour)
    category_title_label.SetForegroundColour(colour)
    category_value_label.SetForegroundColour(colour)
    tip_label.SetForegroundColour(colour)

    # Show tip below (and wrap so it doesn’t get cut)
    tip_label.SetLabel("Tip: " + tip)
    tip_label.Wrap(330)   # adjust wrap width to window

    # Save to file for history
    save_result_to_file(height_text, weight_text, unit_mode, bmi, category)
    history_info_label.Wrap(430)


def on_view_history(event):
    """Open a simple dialog to show saved BMI history."""
    try:
        with open("bmi_history.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        wx.MessageBox("No history found yet. Calculate at least one BMI first.",
                      "History", wx.OK | wx.ICON_INFORMATION)
        return

    if content.strip() == "":
        wx.MessageBox("History file is empty.", "History",
                      wx.OK | wx.ICON_INFORMATION)
        return

    wx.MessageBox(content, "BMI History", wx.OK | wx.ICON_INFORMATION)


# ---------- GUI creation ----------

app = wx.App()

# made window bigger: height + width
frame = wx.Frame(None, title="BMI Calculator (Enhanced)", size=(580, 480))
panel = wx.Panel(frame)

# Heading
title = wx.StaticText(panel, label="BMI CALCULATOR")
title_font = title.GetFont()
title_font.PointSize = 16
title_font = title_font.Bold()
title.SetFont(title_font)

# Unit selection
units_box = wx.RadioBox(
    panel,
    label="Units",
    choices=["Metric (cm, kg)", "Imperial (inch, lb)"],
    majorDimension=1,
    style=wx.RA_SPECIFY_ROWS
)

# Labels and inputs
height_label = wx.StaticText(panel, label="Height (cm):")
weight_label = wx.StaticText(panel, label="Weight (kg):")

height_input = wx.TextCtrl(panel)
weight_input = wx.TextCtrl(panel)

# Buttons
calc_button = wx.Button(panel, label="Calculate BMI")
reset_button = wx.Button(panel, label="Reset")
history_button = wx.Button(panel, label="View History")

# Result + category + tip labels
bmi_label = wx.StaticText(panel, label="BMI : --")

# split category into title + value
category_title_label = wx.StaticText(panel, label="Category:")
category_value_label = wx.StaticText(panel, label="--")

tip_label = wx.StaticText(panel, label="")
history_info_label = wx.StaticText(panel, label="")

# Make result font bigger and bold
result_font = bmi_label.GetFont()
result_font.PointSize += 2
result_font = result_font.Bold()
bmi_label.SetFont(result_font)
category_title_label.SetFont(result_font)
category_value_label.SetFont(result_font)

# Tip slightly smaller
tip_font = tip_label.GetFont()
tip_font.PointSize -= 1
tip_label.SetFont(tip_font)
tip_label.SetForegroundColour(wx.Colour(80, 80, 80))

# Layout using vertical BoxSizer
main_sizer = wx.BoxSizer(wx.VERTICAL)

main_sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
main_sizer.Add(units_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

main_sizer.Add(height_label, 0, wx.LEFT | wx.TOP, 10)
main_sizer.Add(height_input, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

main_sizer.Add(weight_label, 0, wx.LEFT | wx.TOP, 10)
main_sizer.Add(weight_input, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

# Buttons row
btn_row = wx.BoxSizer(wx.HORIZONTAL)
btn_row.Add(calc_button, 1, wx.RIGHT, 5)
btn_row.Add(reset_button, 1, wx.RIGHT, 5)
btn_row.Add(history_button, 1, wx.LEFT, 0)
main_sizer.Add(btn_row, 0, wx.EXPAND | wx.ALL, 10)

# Results
main_sizer.Add(bmi_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)

# category: title + value stacked
main_sizer.Add(category_title_label, 0, wx.ALIGN_CENTER | wx.TOP, 4)
main_sizer.Add(category_value_label, 0, wx.ALIGN_CENTER | wx.TOP, 0)

main_sizer.Add(tip_label, 0, wx.ALIGN_CENTER | wx.TOP, 8)


panel.SetSizer(main_sizer)

# Bind events
units_box.Bind(wx.EVT_RADIOBOX, on_units_change)
calc_button.Bind(wx.EVT_BUTTON, on_calculate)
reset_button.Bind(wx.EVT_BUTTON, on_reset)
history_button.Bind(wx.EVT_BUTTON, on_view_history)

frame.Centre()
frame.Show()
app.MainLoop()

