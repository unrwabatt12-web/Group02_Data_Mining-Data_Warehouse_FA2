import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("="*80)
print("PHASE 1: DATA COLLECTION & LOADING")
print("="*80)

# ============================================================================
# SECTION 1: GENERATE RAW DATA WITH INTENTIONAL ISSUES
# ============================================================================

# Campus configurations
campuses = {
    'HUYE': {'id': 'RPH', 'name': 'Rwanda Polytechnic Huye'},
    'KIGALI': {'id': 'RPK', 'name': 'Rwanda Polytechnic Kigali'},
    'MUSANZE': {'id': 'RPM', 'name': 'Rwanda Polytechnic Musanze'}
}

# Programs offered
programs = ['Computer Science', 'Information Technology', 'Software Engineering', 
            'Electronics', 'Civil Engineering', 'Mechanical Engineering']

# Courses catalog
courses = [
    ('CS101', 'Introduction to Programming', 4),
    ('CS102', 'Data Structures', 5),
    ('CS201', 'Database Systems', 4),
    ('CS202', 'Web Development', 3),
    ('MTH101', 'Calculus I', 4),
    ('MTH102', 'Linear Algebra', 4),
    ('ENG101', 'Technical Writing', 3),
    ('PHY101', 'Physics for Engineers', 4),
    ('CS301', 'Machine Learning', 5),
    ('CS302', 'Cloud Computing', 4)
]

# Assessment types
assessment_types = ['Quiz', 'Assignment', 'Cat', 'Final Exam', 'Final Project']

# Helper function to generate Rwandan names
def generate_rwandan_name():
    first_names = ['Jean', 'Marie', 'Claude', 'Diane', 'Eric', 'Grace', 'Patrick', 
                   'Alice', 'Emmanuel', 'Francine', 'David', 'Sarah', 'Joseph', 
                   'Beatrice', 'Samuel', 'Kevine', 'Benjamin', 'Aline']
    last_names = ['Uwamahoro', 'Niyonzima', 'Mukamana', 'Habimana', 'Ntawukuriryayo',
                  'Mutabazi', 'Kamanzi', 'Uwase', 'Nshimiyimana', 'Iradukunda',
                  'Mugisha', 'Niyibizi', 'Tuyisenge', 'Gasana']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Helper function to generate phone numbers
def generate_phone():
    prefixes = ['078', '079', '072', '073']
    return f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"

# Helper function to generate student ID
def generate_student_id(campus_id, year, seq):
    return f"{campus_id}{year}{seq:04d}"

# ============================================================================
# GENERATE DATA FOR EACH CAMPUS
# ============================================================================

