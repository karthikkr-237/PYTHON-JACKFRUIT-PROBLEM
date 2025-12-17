# BMI Health Assistant - College Project

A desktop application built with Python to calculate Body Mass Index (BMI) and track health metrics with support for both metric and imperial units. 

---

## Project Overview

The BMI Health Assistant is a graphical user interface (GUI) application that helps users: 
- Calculate their BMI using standard WHO formulas
- Switch between Metric (kg/cm) and Imperial (lbs/ft/in) units
- Track multiple users' BMI history
- View BMI trends through interactive charts
- Export health data to CSV files
- Get personalized health recommendations

This project demonstrates Python GUI programming, data visualization, and object-oriented programming concepts.

---

## Technologies & Libraries Used

| Library | Purpose | Version |
|---------|---------|---------|
| **wxPython** | GUI framework for creating the desktop interface | 4.0+ |
| **Matplotlib** | Plotting BMI trend charts | 3.0+ |
| **csv** | Exporting data to CSV format | Built-in |
| **datetime** | Handling dates and timestamps | Built-in |
| **collections** | Managing user history with defaultdict | Built-in |

---

## Installation Guide

### Step 1: Install Python
Download and install Python 3.8 or higher from [python.org](https://www.python.org/)

Verify installation:
```bash
python --version
```

### Step 2: Install Required Libraries
Open your terminal/command prompt and run: 

```bash
pip install wxPython
pip install matplotlib
```

### Step 3: Download the Code
Save the code as `bmi_calculator.py` on your computer.

### Step 4: Run the Application
Navigate to the folder containing the file: 
```bash
cd path/to/your/folder
```

Run the program:
```bash
python bmi_calculator.py
```

---

## How to Use the Application

### 1. Launching the Program
When you run the program, a window opens with:
- **Left side**: Input form and results
- **Right side**: Charts and calculation history

### 2. Selecting Measurement Units
At the top, choose your preferred unit system:
- **Metric (kg/cm)**: For kilograms and centimeters
- **Imperial (lbs/ft/in)**: For pounds and feet/inches

The input fields will automatically adjust based on your selection.

### 3. Entering Your Information

Fill in all required fields: 

**Personal Details:**
- **Full Name**: Enter your name (e.g., "John Doe")
- **Age**: Select age from 1 to 120 years
- **Gender**: Choose Male, Female, or Other
- **Activity Level**: Select from 5 activity options: 
  - Sedentary (little or no exercise)
  - Lightly Active (light exercise 1-3 days/week)
  - Moderately Active (moderate exercise 3-5 days/week)
  - Very Active (hard exercise 6-7 days/week)
  - Extra Active (very hard exercise & physical job)

**Physical Measurements:**

*For Metric: *
- **Height (cm)**: Enter height in centimeters (50-250 cm)
- **Weight (kg)**: Enter weight in kilograms (10-300 kg)

*For Imperial:*
- **Height**:  Enter feet (1-8) and inches (0-11. 9)
- **Weight (lbs)**: Enter weight in pounds (20-660 lbs)

### 4. Calculating BMI
Click the **"Calculate BMI"** button.  The application will: 
- Validate all inputs
- Calculate your BMI
- Display results with color coding
- Show your BMI category
- Calculate ideal weight range
- Provide personalized health tips
- Add entry to history
- Update the trend chart

### 5. Understanding the Results

**BMI Value Display:**
- Shows your BMI as a large number
- Color-coded for quick understanding: 
  - **Blue** = Underweight (BMI < 18.5)
  - **Green** = Normal Weight (BMI 18.5-24.9)
  - **Orange** = Overweight (BMI 25-29.9)
  - **Red** = Obese (BMI ≥ 30)

**Category Display:**
- Shows your weight classification
- Based on WHO standards for adults
- Simplified categories for children (under 18)

**Ideal Weight Range:**
- Shows healthy weight range for your height
- Displayed in your selected unit system
- Based on BMI 18.5-24.9 range

**Health Tips:**
- Personalized recommendations
- Based on your BMI category
- Includes diet and exercise suggestions

### 6. Viewing History
The right panel shows:
- **Person Selector**: Choose specific person or "All Persons"
- **BMI Trend Chart**: Line graph showing BMI over time with colored zones
- **History Grid**: Table with all past calculations (last 50 entries)

### 7. Exporting Data
To save your data:
1. Click **"Export History"** button (or press Ctrl+S)
2. Choose save location
3. File is saved as CSV format
4. Can be opened in Excel or Google Sheets

### 8. Other Features
- **Reset All**: Clears all input fields
- **Clear History**:  Deletes all stored calculations
- **Dark Mode**: Toggle using View menu or Ctrl+D
- **About**: Shows application information

---

## Code Structure Explanation

### Main Class:  BMICalculator

The entire application is built as a single class that inherits from `wx.Frame`.

```python
class BMICalculator(wx.Frame):
```

### Important Methods Explained

#### 1. `__init__(self)` (Lines 22-33)
**Purpose**:  Initializes the application window

**What it does:**
- Sets window title to "BMI Health Assistant"
- Sets window size to 1280x720 pixels
- Sets minimum size to 1024x576 pixels
- Initializes variables: 
  - `self.dark_mode = False` - Tracks theme setting
  - `self.history = []` - Stores all calculations
  - `self.person_history = defaultdict(list)` - Stores per-person data
  - `self.is_metric = True` - Tracks selected unit system
- Creates custom icon
- Builds the user interface
- Applies default theme

#### 2. `create_icon()` and `create_bitmap_icon()` (Lines 35-51)
**Purpose**: Creates a custom icon for the application window

**How it works:**
- Creates a 32x32 pixel bitmap
- Draws a simple person figure using lines
- Uses blue background (70, 130, 180 RGB)
- White lines for the figure

#### 3. `init_ui(self)` (Lines 53-289)
**Purpose**: Creates the entire user interface

**Structure:**
```
Window
├── Menu Bar
│   ├── File Menu (Export CSV, Export PDF, Exit)
│   ├── View Menu (Dark Mode toggle)
│   └── Help Menu (Health Tips, About)
├── Left Panel
│   ├── Personal Information Box
│   │   ├── Unit Selection (Metric/Imperial)
│   │   ├── Name Input
│   │   ├── Age & Gender
│   │   ├── Activity Level
│   │   ├── Height Input (cm or ft/in)
│   │   └── Weight Input (kg or lbs)
│   ├── Buttons (Calculate BMI, Reset All)
│   ├── BMI Results Box
│   │   ├── BMI Value (large display)
│   │   ├── Category Label
│   │   └── Ideal Weight Range
│   └── Health Tips Box
│       └── Scrollable tips panel
└── Right Panel
    ├── Person Selector
    ├── BMI Trend Chart (if matplotlib available)
    └── Calculation History Grid
        └── Export/Clear buttons
```

**Key UI Elements:**
- **wxPython Sizers**: Used for layout management
  - `wx.BoxSizer` - Arranges items horizontally or vertically
  - `wx.StaticBoxSizer` - Adds border and label around grouped items
  - `wx.GridBagSizer` - Arranges items in a grid
- **Input Controls**:
  - `wx.TextCtrl` - Text input for name
  - `wx.SpinCtrl` - Integer spinner for age and feet
  - `wx.SpinCtrlDouble` - Decimal spinner for height and weight
  - `wx.Choice` - Dropdown menu for gender and activity
  - `wx.RadioBox` - Radio buttons for unit selection
- **Display Controls**:
  - `wx.StaticText` - Non-editable text labels
  - `wx.grid.Grid` - Table for history display
  - `FigureCanvas` - Matplotlib chart embedded in wxPython

#### 4. `on_unit_change(self, event)` (Lines 291-296)
**Purpose**: Handles switching between metric and imperial units

**How it works:**
- Gets selected radio button (0 = Metric, 1 = Imperial)
- Sets `self.is_metric` flag accordingly
- Calls `update_unit_ui()` to show/hide appropriate fields
- Re-layouts the window

#### 5. `update_unit_ui(self)` (Lines 298-320)
**Purpose**: Shows or hides input fields based on selected unit system

**For Metric Mode:**
- Shows: Single height input in cm
- Hides:  Feet and inches inputs
- Weight range:  10-300 kg

**For Imperial Mode:**
- Shows: Separate feet and inches inputs
- Hides:  Centimeter input
- Weight range: 20-660 lbs

#### 6. `on_calculate(self, event)` (Lines 322-428)
**Purpose**: Main calculation function - validates inputs and calculates BMI

**Step-by-step process:**

**Step 1: Get Input Values** (Lines 325-329)
```python
name = self.name_ctrl.GetValue().strip()  # Get and trim name
age_str = self.age_ctrl. GetValue()        # Get age
gender = self.gender_choice. GetStringSelection()  # Get gender
activity = self.activity_choice.GetStringSelection()  # Get activity
```

**Step 2: Validate Inputs** (Lines 331-343)
Checks for: 
- Empty name field
- Missing age
- Unselected gender
- Unselected activity level
If any validation fails, shows error dialog and focuses on problematic field.

**Step 3: Convert Units to Metric** (Lines 345-372)

*If Metric Selected:*
```python
height_cm = self.height_cm_ctrl.GetValue()  # Get height in cm
weight_val = self.weight_ctrl.GetValue()    # Get weight in kg
height_m = height_cm / 100.0                # Convert cm to meters
weight_kg = weight_val                      # Already in kg
```

*If Imperial Selected:*
```python
ft = self.height_ft_ctrl.GetValue()         # Get feet
inches = self.height_in_ctrl.GetValue()     # Get inches
weight_lbs = self.weight_ctrl.GetValue()    # Get pounds

total_inches = (ft * 12) + inches           # Convert to total inches
height_m = total_inches * 0.0254            # Convert inches to meters
weight_kg = weight_lbs * 0.453592           # Convert pounds to kg
```

**Conversion Formulas:**
- 1 inch = 0.0254 meters
- 1 pound = 0.453592 kilograms

**Step 4: Calculate BMI** (Lines 374-376)
```python
bmi = weight_kg / (height_m * height_m)
```
This is the standard WHO formula:  BMI = weight(kg) / height²(m²)

**Step 5: Determine Category** (Line 378)
Calls `get_bmi_category()` which returns category based on BMI value and age. 

**Step 6: Calculate Ideal Weight Range** (Lines 381-384)
```python
ideal_min_kg = 18.5 * (height_m * height_m)  # Minimum healthy weight
ideal_max_kg = 24.9 * (height_m * height_m)  # Maximum healthy weight
```
Based on healthy BMI range of 18.5-24.9

**Step 7: Update Display** (Lines 386-397)
- Shows BMI value with color coding
- Displays category
- Shows ideal weight in user's preferred units
- Converts to Imperial if needed: 
  ```python
  ideal_min_lbs = ideal_min_kg * 2.20462
  ideal_max_lbs = ideal_max_kg * 2.20462
  ```

**Step 8: Generate Health Tips** (Lines 399-400)
Calls `get_personalized_tips()` with all user data.

**Step 9: Store in History** (Lines 402-417)
Creates a dictionary with all data: 
```python
history_entry = {
    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
    'name': name,
    'age': age,
    'gender': gender,
    'activity': activity,
    'bmi': round(bmi, 1),
    'category': category,
    'height': round(height_m * 100, 1),  # Stored in cm
    'weight': round(weight_kg, 1)         # Stored in kg
}
```
**Note**: History is always stored in metric units for consistency.

**Step 10: Update UI Components** (Lines 412-421)
- Adds entry to global history list
- Adds entry to person-specific history
- Updates person dropdown list
- Refreshes history grid
- Updates chart
- Shows status message

**Error Handling** (Lines 423-428)
- Catches `ValueError` for validation errors
- Catches all other exceptions
- Shows user-friendly error dialogs

#### 7. `get_bmi_color(self, bmi)` (Lines 430-434)
**Purpose**: Returns appropriate color for BMI value

**Color Scheme:**
```python
if bmi < 18.5:   return wx. Colour(0, 0, 255)      # Blue (Underweight)
elif bmi < 25:   return wx.Colour(0, 128, 0)      # Green (Normal)
elif bmi < 30:   return wx.Colour(255, 165, 0)    # Orange (Overweight)
else:            return wx.Colour(255, 0, 0)      # Red (Obese)
```

#### 8. `get_bmi_category(self, bmi, age)` (Lines 436-449)
**Purpose**: Determines BMI category based on value and age

**For Adults (18+ years):**
| BMI Range | Category |
|-----------|----------|
| < 16 | Severely Underweight |
| 16 - 18.4 | Underweight |
| 18.5 - 24.9 | Normal Weight |
| 25 - 29.9 | Overweight |
| 30 - 34.9 | Obesity Class I |
| 35 - 39.9 | Obesity Class II |
| 40+ | Obesity Class III |

**For Children (< 18 years):**
Simplified categories (actual pediatric BMI requires percentile charts):
| BMI Range | Category |
|-----------|----------|
| < 5 | Underweight (Child) |
| 5 - 84 | Healthy Weight (Child) |
| 85 - 94 | Overweight (Child) |
| 95+ | Obese (Child) |

#### 9. `get_personalized_tips(self, bmi, category, age, gender, activity, weight, height)` (Lines 451-461)
**Purpose**: Generates personalized health recommendations

**Logic:**
```python
if "Underweight" in category:
    # Weight gain tips
    # - Eat 5-6 small meals
    # - Add healthy fats & protein
    # - Strength train
    
elif "Normal" in category:
    # Maintenance tips
    # - Maintain balanced diet
    # - Regular exercise
    # - Hydration
    
elif "Overweight" or "Obese" in category: 
    # Weight loss tips
    # - Caloric deficit
    # - Increase veggies & fiber
    # - Cardio & weights

# Always adds general tips: 
# - Drink water
# - Sleep 7-9 hours
# - Manage stress
```

Returns combined tips as a single string.

#### 10. `update_tips_display(self, tips)` (Lines 463-471)
**Purpose**: Updates the health tips panel with new content

**How it works:**
- Destroys previous content
- Creates new multiline text control
- Sets text to read-only
- Displays the tips
- Enables scrolling if content is long

#### 11. `update_person_list(self)` (Lines 473-476)
**Purpose**: Updates the person dropdown menu

**How it works:**
- Gets all unique names from `person_history` dictionary
- Sorts alphabetically
- Adds "All Persons" as first option
- Updates dropdown choices
- Selects "All Persons" by default

#### 12. `on_person_selected(self, event)` (Lines 478-479)
**Purpose**: Handles person selection change

Simply calls `update_chart()` to refresh the chart with selected person's data.

#### 13. `update_history_grid(self)` (Lines 481-503)
**Purpose**: Refreshes the history table with latest data

**Process:**
1. Clears existing grid content
2. Deletes all existing rows
3. Loops through last 50 history entries
4. For each entry: 
   - Adds a new row
   - Fills in:  date, name, age, gender, activity, BMI, category
   - Applies color coding to category cell: 
     - Light green for normal BMI
     - Light blue for underweight
     - Orange for overweight
     - Red for obese
   - Sets text color (white for obese, black for others)
5. Auto-sizes columns to fit content

#### 14. `update_chart(self)` (Lines 505-529)
**Purpose**: Creates/updates the BMI trend line chart

**How it works:**

**Step 1: Check if matplotlib is available**
```python
if not MATPLOTLIB_AVAILABLE:  return
```

**Step 2: Clear previous chart**
```python
self.axes.clear()
```

**Step 3: Determine data to plot**
- If "All Persons" selected: use entire history
- If specific person selected: use that person's history only

**Step 4: Plot the data**
- Extracts dates and BMI values from history entries
- Creates line plot with markers
- Adds colored background zones: 
  - Green zone (18.5-25): Normal range
  - Yellow zone (25-30): Overweight range
  - Red zone (30-50): Obese range
- Sets chart title
- Formats x-axis dates

**Step 5: Refresh canvas**
```python
self.canvas.draw()
```

#### 15. `on_reset(self, event)` (Lines 531-543)
**Purpose**: Clears all input fields and resets results display

Resets:
- Name field (empty)
- Age spinner (blank)
- Gender choice (back to "Select Gender")
- Activity choice (back to "Select Activity Level")
- All height fields (cm, ft, in - all blank)
- Weight field (blank)
- BMI result ("--")
- Category ("Category:  --")
- Ideal weight ("Ideal Weight Range: --")
- Tips (back to default message)

#### 16. `on_export_csv(self, event)` (Lines 545-560)
**Purpose**: Exports calculation history to CSV file

**Process:**

**Step 1: Check if data exists**
```python
if not self.history:
    wx.MessageBox("No data to export.", "Export", wx.OK | wx.ICON_WARNING)
    return
```

**Step 2: Show file save dialog**
- Opens file picker
- Filters for . csv files
- Allows overwrite with confirmation

**Step 3: Write CSV file**
```python
fieldnames = ['date', 'name', 'age', 'gender', 'activity', 
              'height_cm', 'weight_kg', 'bmi', 'category']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()  # Writes column headers
for entry in self.history:
    writer.writerow({k: entry[k] for k in fieldnames if k in entry})
```

**CSV Format Example:**
```
date,name,age,gender,activity,height_cm,weight_kg,bmi,category
2025-12-17 14:30,John Doe,25,Male,Moderately Active,175. 0,70.0,22.9,Normal Weight
```

**Step 4: Show success/error message**

#### 17. `on_export_pdf(self, event)` (Lines 562-563)
**Purpose**: PDF export (currently redirects to CSV export)

**Note**: This is a simplified implementation. A full PDF export would require additional libraries like `reportlab` or `fpdf`.

#### 18. `on_clear_history(self, event)` (Lines 565-571)
**Purpose**: Deletes all stored calculation history

**Safety feature**: Shows confirmation dialog before clearing: 
```python
if wx.MessageBox("Clear history?", "Confirm", wx. YES_NO) == wx.YES:
```

**What it clears:**
- `self.history` list (all calculations)
- `self.person_history` dictionary (per-person data)
- History grid display
- Person dropdown list
- BMI trend chart

#### 19. `show_health_tips(self, event)` (Lines 573-574)
**Purpose**: Shows information about health tips feature

Simply displays a message box explaining that tips appear after calculation.

#### 20. `toggle_dark_mode(self, event)` (Lines 576-578)
**Purpose**: Switches between light and dark themes

```python
self.dark_mode = not self.dark_mode  # Toggle boolean
self.apply_theme()                    # Apply new theme
```

#### 21. `apply_theme(self)` (Lines 580-589)
**Purpose**: Applies color scheme based on dark mode setting

**Dark Mode Colors:**
- Background: `wx.Colour(75, 75, 75)` - Dark gray
- Foreground:  `wx.Colour(250, 250, 250)` - Light gray/white

**Light Mode Colors:**
- Uses system default colors
- `wx.SystemSettings.GetColour()` - Gets OS theme colors

#### 22. `on_about(self, event)` (Lines 591-600)
**Purpose**: Shows "About" dialog with application information

Displays:
- Application name:  "BMI Health Assistant"
- Version: "2.0"
- Description of features
- Copyright:  "@ 2025"
- Website link (your GitHub repository)

#### 23. `on_exit(self, event)` (Lines 602-603)
**Purpose**: Closes the application window

```python
self.Close()  # Closes the frame and exits
```

### Main Function

#### `main()` (Lines 605-609)
**Purpose**: Entry point of the application

```python
def main():
    app = wx.App(False)       # Create wxPython application object
    frame = BMICalculator()   # Create main window
    frame.Show()              # Display the window
    app.MainLoop()            # Start event loop (keeps app running)
```

#### `if __name__ == "__main__": ` (Lines 611-612)
**Purpose**: Ensures `main()` only runs when script is executed directly

This allows the file to be imported as a module without automatically running. 

---

## BMI Formula & Calculations

### Standard BMI Formula
```
BMI = weight (kg) / height² (m²)
```

### Example Calculation
For a person who is 175 cm tall and weighs 70 kg: 
```
Height in meters = 175 / 100 = 1.75 m
Height squared = 1.75 × 1.75 = 3.0625 m²
BMI = 70 / 3.0625 = 22.9
Category = Normal Weight
```

### Unit Conversions Used

**Length Conversions:**
```
1 inch = 0.0254 meters
1 foot = 12 inches
1 cm = 0.01 meters
```

**Weight Conversions:**
```
1 pound = 0.453592 kilograms
1 kilogram = 2.20462 pounds
```

### Ideal Weight Calculation
```
Minimum healthy weight = 18.5 × height²(m²)
Maximum healthy weight = 24.9 × height²(m²)
```

For example, at 1.75m height:
```
Min weight = 18.5 × 3.0625 = 56.7 kg
Max weight = 24.9 × 3.0625 = 76.3 kg
```

---

## Features in Detail

### 1. Dual Unit System
- Seamlessly switch between metric and imperial
- All data stored in metric for consistency
- Display automatically converts to user's preferred units
- Height input changes from single field (cm) to two fields (ft/in)

### 2. Multi-User Support
- Track different family members separately
- Each person's data stored in `person_history` dictionary
- Person selector dropdown for individual chart viewing
- Name-based organization

### 3. Data Persistence
- History stored in memory during session
- Export to CSV for permanent storage
- Can import back into Excel/Google Sheets
- Data includes full user profile with timestamp

### 4. Visual Analytics
- Line chart shows BMI progression over time
- Color-coded zones (green/yellow/red)
- Individual or combined view
- Date-based x-axis
- Automatic scaling

### 5. Input Validation
- Checks for empty required fields
- Validates numeric ranges
- Provides specific error messages
- Auto-focuses on problematic field
- Prevents calculation with invalid data

### 6. Color Coding
- Instant visual feedback on health status
- Consistent color scheme throughout app
- Applied to BMI display, history grid, and charts
- Accessibility consideration (not relying on color alone)

---

## Data Structures Used

### 1. History List
```python
self.history = []
```
A simple list storing all calculations chronologically.

**Example entry:**
```python
{
    'date': '2025-12-17 14:30',
    'name':  'John Doe',
    'age': 25,
    'gender': 'Male',
    'activity': 'Moderately Active',
    'bmi': 22.9,
    'category': 'Normal Weight',
    'height':  175.0,  # Always in cm
    'weight': 70.0    # Always in kg
}
```

### 2. Person History Dictionary
```python
self.person_history = defaultdict(list)
```
A dictionary where keys are names and values are lists of that person's calculations.

**Example structure:**
```python
{
    'John Doe': [entry1, entry2, entry3],
    'Jane Smith':  [entry1, entry2]
}
```

Using `defaultdict(list)` means if a name doesn't exist, it automatically creates an empty list. 

---

## Menu System

### File Menu
- **Export to CSV (Ctrl+S)**: Saves all history to CSV file
- **Export to PDF (Ctrl+P)**: Currently saves as CSV
- **Exit (Ctrl+Q)**: Closes application

### View Menu
- **Dark Mode (Ctrl+D)**: Toggles between light/dark theme

### Help Menu
- **Health Tips**: Information about health tips feature
- **About**: Application info and version

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + S` | Export to CSV |
| `Ctrl + P` | Export to PDF |
| `Ctrl + D` | Toggle Dark Mode |
| `Ctrl + Q` | Exit Application |

---

## Error Handling

The application handles various error scenarios:

### Input Validation Errors
- Empty name field
- Missing age value
- Unselected gender
- Unselected activity level
- Height below minimum (50cm or 20 inches)
- Weight below minimum (10kg or 20lbs)

### Runtime Errors
- CSV export failures (permissions, disk space)
- Chart rendering errors (matplotlib issues)
- Unexpected calculation errors

All errors display user-friendly dialog boxes with clear messages.

---

## Limitations

1. **No Data Persistence**: Data is lost when application closes (must export to CSV)
2. **No Database**: Everything stored in memory
3. **Simplified Children's BMI**: Real pediatric BMI requires CDC/WHO percentile charts
4. **No Network Features**: Cannot sync between devices
5. **Basic PDF Export**: Currently just saves as CSV
6. **No User Authentication**: Anyone can see all history
7. **Limited History**: Grid shows only last 50 entries

---

## Future Enhancements

### Possible Improvements: 
1. **Database Integration**: SQLite for permanent storage
2. **User Accounts**: Login system with password protection
3. **Real PDF Reports**: Professional formatted reports with charts
4. **Goal Tracking**: Set target weight and track progress
5. **Reminders**:  Scheduled notifications for weigh-ins
6. **Nutrition Tracking**: Log meals and calories
7. **Exercise Logging**: Track workouts and activities
8. **Body Measurements**: Waist, hip, neck circumference
9. **Multiple Languages**:  Internationalization support
10. **Mobile App**:  Companion Android/iOS app

---

## Troubleshooting

### Problem: Application won't start
**Possible causes:**
- Python not installed correctly
- wxPython not installed

**Solution:**
```bash
pip install --upgrade wxPython
```

### Problem: Charts don't appear
**Cause:** Matplotlib not installed

**Solution:**
```bash
pip install matplotlib
```

### Problem: Error "No module named 'wx'"
**Cause:** wxPython installation failed

**Solution:**
Try installing with specific version:
```bash
pip install wxPython==4.2.0
```

### Problem: Dark mode doesn't change everything
**Cause:** Some wxPython controls use system colors

**Note:** This is expected behavior.  Full dark mode requires more extensive coding.

### Problem: CSV export fails
**Possible causes:**
- No write permission in selected folder
- Disk full
- File is open in another program

**Solution:**
- Choose different folder
- Close file if open
- Check disk space

---

## Project Information

**File Name**:  `bmi_calculator.py`  
**Programming Language**: Python 3.8+  
**Total Lines of Code**: 612  
**Main Class**: BMICalculator  
**Number of Methods**: 23  

**Author**: [Your Name]  
**Roll Number**: [Your Roll Number]  
**Course**: [Your Course Name]  
**Year**: 2025  

---

## References

1. **WHO BMI Classification**  
   https://www.who.int/health-topics/obesity

2. **CDC BMI Information**  
   https://www.cdc.gov/healthyweight/assessing/bmi/

3. **wxPython Documentation**  
   https://docs.wxpython.org/

4. **Matplotlib Documentation**  
   https://matplotlib.org/stable/index.html

5. **Python Official Documentation**  
   https://docs.python.org/3/

---

## License

This project is created for educational purposes as part of a college assignment. 

---

## Contact

For questions or issues regarding this project, please contact through GitHub repository.

---

**Last Updated**: December 2025
