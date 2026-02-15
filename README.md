# Multi-Campus Education Data Preprocessing Pipeline
## FA2 Group Work - Rwanda Polytechnic

**Presentation Date:** February 15, 2026

---

##  Project Overview

This project implements a comprehensive data preprocessing pipeline for integrating student, course, and assessment data from three Rwanda Polytechnic campuses (Huye, Kigali, and Musanze). The pipeline handles real-world data quality issues and creates a clean, analysis-ready "gold" dataset suitable for reporting and machine learning applications.

##  Objectives

- Integrate multi-campus education data with intentional quality issues
- Apply comprehensive data cleaning and preprocessing techniques
- Create engineered features for performance prediction and risk analysis
- Generate professional documentation and visualizations

##  Project Structure

```
Group02- Rwanda Polytechnic-FA2/
├── 01_load_and_profile.py          # Phase 1: Data generation and loading
├── notebooks/
│   ├── 02_cleaning_pipeline.ipynb   # Phase 2: Data cleaning
│   ├── 03_transformation.ipynb      # Phase 3: Transformations
│   ├── 04_integration.ipynb         # Phase 4: Data integration
│   ├── 05_reduction.ipynb           # Phase 5: Data reduction
│   └── 06_feature_engineering.ipynb # Phase 6: Feature engineering
├── raw_data/                        # Raw data from each campus
│   ├── huye/
│   ├── kigali/
│   └── musanze/
└── outputs/                         # Final datasets and reports
```

##  Data Sources

### Campuses
1. **Rwanda Polytechnic Huye (RPH)**
2. **Rwanda Polytechnic Kigali (RPK)**
3. **Rwanda Polytechnic Musanze (RPM)**

### Datasets per Campus
- **Students Dataset:** Student profiles with demographics
- **Courses Dataset:** Course enrollments and academic info
- **Assessments Dataset:** Assessment records with marks and attendance

##  Pipeline Phases

### Phase 1: Data Collection & Loading
**File:** `01_load_and_profile.py`

**Tasks:**
- Generate realistic multi-campus datasets with intentional issues
- Load data from CSV and Excel files
- Add metadata (Campus_ID, Source_Campus_File, Upload_Date)
- Profile data quality issues

**Intentional Issues Created:**
- Missing values (15-25% in various fields)
- Duplicates (3-5% across datasets)
- Outliers (marks <0 or >100, ~2%)
- Inconsistent formats (gender, level, semester, course codes)
- Noisy data (extra spaces, mixed case)

**Outputs:**
- `raw_data/{campus}/students.csv`
- `raw_data/{campus}/courses.csv`
- `raw_data/{campus}/assessments.xlsx`
- `outputs/raw_*_combined.csv`

---

### Phase 2: Data Cleaning
**File:** `notebooks/02_cleaning_pipeline.ipynb`

**Tasks:**
1. **Missing Data:**
   - Visualize missing values with bar charts
   - Impute Gender with mode
   - Fill DOB with default date
   - Drop rows with missing critical fields (Course_Code)
   - Impute marks and attendance with median/mean

2. **Duplicates:**
   - Remove duplicate Student_IDs (keep latest upload)
   - Remove duplicate course enrollments
   - Remove duplicate assessments (keep highest mark)

3. **Outliers:**
   - Detect marks outside 0-100 range
   - Set outliers to NaN and impute with median
   - Recalculate grades after mark correction

4. **Format Standardization:**
   - Gender: M/F/Male/Female → Male/Female
   - Level: L4/L5/L6 → Level 4/5/6
   - Semester: S1/SEM1 → Semester 1
   - Course codes: uppercase, no hyphens
   - Dates: standardize to YYYY-MM-DD

5. **Noisy Data:**
   - Trim spaces from names
   - Title case for names
   - Validate numeric fields

**Outputs:**
- `students_cleaned.csv`
- `courses_cleaned.csv`
- `assessments_cleaned.csv`
- `cleaning_summary_report.csv`

---

### Phase 3: Data Transformation
**File:** `notebooks/03_transformation.ipynb`

**Tasks:**
1. **Scaling:**
   - StandardScaler on Attendance_Rate (mean=0, std=1)

2. **Encoding:**
   - One-hot encode Campus_Name (3 binary columns)
   - One-hot encode Assessment_Type (5 binary columns)
   - One-hot encode Program (6 binary columns)

3. **Binning:**
   - Performance bands: Fail/Pass/Credit/Distinction
   - Performance_Band_Numeric: 1-4 ordinal encoding
   - Attendance categories: Poor/Fair/Good/Excellent

**Outputs:**
- `students_transformed.csv`
- `courses_transformed.csv`
- `silver_transformed.csv`

---

### Phase 4: Data Integration
**File:** `notebooks/04_integration.ipynb`

**Tasks:**
1. **Merge Operations:**
   - Courses ← Students (on Student_ID)
   - Assessments ← Courses-Students (on Student_ID, Course_Code, Academic_Year, Semester)

2. **Conflict Resolution:**
   - Handle duplicate column suffixes
   - Resolve campus information conflicts
   - Standardize final column structure

3. **Quality Validation:**
   - Verify all merges successful
   - Check for unmatched records
   - Validate data integrity

**Outputs:**
- `gold_integrated.csv` (7,000+ records)

---

### Phase 5: Data Reduction
**File:** `notebooks/05_reduction.ipynb`

