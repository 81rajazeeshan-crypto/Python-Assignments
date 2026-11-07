### Task 11 | Multi-File Student Gradebook
### Concepts: File handling, dictionaries, exceptions
### Problem: Merge students.csv (student_id,name) and scores.csv (student_id,subject,marks). Calculate per-student average, grade, and rank; export report.csv.
### Requirements: Marks must be 0–100; reject unknown IDs and duplicate student-subject entries. Grades: A>=85, B>=70, C>=55, D>=40, otherwise F. Rank by average, then ID.
### Sample / expected behavior: Student 101 with marks 90,80,85 -> average 85.0, grade A.


import csv
import os

def generate_gradebook(students_path, scores_path, report_path):
    # Load students
    students = {}
    with open(students_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s_id = row['student_id'].strip()
            name = row['name'].strip()
            students[s_id] = {"name": name, "scores": {}, "seen_subjects": set()}

    
    with open(scores_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s_id = row['student_id'].strip()
            subject = row['subject'].strip()
            
            if s_id not in students:
                continue  
                
            if subject in students[s_id]["seen_subjects"]:
                continue  
                
            try:
                marks = float(row['marks'].strip())
            except ValueError:
                continue  
                
            if not (0 <= marks <= 100):
                continue  
                
            students[s_id]["seen_subjects"].add(subject)
            students[s_id]["scores"][subject] = marks

    
    report_data = []
    for s_id, data in students.items():
        scores = data["scores"]
        if scores:
            avg = sum(scores.values()) / len(scores)
        else:
            avg = 0.0
            
       
        if avg >= 85:
            grade = 'A'
        elif avg >= 70:
            grade = 'B'
        elif avg >= 55:
            grade = 'C'
        elif avg >= 40:
            grade = 'D'
        else:
            grade = 'F'
            
        report_data.append({
            'student_id': s_id,
            'name': data['name'],
            'average': round(avg, 2),
            'grade': grade
        })

    
    report_data.sort(key=lambda x: (-x['average'], x['student_id']))
    
    # Assign ranks
    for rank, item in enumerate(report_data, start=1):
        item['rank'] = rank

    
    with open(report_path, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['rank', 'student_id', 'name', 'average', 'grade']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in report_data:
            writer.writerow(row)



if __name__ == "__main__":
    stud_file = "students.csv"
    score_file = "scores.csv"
    rep_file = "report.csv"
    
    
    with open(stud_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['student_id', 'name'])
        writer.writerow(['101', 'Ali'])
        writer.writerow(['102', 'Sara'])
        
   
    with open(score_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['student_id', 'subject', 'marks'])
        writer.writerow(['101', 'Math', '90'])
        writer.writerow(['101', 'English', '80'])
        writer.writerow(['101', 'Science', '85'])
        writer.writerow(['102', 'Math', '60'])
        writer.writerow(['102', 'English', '70'])
        
    generate_gradebook(stud_file, score_file, rep_file)
    
    print("--- Report CSV Content ---")
    with open(rep_file, 'r', encoding='utf-8') as f:
        print(f.read())
        
   
    for path in [stud_file, score_file, rep_file]:
        if os.path.exists(path):
            os.remove(path)