# PYTHON-JACKFRUIT-PROBLEM

BMI CALCULATOR – PYTHON (wxPython GUI)

A fast, clean, and user-friendly BMI Calculator built using Python and wxPython, capable of handling both Metric and Imperial units.
It computes BMI, assigns the correct category, gives a helpful health tip, and stores every result in a history file for future reference.

📌 Features

✔ Calculate BMI using Metric (cm, kg) or Imperial (inch, lb)

✔ Automatic BMI Category Detection

✔ Dynamic Health Tips

✔ Clean wxPython GUI

✔ bmi_history.txt with auto-saving of all calculations

✔ Layout auto-adjusts during window resizing

✔ Error handling for invalid or missing inputs

🧠 How It Works

The app separates core logic and GUI:

Logic Functions

compute_bmi() – Calculates BMI

get_bmi_category() – Categorizes BMI

get_bmi_tip() – Provides meaningful health advice

get_category_colour() – Chooses display color

save_result_to_file() – Stores history entries

GUI (wxPython)

Clean interface built with BoxSizer layouts

Event-driven functions for:

Calculate BMI

Reset

Switch Units

View History

Maintain UI consistency during window resize

📷 Screenshots

![BMI Calculator Screenshot](path/to/image.png)

📂 File Structure
/
├── bmi_history.txt
├── BMI Calculator.py
├── README.md
└── assets/ (optional for screenshots)

▶ Running the Project
1. Install wxPython
pip install wxPython

2. Run the Program
python "BMI Calculator.py"

📈 Sample Input / Output

Input:

Height: 170 cm

Weight: 65 kg

Output:

BMI: 22.5

Category: Normal Weight

Tip: Maintain your current lifestyle with balanced diet and regular activity

Saved to bmi_history.txt

🔥 Challenges We Faced

Fixing label color resets during window resizing

Sizer layout breaking when window expanded

Handling different units and conversions

Managing wrap(), Refresh(), and Layout() correctly

Debugging malformed file writes

Learning wxPython from scratch

This project taught us event handling, GUI architecture, readability, and debugging in the real world.

🚀 Scope for Future Improvements

Add charts to visualize BMI history

Modern UI redesign

Export history to CSV/PDF

Add age/gender-specific BMI modes

Integrate animations or improved color themes

👥 Team Members

•	Chandru G,     SRN: PES1UG25AM086
•	Karthik. K. R, SRN; PES1UG25AM167
•	Bhavith V C,   SRN: PES1UG25EC061
•	Daksh Nayak,   SRN:

💡 Why We Built This

Because BMI calculators online are cluttered, inaccurate, or filled with ads.
We wanted a clean, offline, reliable tool built entirely by us, learning GUI programming along the way.