def generate_campus_data(campus_key, num_students=400):
    """Generate datasets for one campus with intentional data issues"""
    
    campus_id = campuses[campus_key]['id']
    campus_name = campuses[campus_key]['name']
    
    print(f"\n{'='*60}")
    print(f"Generating data for {campus_name} ({campus_id})")
    print(f"{'='*60}")
    
    # -------------------------------------------------------------------
    # STUDENTS DATASET
    # -------------------------------------------------------------------
    students_data = []
    intake_years = [2022, 2023, 2024, 2025]
    
    for i in range(num_students):
        intake_year = random.choice(intake_years)
        student_id = generate_student_id(campus_id, intake_year, i+1)
        
        # Introduce missing values intentionally
        gender = random.choice(['M', 'F', 'Male', 'Female', 'f', 'm', None, ''])
        dob = None if random.random() < 0.05 else (
            datetime(random.randint(1998, 2006), random.randint(1, 12), 
                    random.randint(1, 28)).strftime('%Y-%m-%d')
        )
        phone = None if random.random() < 0.08 else generate_phone()
        
        # Introduce inconsistent formats
        name = generate_rwandan_name()
        if random.random() < 0.1:        # Add noise
            name = "  " + name + "  "      # Extra spaces
        if random.random() < 0.05:
            name = name.upper()            # All caps
        if random.random() < 0.05:
            name = name.lower()            # All lowercase
        
        program = random.choice(programs)
        if random.random() < 0.08:           # Inconsistent program names
            program = program.upper()
        
        level = random.choice(['L4', 'L5', 'L6', 'Level 4', 'Level 5', 'Level 6'])
        
        students_data.append({
            'Student_ID': student_id,
            'Full_Name': name,
            'Gender': gender,
            'DOB': dob,
            'Phone': phone,
            'Program': program,
            'Level': level,
            'Intake_Year': intake_year,
            'Email': f"{name.replace(' ', '.').lower()}@rp.ac.rw" if name else None
        })
    
    # Add duplicate students (same ID, slightly different info)
    num_duplicates = int(num_students * 0.03)
    for _ in range(num_duplicates):
        dup_student = random.choice(students_data).copy()
        dup_student['Phone'] = generate_phone()  # Different phone
        students_data.append(dup_student)
    
    students_df = pd.DataFrame(students_data)
    
    # -------------------------------------------------------------------
    # COURSES DATASET
    # -------------------------------------------------------------------
    courses_data = []
    academic_years = ['2023/2024', '2024/2025', '2025/2026']
    semesters = ['Semester 1', 'Semester 2', 'SEM1', 'SEM2', 'S1', 'S2']
    
    for student in students_data[:num_students]:  # Use original students only
        num_courses = random.randint(4, 7)
        enrolled_courses = random.sample(courses, num_courses)
        
        for course_code, course_title, credits in enrolled_courses:
            # Introduce inconsistent course codes
            if random.random() < 0.1:
                course_code_variant = course_code.replace('CS', 'CS-')
            elif random.random() < 0.05:
                course_code_variant = course_code.lower()
            else:
                course_code_variant = course_code
            
            # Missing module codes
            if random.random() < 0.04:
                course_code_variant = None
            
            academic_year = random.choice(academic_years)
            semester = random.choice(semesters)
            
            courses_data.append({
                'Student_ID': student['Student_ID'],
                'Course_Code': course_code_variant,
                'Course_Title': course_title,
                'Credits': credits if random.random() > 0.02 else None,  # Missing credits
                'Academic_Year': academic_year,
                'Semester': semester,
                'Enrollment_Date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
            })
    
    courses_df = pd.DataFrame(courses_data)
    
    # -------------------------------------------------------------------
    # ASSESSMENTS/RESULTS DATASET
    # -------------------------------------------------------------------
    assessments_data = []
    
    for _, enrollment in courses_df.iterrows():
        num_assessments = random.randint(2, 4)
        
        for _ in range(num_assessments):
            assessment_type = random.choice(assessment_types)
            
            # Generate marks with outliers
            if random.random() < 0.02:  # Outliers
                mark = random.choice([120, 150, -5, -10, 999])
            elif random.random() < 0.05:  # Missing marks
                mark = None
            else:
                mark = round(random.uniform(30, 95), 1)
            
            # Inconsistent date formats
            date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y']
            assessment_date = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime(
                random.choice(date_formats)
            )
            
            # Generate attendance with some missing
            attendance = round(random.uniform(60, 100), 1) if random.random() > 0.1 else None
            
            # Calculate grade
            if mark and 0 <= mark <= 100:
                if mark >= 70:
                    grade = 'A'
                elif mark >= 60:
                    grade = 'B'
                elif mark >= 50:
                    grade = 'C'
                elif mark >= 40:
                    grade = 'D'
                else:
                    grade = 'F'
            else:
                grade = None
            
            assessments_data.append({
                'Student_ID': enrollment['Student_ID'],
                'Course_Code': enrollment['Course_Code'],
                'Academic_Year': enrollment['Academic_Year'],
                'Semester': enrollment['Semester'],
                'Assessment_Type': assessment_type,
                'Mark': mark,
                'Grade': grade,
                'Assessment_Date': assessment_date,
                'Attendance_Rate': attendance
            })
    
    # Add duplicate assessments
    num_dup_assessments = int(len(assessments_data) * 0.02)
    for _ in range(num_dup_assessments):
        dup_assessment = random.choice(assessments_data).copy()
        dup_assessment['Mark'] = round(random.uniform(40, 90), 1)  # Different mark
        assessments_data.append(dup_assessment)
    
    assessments_df = pd.DataFrame(assessments_data)
    
    # -------------------------------------------------------------------
    # SAVE TO FILES
    # -------------------------------------------------------------------
    output_dir = f'raw_data/{campus_key.lower()}'
    os.makedirs(output_dir, exist_ok=True)
    
    students_df.to_csv(f'{output_dir}/students.csv', index=False)
    courses_df.to_csv(f'{output_dir}/courses.csv', index=False)
    assessments_df.to_excel(f'{output_dir}/assessments.xlsx', index=False)
    
    print(f"✓ Generated {len(students_df)} student records (with duplicates)")
    print(f"✓ Generated {len(courses_df)} course enrollments")
    print(f"✓ Generated {len(assessments_df)} assessment records (with duplicates)")
    print(f"✓ Files saved to: {output_dir}/")
    
    return students_df, courses_df, assessments_df

