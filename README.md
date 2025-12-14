# 🚀 BMI CALCULATOR – PYTHON (wxPython GUI)

A clean, reliable, and fully functional **BMI Calculator** built by our team using **Python** and **wxPython**.  
This project wasn’t just an assignment — it was a journey where we learned GUI development from scratch, solved bugs that made us question reality, and built something we’re genuinely proud of.

---

## 📌 Project Overview
This BMI Calculator:
- Computes BMI using **Metric (cm, kg)** and **Imperial (inch, lb)**.
- Classifies the result into the correct **BMI Category**.
- Displays a meaningful **Health Tip** based on the category.
- Automatically logs every BMI calculation into **bmi_history.txt**.
- Maintains a clean and stable UI even on window resizing.
- Handles invalid/empty inputs gracefully.

This project reflects our collective effort, debugging sessions, and the grind of learning wxPython from ground zero.

---

## 🧠 Features at a Glance
- ✔️ Metric & Imperial unit support  
- ✔️ Dynamic BMI category detection  
- ✔️ Smart health tips  
- ✔️ Auto-saving calculation history  
- ✔️ Clean GUI layout using BoxSizers  
- ✔️ Color-coded results for clarity  
- ✔️ Persistent UI color states on resizing  
- ✔️ Beginner-friendly & lightweight  

---

## 🛠️ How We Built It

### **Core Logic (Backend)**
We separated logic and GUI for clarity and maintainability.

- `compute_bmi()` → Calculates BMI  
- `get_bmi_category()` → Categorizes BMI  
- `get_bmi_tip()` → Suggests a quick health tip  
- `get_category_colour()` → Chooses the display color  
- `save_result_to_file()` → Appends results to `bmi_history.txt`  

### **wxPython GUI (Frontend)**
This is where the real struggle was —  
alignments breaking, colors resetting, resizing issues… everything.

We built:
- Radio buttons for unit selection  
- Input fields for height & weight  
- Buttons for Calculate, Reset & View History  
- Dynamic labels for BMI, category & tips  
- A history viewer using message dialogs  

And then we patched issues like:
- Colors resetting on maximization  
- Wrapped text overflowing  
- Sizers breaking layout  

Finally, the GUI became stable and clean.

---

## 📂 Project Structure
```
/
├── BMI Calculator.py
├── README.md
└── assets/ 
```

---

## 📈 Sample Input & Output

**Input**
- Height: 170 cm  
- Weight: 65 kg  
- Units: Metric  

**Output**
- BMI = 22.5  
- Category: Normal Weight  
- Tip: Maintain your current lifestyle with balanced diet and regular activity  
- Saved automatically to bmi_history.txt  

---

## 🔥 Challenges We Faced
This project tested us in ways we didn’t expect:

- Fixing color resets on window resizing  
- Layouts breaking due to long text wraps  
- Managing `Layout()`, `Wrap()`, `Refresh()` correctly  
- Handling incorrect numeric inputs  
- Debugging history file write issues  
- Learning wxPython from scratch  

Each of these forced us to think, experiment, and improve our understanding of GUI programming.

---

## 🚀 Scope for Future Enhancements
- A more modern and animated GUI  
- Export BMI history to CSV or PDF  
- Graphical charts for BMI progression  
- Age/gender-based BMI evaluation  
- Dark mode UI  
- Mobile/desktop app versions  

---

## 👥 Team Members  
  
- Chandru G – SRN : PES1UG25AM086  
- Karthik. K. R – SRN : PES1UG25AM167 
- Bhavith V C – SRN : PES1UG25EC061  
- Daksh Nayak – SRN : PES1UG25AM103  

---

## 💡 Why This Project Matters
This wasn’t just code.  
It was hours of trial, error, debugging, fixing, breaking, rebuilding, and learning how real software development works.

It resembles **our struggles**, **our teamwork**, and **our growth as developers**.

---

## ▶️ How to Run the Project

### 1. Install Dependencies
```bash
pip install wxPython
```

### 2. Run the App
```bash
python "BMI Calculator.py"
```

---

If you like this project or found it helpful, consider ⭐ starring the repository!