**Tasks:**
1. **Remove Irrelevant Columns:**
   - Metadata columns (Source_Campus_File, Upload_Date)
   - Non-analytical fields (Email, Phone)

2. **Remove High Missing Columns:**
   - Columns with >50% missing values

3. **Remove Low-Variance Columns:**
   - Constant value columns

**Outputs:**
- `gold_reduced.csv`
- `reduction_report.csv`

---

### Phase 6: Feature Engineering
**File:** `notebooks/06_feature_engineering.ipynb`

**Engineered Features (18 total):**

**A) Date-Time Features (5):**
- `assessment_month` - Month of assessment
- `assessment_weekday` - Day of week (0-6)
- `is_weekend_assessment` - Binary flag
- `assessment_year` - Year of assessment
- `assessment_quarter` - Quarter (1-4)

**B) Student Performance Features (8):**
- `student_course_count` - Number of courses enrolled
- `student_avg_mark` - Average mark across all assessments
- `student_max_mark` - Highest mark achieved
- `student_min_mark` - Lowest mark achieved
- `student_fail_count` - Number of failed assessments (<40)
- `student_total_credits_earned` - Credits from passing grades
- `student_mark_std` - Standard deviation of marks
- `student_assessment_count` - Total assessments taken

**C) Risk Flags (5):**
- `is_at_risk` - Binary flag (avg_mark < 50 OR fails >= 2)
- `low_attendance_flag` - Attendance < 70%
- `high_performer` - Average mark >= 70
- `struggling_student` - Multiple risk criteria
- `excellent_attendance` - Attendance >= 90%

**Visualizations:**
- Chart 1: Missing values analysis
- Chart 2: Mark distribution (4 subplots)
- Chart 3: At-risk students by campus (4 subplots)

**Outputs:**
- `gold_features.csv` (FINAL DATASET)
- `chart1_missing_values.png`
- `chart2_mark_distribution.png`
- `chart3_at_risk_analysis.png`

---

##  Final Dataset Summary

**Gold Features Dataset (`gold_features.csv`):**
- **Records:** 56,896 assessment records
- **Students:** 4,500 unique students
- **Courses:** 10 unique courses
- **Campuses:** 3 campuses
- **Total Features:** 60+ columns
  - Core fields: 20
  - Transformed features: 15
  - Engineered features: 18
  - Encoded features: 10+

**Data Quality Metrics:**
- Missing values: < 1% (only in non-critical fields) handled :100%
- Duplicates: 0 (all removed)
- Outliers: 0 (all treated)
- Format consistency: 100%

---

##  Key Insights

### Performance Analysis
- **Average Mark:** 62.5 across all campuses
- **Performance Distribution:**
  - Distinction (70-100): 35%
  - Credit (50-69): 42%
  - Pass (40-49): 15%
  - Fail (0-39): 8%

### Risk Analysis
- **At-Risk Students:** 18-22% per campus
- **High Performers:** 35% of students
- **Struggling Students:** 8% need immediate intervention

### Campus Comparison
- Performance varies by 3-5% across campuses
- All campuses show similar distribution patterns
- Kigali campus has slightly higher average marks

---

##  Technologies Used

- pip install -r requirements.txt

- **Python 3.12**
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **matplotlib** - Visualization
- **seaborn** - Statistical visualization
- **scikit-learn** - Preprocessing and scaling
- **openpyxl** - Excel file handling

---

##  How to Run

### 1. Generate Data and Run Phase 1
```bash
python 01_load_and_profile.py
```

### 2. Run Notebooks in Order
Open and run each notebook sequentially:
1. `02_cleaning_pipeline.ipynb`
2. `03_transformation.ipynb`
3. `04_integration.ipynb`
4. `05_reduction.ipynb`
5. `06_feature_engineering.ipynb`

Each notebook is self-contained and includes:
- Clear step-by-step cells
- Comprehensive comments
- Progress indicators
- Visualization outputs

---

##  Deliverables Checklist

- [x] Phase 1: Data generation and profiling
- [x] Phase 2: Comprehensive cleaning pipeline
- [x] Phase 3: Transformations (scaling, encoding, binning)
- [x] Phase 4: Data integration
- [x] Phase 5: Data reduction
- [x] Phase 6: Feature engineering (18 features)
- [x] Final datasets (gold_integrated.csv, gold_features.csv)
- [x] 3 visualization charts
- [x] Documentation and code comments
- [x] Before/after metrics and reports

---

##  Use Cases

The final gold dataset is ready for:

1. **Reporting & Analytics:**
   - Student performance dashboards
   - Campus comparison reports
   - Program effectiveness analysis

2. **Machine Learning:**
   - Performance prediction models
   - Dropout risk classification
   - Student clustering and segmentation
   - Grade prediction systems

3. **Decision Support:**
   - Early warning systems
   - Resource allocation
   - Intervention program targeting

---

##  Team Information

**Group Members:** 3 students 
**Institution:** Rwanda Polytechnic  
**Course:** FA2 - Data Preprocessing

---

## Timeline

- **Start Date:** February 07, 2026
- **Duration:** 1 week
- **Presentation:** February 16, 2026


## Contact

For questions or support, please contact your group members or course instructor.

---

**© 2026 Rwanda Polytechnic - Group02- Rwanda Polytechnic-FA2**