# Generate data for all campuses
all_campus_data = {}
for campus in ['HUYE', 'KIGALI', 'MUSANZE']:
    all_campus_data[campus] = generate_campus_data(campus, num_students=1500)  # Increased from 50 to 600

# ============================================================================
# SECTION 2: LOAD AND PROFILE DATA
# ============================================================================

print("\n" + "="*80)
print("DATA LOADING AND PROFILING")
print("="*80)

def load_and_profile_campus(campus_key):
    """Load datasets from a campus and add metadata"""
    
    campus_id = campuses[campus_key]['id']
    campus_name = campuses[campus_key]['name']
    data_dir = f'raw_data/{campus_key.lower()}'
    
    print(f"\n{'='*60}")
    print(f"Loading data for: {campus_name}")
    print(f"{'='*60}")
    
    # Load datasets
    students_df = pd.read_csv(f'{data_dir}/students.csv')
    courses_df = pd.read_csv(f'{data_dir}/courses.csv')
    assessments_df = pd.read_excel(f'{data_dir}/assessments.xlsx')
    
    # Add metadata columns
    students_df['Campus_ID'] = campus_id
    students_df['Campus_Name'] = campus_name
    students_df['Source_Campus_File'] = f'{campus_key.lower()}/students.csv'
    students_df['Upload_Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    courses_df['Campus_ID'] = campus_id
    courses_df['Campus_Name'] = campus_name
    courses_df['Source_Campus_File'] = f'{campus_key.lower()}/courses.csv'
    courses_df['Upload_Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    assessments_df['Campus_ID'] = campus_id
    assessments_df['Campus_Name'] = campus_name
    assessments_df['Source_Campus_File'] = f'{campus_key.lower()}/assessments.xlsx'
    assessments_df['Upload_Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Profile each dataset
    print(f"\n--- Students Dataset Profile ---")
    print(f"Shape: {students_df.shape}")
    print(f"Columns: {list(students_df.columns)}")
    print(f"\nData Types:")
    print(students_df.dtypes)
    print(f"\nMissing Values Count:")
    print(students_df.isnull().sum())
    print(f"\nDuplicate Student IDs: {students_df['Student_ID'].duplicated().sum()}")
    
    print(f"\n--- Courses Dataset Profile ---")
    print(f"Shape: {courses_df.shape}")
    print(f"Columns: {list(courses_df.columns)}")
    print(f"\nMissing Values Count:")
    print(courses_df.isnull().sum())
    
    print(f"\n--- Assessments Dataset Profile ---")
    print(f"Shape: {assessments_df.shape}")
    print(f"Columns: {list(assessments_df.columns)}")
    print(f"\nMissing Values Count:")
    print(assessments_df.isnull().sum())
    print(f"\nMark Statistics:")
    print(assessments_df['Mark'].describe())
    print(f"\nPotential Outliers (Mark < 0 or Mark > 100): {((assessments_df['Mark'] < 0) | (assessments_df['Mark'] > 100)).sum()}")
    
    return {
        'students': students_df,
        'courses': courses_df,
        'assessments': assessments_df
    }

# Load data from all campuses
loaded_data = {}
for campus in ['HUYE', 'KIGALI', 'MUSANZE']:
    loaded_data[campus] = load_and_profile_campus(campus)

# ============================================================================
# SECTION 3: COMBINED PROFILING SUMMARY
# ============================================================================

print("\n" + "="*80)
print("COMBINED DATA PROFILING SUMMARY")
print("="*80)

# Combine all datasets
all_students = pd.concat([loaded_data[c]['students'] for c in ['HUYE', 'KIGALI', 'MUSANZE']], 
                         ignore_index=True)
all_courses = pd.concat([loaded_data[c]['courses'] for c in ['HUYE', 'KIGALI', 'MUSANZE']], 
                        ignore_index=True)
all_assessments = pd.concat([loaded_data[c]['assessments'] for c in ['HUYE', 'KIGALI', 'MUSANZE']], 
                            ignore_index=True)

print(f"\nTotal Students Records: {len(all_students)}")
print(f"Total Courses Enrollments: {len(all_courses)}")
print(f"Total Assessment Records: {len(all_assessments)}")

print(f"\n--- Key Data Quality Issues Identified ---")
print(f"1. Missing Values:")
print(f"   - Students with missing Gender: {all_students['Gender'].isnull().sum()}")
print(f"   - Students with missing DOB: {all_students['DOB'].isnull().sum()}")
print(f"   - Students with missing Phone: {all_students['Phone'].isnull().sum()}")
print(f"   - Courses with missing Course_Code: {all_courses['Course_Code'].isnull().sum()}")
print(f"   - Assessments with missing Mark: {all_assessments['Mark'].isnull().sum()}")

print(f"\n2. Duplicates:")
print(f"   - Duplicate Student IDs: {all_students['Student_ID'].duplicated().sum()}")
print(f"   - Duplicate Assessment Records: {all_assessments.duplicated(subset=['Student_ID', 'Course_Code', 'Assessment_Type', 'Academic_Year', 'Semester']).sum()}")

print(f"\n3. Outliers:")
outliers = all_assessments[(all_assessments['Mark'].notna()) & 
                          ((all_assessments['Mark'] < 0) | (all_assessments['Mark'] > 100))]
print(f"   - Invalid Marks (< 0 or > 100): {len(outliers)}")
if len(outliers) > 0:
    print(f"   - Outlier values: {sorted(outliers['Mark'].unique())}")

print(f"\n4. Inconsistent Formats:")
print(f"   - Gender value variations: {all_students['Gender'].value_counts().to_dict()}")
print(f"   - Level value variations: {all_students['Level'].value_counts().to_dict()}")
print(f"   - Semester value variations: {all_courses['Semester'].value_counts().to_dict()}")

print(f"\n5. Noisy Data:")
# Check for leading/trailing spaces
names_with_spaces = all_students[all_students['Full_Name'].notna() & 
                                 ((all_students['Full_Name'].str.startswith(' ')) | 
                                  (all_students['Full_Name'].str.endswith(' ')))]
print(f"   - Names with leading/trailing spaces: {len(names_with_spaces)}")

# Make sure the directory exists
os.makedirs('Outputs', exist_ok=True)

# Save combined raw datasets for next phase
all_students.to_csv('Outputs/raw_students_combined.csv', index=False)
all_courses.to_csv('Outputs/raw_courses_combined.csv', index=False)
all_assessments.to_csv('Outputs/raw_assessments_combined.csv', index=False)

print(f"\n{'='*80}")
print("PHASE 1 COMPLETED SUCCESSFULLY")
print(f"{'='*80}")
print(f"\nRaw data files saved to: raw_data/")
print(f"Combined datasets saved to: outputs/")
print(f"\nNext Step: Run 02_cleaning_pipeline.ipynb")