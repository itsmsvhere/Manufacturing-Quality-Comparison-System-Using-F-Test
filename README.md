# Manufacturing Quality Comparison Analyzer
## F-Test Statistical Analysis Application

---

## 📋 TABLE OF CONTENTS
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Features](#features)
4. [How to Use](#how-to-use)
5. [Statistical Background](#statistical-background)
6. [CSV Format Requirements](#csv-format-requirements)
7. [Troubleshooting](#troubleshooting)
8. [Technical Details](#technical-details)

---

## 💾 INSTALLATION

### System Requirements
- Python 3.8 or higher
- Windows, macOS, or Linux
- At least 100MB free disk space

### Step 1: Install Python Dependencies
Open a terminal/command prompt and run:

```bash
pip install customtkinter pandas matplotlib scipy numpy reportlab
```

Or, to install from the requirements file (if available):

```bash
pip install -r requirements.txt
```

### Required Libraries Explained
- **customtkinter**: Modern GUI framework (modern dark theme)
- **pandas**: Data manipulation and CSV reading
- **matplotlib**: Graph generation and visualization
- **scipy**: Statistical functions (F-test)
- **numpy**: Numerical computations
- **reportlab**: PDF report generation (optional but recommended)

### Step 2: Download the Application
Download `manufacturing_quality_analyzer.py` and save it to a folder on your computer.

### Step 3: Run the Application
Navigate to the folder in terminal and run:

```bash
python manufacturing_quality_analyzer.py
```

The application window should appear within 2-3 seconds.

---

## 🚀 QUICK START

### 5-Minute Quick Start

1. **Prepare Data**
   - Ensure you have two CSV files with "Measurement" columns
   - See CSV Format Requirements section below

2. **Launch Application**
   ```bash
   python manufacturing_quality_analyzer.py
   ```

3. **Upload Data**
   - Click "📁 Upload CSV" under Plant 1
   - Select your Plant 1 CSV file
   - Repeat for Plant 2

4. **Analyze**
   - Click "🔬 Analyze Data" button
   - Wait for analysis to complete (~1-2 seconds)

5. **View Results**
   - Statistics appear in "Statistics Results" tab
   - Visualizations appear in "Visualizations" tab

6. **Export (Optional)**
   - Click "📊 Export as PDF" to save results as PDF report

---

## ✨ FEATURES

### Core Features
✅ Modern, intuitive dark-mode GUI  
✅ CSV file upload for two manufacturing plants  
✅ Automatic F-Test statistical analysis  
✅ Comprehensive statistical calculations:
   - Mean and standard deviation
   - Variance (sample variance)
   - F-statistic and p-value
   - Degrees of freedom
   - Hypothesis test conclusion at α=0.05

✅ Publication-quality visualizations:
   - Combined boxplot comparison
   - Separate histograms for each plant
   - Mean lines and distribution shapes

✅ Clear result interpretation  
✅ PDF report export  
✅ Reset functionality  

### Advanced Features
- Threading for responsive UI during analysis
- Robust error handling for invalid data
- Professional formatting and documentation
- Academic-grade statistical implementation

---

## 📖 HOW TO USE

### Step-by-Step Guide

#### 1. Prepare Your Data
Your CSV file must have:
- At least one column named exactly "Measurement"
- Numeric values (integers or decimals)
- Minimum 2 data points per plant (more is better)

Example CSV structure:
```
Measurement
98.5
99.2
101.1
102.3
98.9
```

#### 2. Launch Application
```bash
python manufacturing_quality_analyzer.py
```

#### 3. Upload Plant 1 Data
- Click **"📁 Upload CSV"** button under "Plant 1 Data"
- Select your Plant 1 CSV file
- Filename and record count will display

#### 4. Upload Plant 2 Data
- Click **"📁 Upload CSV"** button under "Plant 2 Data"
- Select your Plant 2 CSV file
- Filename and record count will display

#### 5. Analyze Data
- Click **"🔬 Analyze Data"** button
- Application performs F-Test automatically
- Results display in "Statistics Results" tab
- Visualizations display in "Visualizations" tab

#### 6. Review Results
The application displays:
- **Executive Summary**: Which plant has better consistency
- **Descriptive Statistics**: Mean, variance, standard deviation
- **F-Test Results**: F-statistic, degrees of freedom, p-value
- **Hypothesis Test Conclusion**: Whether variances are significantly different
- **Interpretation**: Plain-language explanation of results

#### 7. View Visualizations
Click the **"Visualizations"** tab to see:
- **Boxplot**: Comparison of data distributions
- **Plant 1 Histogram**: Distribution shape
- **Plant 2 Histogram**: Distribution shape

#### 8. Export Results (Optional)
- Click **"📊 Export as PDF"** button
- Choose a location to save the PDF
- Professional report is generated automatically

#### 9. Reset (Optional)
- Click **"🔄 Reset All"** to clear all data
- Confirm when prompted
- Application returns to initial state

---

## 📊 STATISTICAL BACKGROUND

### What is F-Test?

The F-Test is a statistical hypothesis test that compares the **variances** (consistency) 
of two independent samples.

### Hypotheses

**Null Hypothesis (H₀):** σ₁² = σ₂²  
The variances of both plants are equal (same consistency)

**Alternative Hypothesis (H₁):** σ₁² ≠ σ₂²  
The variances are different (different consistency)

### The F-Statistic

F = Variance₁ / Variance₂

The ratio of the two sample variances. Values far from 1 suggest unequal variances.

### P-Value

The probability of observing an F-statistic as extreme or more extreme if H₀ is true.

- **p-value < 0.05**: Reject H₀ → Variances ARE significantly different
- **p-value ≥ 0.05**: Fail to reject H₀ → Variances are NOT significantly different

### Significance Level (α)

The application uses **α = 0.05** (5% significance level).

This is the standard for most manufacturing and quality control applications.

### Interpretation

**If variances are significantly different:**
- One plant has more consistent quality than the other
- The plant with lower variance has better consistency
- This difference is statistically meaningful

**If variances are similar:**
- Both plants have similar consistency
- Any observed difference could be due to chance
- No significant quality consistency difference

### Assumptions

1. Data are approximately normally distributed
2. Samples are independent
3. Data are continuous measurements

---

## 📁 CSV FORMAT REQUIREMENTS

### Required Format

Your CSV file MUST have:

1. A column named exactly **"Measurement"** (case-sensitive)
2. Numeric values (can be integers or decimals)
3. No special characters in numeric values

### Valid Example

```csv
Measurement
100.5
101.2
99.8
100.1
102.3
99.9
101.5
100.2
```

### Invalid Examples

❌ Column named "measurement" (lowercase)
```csv
measurement
100.5
101.2
```

❌ Non-numeric values
```csv
Measurement
"very good"
100.5
101.2
```

❌ Missing values (empty cells)
```csv
Measurement
100.5

101.2
```

### Tips for CSV Creation

**In Excel:**
1. Create column with header "Measurement"
2. Enter numeric values in cells below
3. Save as CSV: File → Save As → Format: CSV (Comma delimited)

**In Google Sheets:**
1. Create column with header "Measurement"
2. Enter numeric values
3. Download as CSV: File → Download → CSV

**Using Text Editor:**
```
Measurement
100.5
101.2
99.8
102.1
```

---

## 🔧 TROUBLESHOOTING

### Application won't start

**Problem:** "ModuleNotFoundError: No module named 'customtkinter'"

**Solution:**
```bash
pip install customtkinter --upgrade
```

### "Measurement column not found" Error

**Problem:** Error when uploading CSV file

**Solution:**
- Open your CSV file in a text editor
- Ensure the first row has exactly: `Measurement`
- Check for spelling and capitalization
- Remove any extra spaces or quotes

### "Non-numeric values in Measurement column" Error

**Problem:** Can't process data

**Solution:**
- Open CSV file
- Remove any text values (like "N/A", "null", or labels)
- Keep only numeric values
- Remove empty cells

### Application is frozen

**Problem:** GUI becomes unresponsive

**Solution:**
- The application uses threading, so freezing shouldn't occur
- If it does, wait 5-10 seconds for analysis to complete
- Try resetting (🔄 Reset All) and restarting

### PDF export doesn't work

**Problem:** "reportlab library not installed"

**Solution:**
```bash
pip install reportlab
```

### Results tab is blank

**Problem:** Can't see analysis results

**Solution:**
- Click "🔬 Analyze Data" button again
- Wait for analysis to complete (button shows "⏳ Analyzing...")
- Results should appear automatically

---

## 🔬 TECHNICAL DETAILS

### Algorithm Implementation

#### F-Test Calculation

```
1. Calculate sample variance for each plant:
   var₁ = Σ(x - mean₁)² / (n₁ - 1)
   var₂ = Σ(x - mean₂)² / (n₂ - 1)

2. Calculate F-statistic:
   F = max(var₁, var₂) / min(var₁, var₂)

3. Determine degrees of freedom:
   df₁ = n₁ - 1
   df₂ = n₂ - 1

4. Calculate p-value (two-tailed):
   p-value = 2 × P(F > f_stat)

5. Compare p-value to α = 0.05:
   If p-value < 0.05: Reject H₀
   Otherwise: Fail to reject H₀
```

### Code Structure

- **load_data()**: CSV loading and validation
- **perform_f_test()**: Statistical calculations
- **generate_graphs()**: Visualization creation
- **ManufacturingQualityApp**: Main GUI class

### Software Architecture

- **GUI Framework**: CustomTkinter (modern dark-mode)
- **Data Processing**: Pandas DataFrame
- **Statistics**: SciPy stats module
- **Visualization**: Matplotlib
- **Threading**: Python threading module (non-blocking UI)

### Data Validation

The application validates:
- File format (CSV)
- Required column presence ("Measurement")
- Data type (numeric)
- Sample size (minimum 2 points)
- No empty or missing values

---

## 📝 EXAMPLE USAGE SCENARIO

### Scenario: Comparing Two Manufacturing Plants

**Situation:**
- Plant A produces automotive parts
- Plant B also produces same parts
- Need to compare consistency (variance) of measurements

**Data Collection:**
- Measure 50 parts from each plant
- Record measurement in mm

**Process:**
1. Create plant_a.csv with 50 measurements
2. Create plant_b.csv with 50 measurements
3. Run application
4. Upload both files
5. Click "Analyze Data"
6. Review results:
   - If p-value < 0.05: Plants have different consistency
   - If p-value ≥ 0.05: Plants have similar consistency
7. Export PDF report for documentation

**Decision Making:**
- If Plant A has better consistency: Continue with current procedures
- If Plant B has better consistency: Investigate Plant A's processes
- If similar: No significant difference in consistency

---

## 📚 ACADEMIC REFERENCES

### F-Test References
- Walpole, R. E., et al. (2012). Probability & Statistics for Engineers & Scientists
- Montgomery, D. C. (2012). Design and Analysis of Experiments
- Casella, G., & Berger, R. L. (2002). Statistical Inference

### Statistical Quality Control
- Montgomery, D. C. (2013). Introduction to Statistical Quality Control
- Ryan, T. P. (2011). Statistical Methods for Quality Improvement

---

## 📞 SUPPORT

### Common Questions

**Q: Can I use the same CSV file twice?**  
A: Yes, but it would test if the same plant has significantly different variance from itself (should fail to reject H₀).

**Q: What if my data isn't normally distributed?**  
A: The F-Test is relatively robust to non-normality with larger sample sizes (n>20).

**Q: How many measurements do I need?**  
A: Minimum 2 per plant, but 20+ per plant is recommended for robust results.

**Q: Can I modify the significance level?**  
A: Currently set to 0.05. To change, edit `Config.SIGNIFICANCE_LEVEL` in the code.

**Q: What file size can I upload?**  
A: Files up to several MB are supported. No practical limit for typical manufacturing data.

---

## 📄 LICENSE AND ATTRIBUTION

This application is provided as-is for academic and professional use.

**Author:** Manufacturing Quality Analysis Team  
**Version:** 1.0.0  
**Created:** 2025  

---

## VERSION HISTORY

### Version 1.0.0 (Initial Release)
- Core F-Test functionality
- Modern GUI with dark theme
- CSV file upload and validation
- Comprehensive statistical analysis
- Publication-quality visualizations
- PDF report export
- Robust error handling
- Professional documentation

---

**Last Updated:** February 2025  
**Status:** Production Ready  

For questions or issues, please review the Troubleshooting section or check the application code comments.
