# 🚀 BMI Calculator

A powerful and elegant **BMI Calculator** built with **Python** and **wxPython**, designed to help users monitor and improve their health. This project is a proof of our teamwork, learning, and innovation over long hours of development.

---

## 📌 Project Highlights
- **Interactive GUI:** Built from scratch using **wxPython** with a clean, stable, and user-friendly interface.
- **Dual Unit Support:** Calculates BMI using **Metric (kg/cm)** and **Imperial (lbs/in)** units.
- **Smart Health Tips:** Provides customized health advice based on BMI categories.
- **Dynamic Color-coded Results:** Visual BMI outcomes with color-coding for clarity.
- **Auto-saving History:** All BMI calculations get automatically logged into `bmi_history.txt`.
- **Error Handling:** Gracefully handles invalid and empty inputs.
- **Responsive Design:** Maintains a clean GUI even when the window is resized.
- **Beginner-Friendly:** Intuitive layout, lightweight, and straightforward usage.

---

## 🌟 Features at a Glance
### Core Features:
- Metric & Imperial input support  
- Accurate BMI Calculation based on **WHO Standards**  
- BMI category detection (Underweight, Healthy, Overweight, Obesity)  
- Auto-logged history of calculations  

### Advanced Features:
- **Personalized Health Tips:** Tailored advice based on BMI results.  
- **Activity Level Classifications:** 5 activity levels from sedentary to highly active.  
- **Auto-saving Records:** Keeps all BMI results handy in a text file.  
- **Advanced Input Validation:** Catches common input errors and ensures accurate results.  
- **Dynamic UI Updates:** Color-coded results and enhanced layout management.  

---

## 🔀 How We Built It

### **Backend: Business Logic**
Our backend focuses on simplicity and precision. Key functions include:
- **`compute_bmi()`** → Calculates BMI accurately based on input units.  
- **`get_bmi_category()`** → Classifies BMI into categories (WHO standards).  
- **`get_bmi_tip()`** → Offers health advice.  
- **`save_result_to_file()`** → Logs calculation records into `bmi_history.txt`.  

### **Frontend: The GUI**
We designed the GUI using **wxPython**, with key GUI components as:
- Radio buttons for unit selection.  
- Input fields for height & weight (dynamic based on measurement units).  
- Buttons for **Calculate**, **Reset**, and **View History**.  
- Interactive dialogs for BMI history.  

**What makes the GUI stand out?**  
- **Persistent UI Design:** Aligned, color-coded layouts prevent design breaks.  
- **Window Resizing Support:** Improves user experience by maintaining consistent layouts.  

---

## 📂 Project Structure
```
/
├── BMI_Calculator.py   # Main application script
├── README.md           # Project documentation
└── assets/             # [Optional] Screenshots and media
```

---

## 🚀 Sample Input & Output
### Example Scenario:
**Input:**
- Height: 170 cm  
- Weight: 65 kg  
- Units: Metric  

**Output:**
- **BMI:** 22.5  
- **Category:** Normal Weight  
- **Tip:** "Maintain your current lifestyle with a balanced diet and regular activity."  
- Action: Results saved to `bmi_history.txt`.  

---

## 💡 Why This Project Stands Out
This project didn’t just focus on **building a functional BMI calculator**. It teaches **end-to-end software development**:
- **Planning:** Designing a health tool that users love.  
- **Coding:** Implementing advanced Python constructs seamlessly.  
- **Debugging:** Fixing UI quirks and improving responsiveness.  
- **UI/UX:** Building solutions even for corner-edge cases.  

It reflects our creativity, teamwork, problem-solving skills, and pride as developers.

---

## 🔧 Installation Guide
### Dependencies:
- **Python 3.8+**  
- **wxPython** for GUI.  
To install wxPython:  
```bash
pip install wxPython
```

### Running the Application
1. Clone the repository:
    ```bash
    git clone https://github.com/karthikkr-237/PYTHON-JACKFRUIT-PROBLEM.git
    ```
2. Navigate into the directory:
    ```bash
    cd PYTHON-JACKFRUIT-PROBLEM
    ```
3. Run the application:
    ```bash
    python BMI_Calculator.py
    ```

---

## 🛠️ Challenges (& Solutions)
1. **GUI Component Alignment:**  
   - Issue: Colors resetting on maximizing the window.  
   - **Solution:** Defined layout strategies to persist styles dynamically.  

2. **Error Handling:**  
   - Issue: Incorrect or incomplete numeric inputs crashing app.  
   - **Solution:** Introduced comprehensive input sanitization.  

3. **Dynamic UI Resizing:**  
   - Issue: UI components breaking when resized.  
   - **Solution:** Developed responsive layouts using BoxSizers.  

---

## 📊 Future Scope
Here's what we plan to enhance next:
- Export BMI history data to **CSV or PDF.**  
- Introduce a **modern theme** with light/dark modes.  
- Add **graphical BMI timelines** for progress tracking.  
- Support calculations based on age and gender.  
- Develop a **standalone mobile/desktop app version**.  

---

## 🙌 Meet the Team
*(Add your team details here, replacing placeholders)*  
- **Chandru G**    –  PES1UG25AM086   
- **Karthik K R**  –  PES1UG25AM167
- **Daksh Nayak**  –  PES1UG25AM103 
- **Bhavith V C** –  PES1UG25EC061
  
*Together we built something more than just a project — a tool for health!*

---

If you enjoy this project, please **⭐ star the repository**! Contributions and feedback are welcome.
