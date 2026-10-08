"""
rules.py - Knowledge Base and Inference Engine for B.Tech Student Performance Advisor
====================================================================================
Expert System / Rule-Based AI architecture:
- Analyzes student academic performance using deterministic IF-THEN rules.
- Supports subject-wise marks entry: calculates average mid (0-30) and semester (0-70) marks automatically.
- In 1st Year 1st Semester: evaluates purely on Mid Exam marks (0-30 scale) since semester exams have not yet occurred.
- In subsequent semesters: evaluates combined Mid (0-30) and End-Semester (0-70) marks (0-100 scale).
- Generates short, concise, and punchy advice without unnecessary length.
"""

from typing import Dict, List, Any


# ==============================================================================
# 1. KNOWLEDGE BASE CONSTANTS & DOMAIN MAPPINGS
# ==============================================================================

BRANCH_OPTIONS = [
    "CSE – Computer Science and Engineering",
    "CST – Computer Science and Technology",
    "ECE – Electronics and Communication Engineering",
    "EEE – Electrical and Electronics Engineering",
    "ME – Mechanical Engineering",
    "Civil Engineering",
    "IT – Information Technology",
    "AI & ML",
    "Data Science",
    "Other"
]

YEAR_OPTIONS = [
    "1st Year",
    "2nd Year",
    "3rd Year",
    "4th Year"
]

SEMESTER_OPTIONS = [
    "1st Semester",
    "2nd Semester"
]

PERFORMANCE_LEVELS = [
    "Excellent",
    "Good",
    "Average",
    "Poor"
]

DIFFICULTY_OPTIONS = [
    "No major difficulty",
    "Difficulty understanding concepts",
    "Poor time management",
    "Difficulty in programming",
    "Difficulty in mathematics",
    "Difficulty in core subjects",
    "Difficulty preparing for exams",
    "Lack of regular study",
    "Low attendance",
    "Other"
]


# ==============================================================================
# 2. DEFAULT B.TECH CURRICULUM SUBJECTS MAPPING
# ==============================================================================

def get_default_subjects(branch: str, year: str) -> List[str]:
    """Provide realistic default B.Tech subjects based on branch and year."""
    is_computer = any(b in branch for b in ["CSE", "CST", "IT", "AI & ML", "Data Science"])
    is_ece = "ECE" in branch
    is_eee = "EEE" in branch
    is_mech = "ME" in branch
    is_civil = "Civil" in branch

    if "1st" in year:
        return [
            "Engineering Mathematics - I",
            "Engineering Physics / Chemistry",
            "Programming in C / Python",
            "Basic Electrical & Electronics",
            "Engineering Graphics & Design"
        ]
    elif "2nd" in year:
        if is_computer:
            return [
                "Data Structures & Algorithms",
                "Digital Logic & Computer Org.",
                "OOP with Java / C++",
                "Discrete Mathematics",
                "Database Management Systems"
            ]
        elif is_ece:
            return [
                "Electronic Devices & Circuits",
                "Signals & Systems",
                "Network Theory",
                "Digital System Design",
                "Probability & Random Processes"
            ]
        elif is_eee:
            return [
                "Electrical Circuit Analysis",
                "DC Machines & Transformers",
                "Analog Electronic Circuits",
                "Electromagnetic Fields",
                "Engineering Mathematics - III"
            ]
        elif is_mech:
            return [
                "Mechanics of Solids",
                "Engineering Thermodynamics",
                "Fluid Mechanics & Machinery",
                "Manufacturing Processes",
                "Material Science"
            ]
        elif is_civil:
            return [
                "Strength of Materials",
                "Fluid Mechanics",
                "Surveying & Geomatics",
                "Building Materials",
                "Engineering Geology"
            ]
        else:
            return [
                "Core Engineering Subject 1",
                "Core Engineering Subject 2",
                "Core Engineering Subject 3",
                "Applied Mathematics",
                "Technical Elective"
            ]
    elif "3rd" in year:
        if is_computer:
            return [
                "Operating Systems",
                "Computer Networks",
                "Automata Theory (TOC)",
                "Software Engineering",
                "Web Technologies"
            ]
        elif is_ece:
            return [
                "Microprocessors & Microcontrollers",
                "Digital Signal Processing",
                "VLSI Design",
                "Control Systems",
                "Antennas & Propagation"
            ]
        elif is_eee:
            return [
                "Power Electronics",
                "Power System Analysis",
                "Control Systems",
                "Microprocessors",
                "Electrical Machine Design"
            ]
        elif is_mech:
            return [
                "Heat & Mass Transfer",
                "Design of Machine Elements",
                "Dynamics of Machinery",
                "IC Engines",
                "CAD / CAM"
            ]
        elif is_civil:
            return [
                "Structural Analysis - II",
                "Design of RC Structures",
                "Geotechnical Engineering",
                "Transportation Engineering",
                "Environmental Engineering"
            ]
        else:
            return [
                "Advanced Core Subject 1",
                "Advanced Core Subject 2",
                "Advanced Core Subject 3",
                "Professional Elective 1",
                "Open Elective"
            ]
    else:  # 4th Year
        return [
            "Professional Elective - I",
            "Professional Elective - II",
            "Professional Elective - III",
            "Engineering Economics & Management",
            "Major Project / Seminar"
        ]


# ==============================================================================
# 3. EVALUATION & CLASSIFICATION FUNCTIONS
# ==============================================================================

def classify_performance(total_marks: float) -> Dict[str, str]:
    """
    Classify student performance based on total marks or percentage score (0-100 scale).
    """
    if total_marks >= 85:
        return {
            "category": "Excellent",
            "badge": "🌟 Excellent",
            "color": "#16A34A",
            "bg_color": "#DCFCE7",
            "summary": "Outstanding academic standing. Maintain consistency for university distinction (8.5+ CGPA)."
        }
    elif total_marks >= 70:
        return {
            "category": "Good",
            "badge": "👍 Good",
            "color": "#2563EB",
            "bg_color": "#DBEAFE",
            "summary": "Strong academic record. Target weaker topics to enter the Distinction tier."
        }
    elif total_marks >= 50:
        return {
            "category": "Average",
            "badge": "📈 Average",
            "color": "#D97706",
            "bg_color": "#FEF3C7",
            "summary": "Passing standing. Consistent daily practice needed to reach First Class."
        }
    else:
        return {
            "category": "Needs Improvement",
            "badge": "⚠️ Needs Improvement",
            "color": "#DC2626",
            "bg_color": "#FEE2E2",
            "summary": "Below passing threshold (50%). Urgent remedial study required."
        }


def classify_attendance(attendance: float) -> Dict[str, str]:
    """Classify attendance percentage."""
    if attendance >= 85:
        return {
            "status": "Excellent",
            "color": "#16A34A",
            "bg_color": "#DCFCE7",
            "message": "Class attendance is exemplary."
        }
    elif attendance >= 75:
        return {
            "status": "Good",
            "color": "#2563EB",
            "bg_color": "#DBEAFE",
            "message": "Meets 75% university eligibility requirement."
        }
    elif attendance >= 65:
        return {
            "status": "Low",
            "color": "#D97706",
            "bg_color": "#FEF3C7",
            "message": "Below 75%. Risk of condonation fines."
        }
    else:
        return {
            "status": "Very Low",
            "color": "#DC2626",
            "bg_color": "#FEE2E2",
            "message": "Critical attendance shortage (<65%). Detention risk!"
        }


# ==============================================================================
# 4. MARK IMPROVEMENT TARGET CALCULATOR
# ==============================================================================

def get_target_improvement_analysis(
    mid_marks: float = 0.0,
    semester_marks: float = 0.0,
    total_marks: float = 0.0,
    is_first_year_first_sem: bool = False,
    cgpa: float = 0.0
) -> Dict[str, Any]:
    """Computes concise mark or CGPA gaps to reach the next tier."""
    if cgpa > 0.0:
        if cgpa >= 9.0:
            target_name = "🏆 University Gold Medal / Top 1% (9.5+ CGPA)"
            marks_needed = round(max(0.0, 9.5 - cgpa), 2)
            action = "Distinction achieved! Focus on research publications, open source contributions, and elite fellowships."
        elif cgpa >= 8.5:
            target_name = "🌟 Tier-1 Elite Distinction (9.0+ CGPA)"
            marks_needed = round(9.0 - cgpa, 2)
            action = f"Need +{marks_needed} CGPA points to reach 9.0+. Secure Grade 'O'/'A+' in 4-credit core subjects."
        elif cgpa >= 7.0:
            target_name = "🌟 University Distinction (8.5+ CGPA)"
            marks_needed = round(8.5 - cgpa, 2)
            action = f"Need +{marks_needed} CGPA points to enter Distinction (8.5+). Aim for Grade 'A+' in semester end exams."
        elif cgpa >= 5.0:
            target_name = "👍 First Class Standing (7.0+ CGPA)"
            marks_needed = round(7.0 - cgpa, 2)
            action = f"Need +{marks_needed} CGPA points to reach First Class (7.0+). Essential benchmark for top corporate drives."
        else:
            target_name = "📈 Passing Threshold (5.0+ CGPA)"
            marks_needed = round(5.0 - cgpa, 2)
            action = f"Need +{marks_needed} CGPA to clear academic probation. Attend remedial sessions and clear all backlogs."

        return {
            "current_total": cgpa,
            "target_name": target_name,
            "marks_needed": marks_needed,
            "action_pathway": action,
            "is_cgpa": True
        }

    if is_first_year_first_sem:
        if mid_marks >= 25.5:
            target_name = "🌟 Distinction Top Standing (28+ / 30)"
            marks_needed = round(max(0.0, 28.5 - mid_marks), 1)
            action = "Distinction level achieved! Keep solving model papers for upcoming finals."
        elif mid_marks >= 21.0:
            target_name = "🌟 Distinction Tier (25.5+ / 30 Mid Marks)"
            marks_needed = round(25.5 - mid_marks, 1)
            action = f"Need +{marks_needed} marks to reach Distinction (85%+). Maximize tutorial assignment scores."
        elif mid_marks >= 15.0:
            target_name = "👍 First Class Tier (21.0+ / 30 Mid Marks)"
            marks_needed = round(21.0 - mid_marks, 1)
            action = f"Need +{marks_needed} marks to reach First Class (70%+). Review test mistakes with faculty."
        else:
            target_name = "📈 Passing Threshold (15.0+ / 30 Mid Marks)"
            marks_needed = round(15.0 - mid_marks, 1)
            action = f"Need +{marks_needed} marks to pass (15/30). Attend remedial sessions and revise standard textbook examples."

        return {
            "current_total": mid_marks,
            "target_name": target_name,
            "marks_needed": marks_needed,
            "action_pathway": action,
            "is_cgpa": False
        }

    # Combined Mid + Semester calculation (0 - 100 scale)
    if total_marks >= 85:
        target_name = "University Top Rank / Gold Medal"
        marks_needed = round(max(0.0, 95.0 - total_marks), 1)
        action = "Distinction band achieved! Focus on error-free exam papers and research projects."
    elif total_marks >= 70:
        target_name = "🌟 Distinction Tier (85+ Marks / 8.5+ CGPA)"
        marks_needed = round(85.0 - total_marks, 1)
        action = f"Need +{marks_needed} marks to enter Distinction. Practice labeled diagrams and structured answers."
    elif total_marks >= 50:
        target_name = "👍 First Class Tier (70+ Marks / 7.0+ CGPA)"
        marks_needed = round(70.0 - total_marks, 1)
        action = f"Need +{marks_needed} marks to reach First Class. Focus on high-weightage question units."
    else:
        target_name = "📈 Passing Threshold (50+ Marks)"
        marks_needed = round(50.0 - total_marks, 1)
        action = f"Need +{marks_needed} marks to clear passing mark. Submit all assignments and revise core definitions."

    return {
        "current_total": total_marks,
        "target_name": target_name,
        "marks_needed": marks_needed,
        "action_pathway": action
    }


# ==============================================================================
# 5. TAILORED BRANCH & YEAR SUGGESTION GENERATORS
# ==============================================================================

def get_academic_suggestions(branch: str, year: str) -> List[str]:
    """Short academic improvement suggestions tailored specifically to Branch AND Year."""
    is_computer = any(b in branch for b in ["CSE", "CST", "IT", "AI & ML", "Data Science"])
    is_circuits = any(b in branch for b in ["ECE", "EEE"])
    is_core_eng = any(b in branch for b in ["ME", "Civil"])

    if "1st" in year:
        return [
            "Mathematics: Practice calculus and differential equations for 45 mins daily.",
            "Basic Sciences: Connect physics and chemistry formulas to laboratory experiments.",
            "Answer Writing: Use neat headings, steps, and labeled diagrams for university exams.",
            "Weekly Revision: Review lecture notes every weekend to prevent last-minute cramming."
        ]
    elif "2nd" in year:
        if is_computer:
            return [
                "Discrete Math: Master set theory, graph theory, and recurrence relations.",
                "Core Theory: Focus on Data Structures, Digital Logic, and Computer Architecture.",
                "Standard Books: Study standard textbooks (Galvin, Cormen) alongside code."
            ]
        elif is_circuits:
            return [
                "Circuit Theory: Solve 5 numericals daily on Network Theorems and AC transients.",
                "Devices & Signals: Clarify semiconductor physics and continuous-time signals.",
                "Formula Sheets: Keep dedicated formula notebooks for nodal and mesh analysis."
            ]
        elif is_core_eng:
            return [
                "Mechanics & Fluids: Practice free-body diagrams (FBD) and SFD/BMD diagrams regularly.",
                "Thermodynamics / Surveying: Master thermodynamic cycles or survey calculation methods.",
                "Engineering Drawing: Practice projections and 3D cross-sectional views."
            ]
        else:
            return [
                "Core Fundamentals: Master 2nd year theoretical foundations of your branch.",
                "Problem Sets: Solve weekly numerical problem sets regularly."
            ]
    elif "3rd" in year:
        if is_computer:
            return [
                "High-Credit Subjects: Dedicate study slots to OS, DBMS, Networks, and Automata.",
                "Algorithmic Analysis: Practice asymptotic complexity and Dynamic Programming.",
                "Mock Papers: Solve full 3-hour university previous question papers."
            ]
        elif is_circuits:
            return [
                "Control Systems & DSP: Master stability criteria (Bode plots) and FFT algorithms.",
                "VLSI & Embedded: Practice CMOS derivations and microcontroller assembly/C code.",
                "Past Papers: Solve 5 years' university questions for high-credit core exams."
            ]
        elif is_core_eng:
            return [
                "Design Elements: Master design standards, load analysis, and heat transfer.",
                "Data Handbooks: Learn to quickly navigate IS / ASME design data handbooks.",
                "Timed Practice: Practice solving multi-step design problems under time limits."
            ]
        else:
            return [
                "Core Specialization: Focus on pre-final year subjects for competitive exams.",
                "Question Banks: Solve comprehensive departmental question banks."
            ]
    else:  # 4th Year
        return [
            "Professional Electives: Focus on advanced elective courses to maximize grade points.",
            "CGPA Protection: Maintain zero backlogs and keep final year CGPA high.",
            "Last-Mile Prep: Prioritize frequent university questions to graduate with Distinction."
        ]


def get_technical_suggestions(branch: str, year: str) -> List[str]:
    """Short technical skill roadmaps."""
    is_computer = any(b in branch for b in ["CSE", "CST", "IT", "AI & ML", "Data Science"])
    is_ece = "ECE" in branch
    is_eee = "EEE" in branch
    is_mech = "ME" in branch
    is_civil = "Civil" in branch

    if is_computer:
        if "1st" in year:
            return [
                "Coding Basics: Master C or Python syntax and loop logic.",
                "Tooling: Set up VS Code, terminal, and create a GitHub profile.",
                "Practice: Solve 30+ beginner problems on HackerRank."
            ]
        elif "2nd" in year:
            return [
                "OOP: Master Java or C++ (Classes, Inheritance, Polymorphism).",
                "DSA: Implement Linked Lists, Stacks, Queues, and Trees from scratch.",
                "Databases: Learn SQL queries (JOINs, GROUP BY) with MySQL."
            ]
        elif "3rd" in year:
            return [
                "LeetCode: Practice 100+ medium problems (Graphs, DP, Trees).",
                "Full-Stack: Build web apps using React, Node.js, or FastAPI.",
                "DevOps: Learn Git, Docker basics, and RESTful APIs."
            ]
        else:
            return [
                "System Design: Study basic HLD, LLD, and database caching.",
                "Placement Coding: Rehearse company-specific coding interview patterns.",
                "Flagship Projects: Polish 2 live projects with documentation on GitHub."
            ]
    elif is_ece:
        if "1st" in year:
            return [
                "Prototyping: Breadboard wiring, multimeter tests, and Ohm's law.",
                "Microcontrollers: Build simple sensor projects using Arduino."
            ]
        elif "2nd" in year:
            return [
                "Circuit Simulation: Use Multisim or LTspice for analog/digital circuits.",
                "HDL: Learn Verilog HDL basics for digital circuit synthesis."
            ]
        elif "3rd" in year:
            return [
                "Embedded RTOS: Work with ESP32, FreeRTOS, and MQTT IoT protocols.",
                "DSP & VLSI: Implement digital filters in MATLAB and learn Vivado."
            ]
        else:
            return [
                "Core Semiconductors: Prepare technical rounds for Qualcomm, TI, Intel.",
                "Firmware: Practice bare-metal drivers and static timing analysis (STA)."
            ]
    elif is_eee:
        if "1st" in year:
            return ["Electrical Basics: Safe wiring, 3-phase power basics, and MATLAB scripting."]
        elif "2nd" in year:
            return ["Simulink: Model transformers and motors in MATLAB/Simulink."]
        elif "3rd" in year:
            return ["Power Electronics: Design DC-DC converters, motor drives, and learn PLC."]
        else:
            return ["EVs & Smart Grid: Study Battery Management Systems (BMS) and renewable power."]
    elif is_mech:
        if "1st" in year:
            return ["CAD: Master AutoCAD 2D drafting and workshop machine skills."]
        elif "2nd" in year:
            return ["3D CAD: Learn SolidWorks or Creo for 3D modeling and GD&T."]
        elif "3rd" in year:
            return ["Simulation: Perform structural FEA and CFD using ANSYS Workbench."]
        else:
            return ["Mechatronics: Integrate sensors, actuators, and prepare for core automotive drives."]
    elif is_civil:
        if "1st" in year:
            return ["AutoCAD: Prepare 2D building plans and learn surveying."]
        elif "2nd" in year:
            return ["BIM: Learn Autodesk Revit and Total Station surveying."]
        elif "3rd" in year:
            return ["Analysis Tools: Master STAAD.Pro or ETABS for 3D structural analysis."]
        else:
            return ["Advanced Design: Multi-story building design and construction management."]
    else:
        return [
            "Programming: Learn Python for data analysis and numerical modeling.",
            "Domain Tools: Master specialized software standard in your branch."
        ]


def get_practical_suggestions(branch: str, year: str) -> List[str]:
    """Short practical skills."""
    if "1st" in year:
        return [
            "Lab Records: Complete observation notes promptly after every practical class.",
            "Instruments: Learn zero-error checks and calibration of meters and calipers.",
            "Lab Safety: Adhere strictly to eye, chemical, and electrical safety standards."
        ]
    elif "2nd" in year:
        return [
            "Core Labs: Perform all departmental experiments independently.",
            "Mini-Project: Form a 3-member team and build a functional mini-project.",
            "Viva Prep: Practice explaining circuit/code logic to external examiners."
        ]
    elif "3rd" in year:
        return [
            "Capstone Project: Build and deploy a working software or hardware prototype.",
            "Certifications: Complete NPTEL or cloud certification courses.",
            "Mock Tests: Practice timed coding assessments and simulation labs."
        ]
    else:
        return [
            "Major Project: Ensure rigorous testing and documentation in final dissertation.",
            "Conference Paper: Aim to publish project results in a peer-reviewed conference.",
            "Project Defense: Rehearse formal technical presentations and examiner viva questions."
        ]


# ==============================================================================
# 6. FORWARD-CHAINING INFERENCE ENGINE & COMPACT ADVICE GENERATOR
# ==============================================================================

def analyze_performance(
    student_name: str,
    branch: str,
    year: str,
    semester: str,
    mid_marks: float = 0.0,
    semester_marks: float = 0.0,
    attendance: float = 75.0,
    study_performance: str = "Good",
    difficulty: str = "No major difficulty",
    subject_scores: List[Dict[str, Any]] = None,
    sgpa: float = 0.0,
    cgpa: float = 0.0,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """
    Inference mechanism executing forward chaining over the Knowledge Base.
    Supports Subject-Wise Mid marks and Overall SGPA/CGPA evaluation.
    """
    is_first_year_first_sem = ("1st" in year and "1st" in semester)
    is_cgpa_mode = (cgpa > 0.0 or sgpa > 0.0)

    # Calculate averages from subject_scores if provided (subject-wise only has Mid marks)
    if subject_scores and len(subject_scores) > 0:
        valid_mids = [float(s.get("mid", 0.0)) for s in subject_scores]
        mid_marks = round(sum(valid_mids) / len(valid_mids), 2)
        semester_marks = 0.0
        is_cgpa_mode = False

    is_mid_only_eval = not is_cgpa_mode and (is_first_year_first_sem or (semester_marks == 0.0))

    if is_cgpa_mode:
        total_marks = round(cgpa * 10.0, 1)
        scaled_percentage = total_marks
        perf_category = classify_performance(scaled_percentage)
    elif is_mid_only_eval:
        total_marks = round(mid_marks, 2)
        scaled_percentage = round((mid_marks / 30.0) * 100.0, 2)
        perf_category = classify_performance(scaled_percentage)
    else:
        total_marks = round(mid_marks + semester_marks, 2)
        scaled_percentage = total_marks
        perf_category = classify_performance(total_marks)

    att_category = classify_attendance(attendance)
    is_computer_branch = any(comp in branch for comp in ["CSE", "CST", "IT", "AI & ML", "Data Science"])

    rules_applied: List[Dict[str, str]] = []
    ai_advice_list: List[str] = []

    # --------------------------------------------------------------------------
    # SUBJECT-WISE SPECIFIC SHORT ADVISORY
    # --------------------------------------------------------------------------
    if subject_scores and len(subject_scores) > 0:
        weak_subjects = [s for s in subject_scores if float(s.get("mid", 0.0)) < 15.0]
        strong_subjects = [s for s in subject_scores if float(s.get("mid", 0.0)) >= 25.0]

        if weak_subjects:
            for s in weak_subjects[:2]:
                rec_weak = f"📚 Weak Subject ({s['name']}): Mid score is {s['mid']}/30. Practice past question papers and clear doubts with faculty."
                rules_applied.append({
                    "rule_id": "Rule-Subject-Remedial",
                    "rule_name": f"Subject Remedial ({s['name']})",
                    "condition": f"Mid Marks in '{s['name']}' < 15 / 30",
                    "student_value": f"{s['name']}: {s['mid']}/30",
                    "recommendation": rec_weak,
                    "badge_type": "warning"
                })
                ai_advice_list.append(rec_weak)

        if strong_subjects:
            names = ", ".join([f"{s['name']} ({s['mid']}/30)" for s in strong_subjects[:2]])
            rec_strong = f"🌟 Strong Subject ({names}): Excellent internal score. Maintain consistency."
            rules_applied.append({
                "rule_id": "Rule-Subject-Mastery",
                "rule_name": "Subject Mastery",
                "condition": "Mid Marks in subject >= 25 / 30",
                "student_value": names,
                "recommendation": rec_strong,
                "badge_type": "success"
            })
            ai_advice_list.append(rec_strong)

    # --------------------------------------------------------------------------
    # RULE SET 1: OVERALL ACADEMIC PERFORMANCE (SHORT FORM)
    # --------------------------------------------------------------------------

    if scaled_percentage >= 85 and attendance >= 85:
        rec = "🌟 Academic Distinction: Excellent performance. Maintain regular revision and prepare for GATE/placements."
        rules_applied.append({
            "rule_id": "Rule 1",
            "rule_name": "Academic Distinction Rule",
            "condition": "Performance Score >= 85% AND Attendance >= 85%",
            "student_value": f"Score: {scaled_percentage}%, Attendance: {attendance}%",
            "recommendation": rec,
            "badge_type": "success"
        })
        ai_advice_list.append(rec)

    elif 70 <= scaled_percentage < 85 and attendance >= 75:
        rec = "👍 Good Standing: Strong score. Review missed test questions to reach Distinction."
        rules_applied.append({
            "rule_id": "Rule 2",
            "rule_name": "First Class Rule",
            "condition": "Performance Score between 70% and 84% AND Attendance >= 75%",
            "student_value": f"Score: {scaled_percentage}%, Attendance: {attendance}%",
            "recommendation": rec,
            "badge_type": "info"
        })
        ai_advice_list.append(rec)

    elif 50 <= scaled_percentage < 70:
        rec = "📈 Average Standing: Increase daily study to 2 hours and solve past 3 years' question papers."
        rules_applied.append({
            "rule_id": "Rule 3",
            "rule_name": "Average Standing Rule",
            "condition": "Performance Score between 50% and 69%",
            "student_value": f"Score: {scaled_percentage}%",
            "recommendation": rec,
            "badge_type": "warning"
        })
        ai_advice_list.append(rec)

    elif scaled_percentage < 50:
        rec = "⚠️ Needs Improvement: Marks are below passing. Attend remedial classes and study 2.5 hours daily."
        rules_applied.append({
            "rule_id": "Rule 4",
            "rule_name": "Critical Recovery Rule",
            "condition": "Performance Score < 50%",
            "student_value": f"Score: {scaled_percentage}%",
            "recommendation": rec,
            "badge_type": "danger"
        })
        ai_advice_list.append(rec)

    # --------------------------------------------------------------------------
    # RULE SET 2: INTERNAL (MID) MARKS SPECIFIC (SHORT FORM)
    # --------------------------------------------------------------------------

    if not is_cgpa_mode:
        if mid_marks < 15:
            rec = f"🎯 Low Mid Marks: Internal average is {mid_marks}/30. Submit all assignments and consult faculty to recover marks."
            rules_applied.append({
                "rule_id": "Rule 5",
                "rule_name": "Low Mid Exam Rule",
                "condition": "Average Mid Exam Marks < 15 / 30",
                "student_value": f"Average Mid: {mid_marks}/30",
                "recommendation": rec,
                "badge_type": "warning"
            })
            ai_advice_list.append(rec)

        elif mid_marks >= 25:
            rec = f"🌟 Strong Mid Marks: High internal average ({mid_marks}/30). Maintain momentum for semester exams."
            rules_applied.append({
                "rule_id": "Rule 5B",
                "rule_name": "Strong Mid Exam Rule",
                "condition": "Average Mid Exam Marks >= 25 / 30",
                "student_value": f"Average Mid: {mid_marks}/30",
                "recommendation": rec,
                "badge_type": "success"
            })
            ai_advice_list.append(rec)

    # --------------------------------------------------------------------------
    # RULE SET 3: INTERNAL VS SEMESTER / CGPA EVALUATION (SHORT FORM)
    # --------------------------------------------------------------------------

    if is_cgpa_mode:
        if cgpa >= 8.5:
            rec_cgpa = f"🌟 Distinction Tier: Outstanding cumulative record ({cgpa:.2f}/10.0 CGPA). Maintain momentum for honors and placement shortlists."
            rules_applied.append({
                "rule_id": "Rule-CGPA-Distinction",
                "rule_name": "CGPA Distinction Rule",
                "condition": "CGPA >= 8.5 / 10.0",
                "student_value": f"CGPA: {cgpa:.2f}",
                "recommendation": rec_cgpa,
                "badge_type": "success"
            })
            ai_advice_list.append(rec_cgpa)
        elif 7.0 <= cgpa < 8.5:
            rec_cgpa = f"👍 First Class Tier: Strong CGPA of {cgpa:.2f}/10.0. Focus on high-credit core subjects to cross the 8.5 distinction cutoff."
            rules_applied.append({
                "rule_id": "Rule-CGPA-FirstClass",
                "rule_name": "CGPA First Class Rule",
                "condition": "CGPA between 7.0 and 8.49",
                "student_value": f"CGPA: {cgpa:.2f}",
                "recommendation": rec_cgpa,
                "badge_type": "info"
            })
            ai_advice_list.append(rec_cgpa)
        elif 5.0 <= cgpa < 7.0:
            rec_cgpa = f"📈 Second Class Tier: Current CGPA is {cgpa:.2f}/10.0. Dedicate 2+ hours daily to raise CGPA above 7.0 for placement cutoffs."
            rules_applied.append({
                "rule_id": "Rule-CGPA-Average",
                "rule_name": "CGPA Average Rule",
                "condition": "CGPA between 5.0 and 6.99",
                "student_value": f"CGPA: {cgpa:.2f}",
                "recommendation": rec_cgpa,
                "badge_type": "warning"
            })
            ai_advice_list.append(rec_cgpa)
        else:
            rec_cgpa = f"⚠️ Critical CGPA Alert: CGPA is {cgpa:.2f}/10.0 (< 5.0). Meet academic counselor immediately and clear all backlogs."
            rules_applied.append({
                "rule_id": "Rule-CGPA-Low",
                "rule_name": "CGPA Low Alert",
                "condition": "CGPA < 5.0",
                "student_value": f"CGPA: {cgpa:.2f}",
                "recommendation": rec_cgpa,
                "badge_type": "warning"
            })
            ai_advice_list.append(rec_cgpa)

        if sgpa > 0.0:
            if sgpa >= cgpa + 0.3:
                rec_sgpa = f"📈 Upward Trend: Current SGPA ({sgpa:.2f}) is higher than cumulative CGPA ({cgpa:.2f}). Outstanding progress!"
                rules_applied.append({
                    "rule_id": "Rule-SGPA-Upward",
                    "rule_name": "Semester Upward Trend",
                    "condition": "SGPA >= CGPA + 0.3",
                    "student_value": f"SGPA: {sgpa:.2f}, CGPA: {cgpa:.2f}",
                    "recommendation": rec_sgpa,
                    "badge_type": "success"
                })
                ai_advice_list.append(rec_sgpa)
            elif sgpa <= cgpa - 0.5:
                rec_sgpa = f"⚠️ Semester Dip: SGPA ({sgpa:.2f}) dropped below cumulative CGPA ({cgpa:.2f}). Focus on high-credit courses."
                rules_applied.append({
                    "rule_id": "Rule-SGPA-Dip",
                    "rule_name": "Semester Dip Alert",
                    "condition": "SGPA <= CGPA - 0.5",
                    "student_value": f"SGPA: {sgpa:.2f}, CGPA: {cgpa:.2f}",
                    "recommendation": rec_sgpa,
                    "badge_type": "warning"
                })
                ai_advice_list.append(rec_sgpa)

    elif not is_mid_only_eval:
        if mid_marks >= 20 and semester_marks < 40:
            rec = f"📝 Exam Preparation: Good internals ({mid_marks}/30) but low semester score ({semester_marks}/70). Practice 3-hour timed mock exams."
            rules_applied.append({
                "rule_id": "Rule 6",
                "rule_name": "Mid vs Sem Imbalance",
                "condition": "Mid Marks >= 20/30 AND Semester Marks < 40/70",
                "student_value": f"Mid: {mid_marks}/30, Sem: {semester_marks}/70",
                "recommendation": rec,
                "badge_type": "warning"
            })
            ai_advice_list.append(rec)

        elif mid_marks < 15 and semester_marks >= 50:
            rec = f"⚖️ Assessment Consistency: Strong semester score ({semester_marks}/70) but low mid marks ({mid_marks}/30). Maintain regular study habits."
            rules_applied.append({
                "rule_id": "Rule 7",
                "rule_name": "Semester Resilience",
                "condition": "Mid Marks < 15/30 AND Semester Marks >= 50/70",
                "student_value": f"Mid: {mid_marks}/30, Sem: {semester_marks}/70",
                "recommendation": rec,
                "badge_type": "info"
            })
            ai_advice_list.append(rec)

        elif mid_marks >= 22 and semester_marks >= 52:
            rec = "🏆 Dual Excellence: Outstanding consistency in both mid and semester exams. Keep it up!"
            rules_applied.append({
                "rule_id": "Rule 7B",
                "rule_name": "Dual Excellence Rule",
                "condition": "Mid Marks >= 22/30 AND Semester Marks >= 52/70",
                "student_value": f"Mid: {mid_marks}/30, Sem: {semester_marks}/70",
                "recommendation": rec,
                "badge_type": "success"
            })
            ai_advice_list.append(rec)
    else:
        if is_first_year_first_sem:
            rec_1st = f"🌱 1st Year 1st Sem Foundation: Average mid score is {mid_marks}/30. Focus on Engineering Mathematics, programming basics, and lab records."
            rules_applied.append({
                "rule_id": "Rule-1stYear1stSem",
                "rule_name": "First Year Foundation",
                "condition": "Year == '1st Year' AND Semester == '1st Semester'",
                "student_value": f"Average Mid: {mid_marks}/30 ({scaled_percentage}%)",
                "recommendation": rec_1st,
                "badge_type": "info"
            })
            ai_advice_list.append(rec_1st)
        else:
            rec_mid = f"📊 Internal Mid Standing: Average mid score is {mid_marks}/30 ({scaled_percentage}%). Prepare for university semester exams."
            rules_applied.append({
                "rule_id": "Rule-MidOnlyStanding",
                "rule_name": "Internal Assessment Standing",
                "condition": "Mid Marks Continuous Evaluation Only",
                "student_value": f"Average Mid: {mid_marks}/30 ({scaled_percentage}%)",
                "recommendation": rec_mid,
                "badge_type": "info"
            })
            ai_advice_list.append(rec_mid)

    # --------------------------------------------------------------------------
    # RULE SET 4: ATTENDANCE (SHORT FORM)
    # --------------------------------------------------------------------------

    if 65 <= attendance < 75:
        rec = f"⚠️ Attendance Warning ({attendance}%): Below 75%. Attend all remaining classes to avoid condonation fines."
        rules_applied.append({
            "rule_id": "Rule 8",
            "rule_name": "Attendance Condonation Risk",
            "condition": "65% <= Attendance < 75%",
            "student_value": f"Attendance: {attendance}%",
            "recommendation": rec,
            "badge_type": "warning"
        })
        ai_advice_list.append(rec)

    elif attendance < 65:
        rec = f"🚨 Critical Attendance ({attendance}%): High detention risk (<65%). Contact HOD and maintain 100% attendance."
        rules_applied.append({
            "rule_id": "Rule 9",
            "rule_name": "Critical Attendance Shortage",
            "condition": "Attendance < 65%",
            "student_value": f"Attendance: {attendance}%",
            "recommendation": rec,
            "badge_type": "danger"
        })
        ai_advice_list.append(rec)

    elif attendance >= 85:
        rec = f"🛡️ High Attendance ({attendance}%): Excellent class attendance. Use faculty guidance for projects."
        rules_applied.append({
            "rule_id": "Rule 9B",
            "rule_name": "High Attendance Advantage",
            "condition": "Attendance >= 85%",
            "student_value": f"Attendance: {attendance}%",
            "recommendation": rec,
            "badge_type": "success"
        })
        ai_advice_list.append(rec)

    # --------------------------------------------------------------------------
    # RULE SET 5: STUDY HABITS (SHORT FORM)
    # --------------------------------------------------------------------------

    if scaled_percentage >= 70 and study_performance == "Poor":
        rec = "⚡ Inconsistent Habits: Good scores but irregular habits. Build a fixed 1.5-hour daily study routine."
        rules_applied.append({
            "rule_id": "Rule 10",
            "rule_name": "Inconsistent Habits Alert",
            "condition": "Score >= 70% AND Study Performance == 'Poor'",
            "student_value": f"Score: {scaled_percentage}%, Habit: {study_performance}",
            "recommendation": rec,
            "badge_type": "warning"
        })
        ai_advice_list.append(rec)

    if study_performance == "Poor":
        rec = "⏰ Daily Habit: Replace last-minute cramming with a fixed 2-hour daily study routine."
        rules_applied.append({
            "rule_id": "Rule-SP-Poor",
            "rule_name": "Study Habit Routine",
            "condition": "Study Performance == 'Poor'",
            "student_value": f"Habit: {study_performance}",
            "recommendation": rec,
            "badge_type": "warning"
        })
        if rec not in ai_advice_list:
            ai_advice_list.append(rec)

    elif study_performance == "Average":
        rec = "🔄 Active Recall: Use flashcards and review class notes within 24 hours of each lecture."
        rules_applied.append({
            "rule_id": "Rule-SP-Avg",
            "rule_name": "Active Recall Rule",
            "condition": "Study Performance == 'Average'",
            "student_value": f"Habit: {study_performance}",
            "recommendation": rec,
            "badge_type": "info"
        })
        if rec not in ai_advice_list:
            ai_advice_list.append(rec)

    elif study_performance == "Excellent":
        rec = "🚀 Advanced Study: Excellent discipline. Practice competitive coding and GATE questions."
        rules_applied.append({
            "rule_id": "Rule-SP-Exc",
            "rule_name": "Advanced Study Rule",
            "condition": "Study Performance == 'Excellent'",
            "student_value": f"Habit: {study_performance}",
            "recommendation": rec,
            "badge_type": "success"
        })
        if rec not in ai_advice_list:
            ai_advice_list.append(rec)

    # --------------------------------------------------------------------------
    # RULE SET 6: ACADEMIC DIFFICULTY (SHORT FORM)
    # --------------------------------------------------------------------------

    if difficulty == "Difficulty in programming":
        rec = "💻 Programming: Practice 1 coding problem daily and dry-run code on paper before typing."
        rules_applied.append({
            "rule_id": "Rule 11",
            "rule_name": "Programming Practice",
            "condition": "Academic Difficulty == 'Difficulty in programming'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "info"
        })
        ai_advice_list.append(rec)

        if is_computer_branch:
            rec_comp = "💻 Tech Career Priority: Commit 1 hour daily to coding and push solutions to GitHub."
            rules_applied.append({
                "rule_id": "Rule 14",
                "rule_name": "Tech Coding Priority",
                "condition": "Branch in Tech AND Difficulty in programming",
                "student_value": f"Branch: {branch}",
                "recommendation": rec_comp,
                "badge_type": "info"
            })
            ai_advice_list.append(rec_comp)

    elif difficulty == "Difficulty in mathematics":
        rec = "📐 Mathematics: Maintain a formula sheet and solve 3 standard textbook problems daily."
        rules_applied.append({
            "rule_id": "Rule 12",
            "rule_name": "Mathematics Practice",
            "condition": "Academic Difficulty == 'Difficulty in mathematics'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "info"
        })
        ai_advice_list.append(rec)

    elif difficulty == "Poor time management":
        rec = "⏳ Time Management: Set a fixed 2-hour evening study block and use 25-minute Pomodoro sessions."
        rules_applied.append({
            "rule_id": "Rule 13",
            "rule_name": "Time Management",
            "condition": "Academic Difficulty == 'Poor time management'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "warning"
        })
        ai_advice_list.append(rec)

    elif difficulty == "Difficulty understanding concepts":
        rec = "💡 Conceptual Clarity: Watch video animations, draw diagrams, and explain concepts to a classmate."
        rules_applied.append({
            "rule_id": "Rule-Concept",
            "rule_name": "Conceptual Clarity",
            "condition": "Academic Difficulty == 'Difficulty understanding concepts'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "info"
        })
        ai_advice_list.append(rec)

    elif difficulty == "Difficulty in core subjects":
        rec = "⚙️ Core Subjects: Focus on high-weightage topics and standard technical diagrams for exams."
        rules_applied.append({
            "rule_id": "Rule-Core",
            "rule_name": "Core Subjects Focus",
            "condition": "Academic Difficulty == 'Difficulty in core subjects'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "info"
        })
        ai_advice_list.append(rec)

    elif difficulty == "Difficulty preparing for exams":
        rec = "🎯 Exam Preparation: Solve 5 years of university question papers and make short formula sheets."
        rules_applied.append({
            "rule_id": "Rule-Exam",
            "rule_name": "Exam Strategy",
            "condition": "Academic Difficulty == 'Difficulty preparing for exams'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "info"
        })
        ai_advice_list.append(rec)

    elif difficulty == "Lack of regular study":
        rec = "📅 Regular Study: Study 30 minutes at the same time every day to build a habit."
        rules_applied.append({
            "rule_id": "Rule-Habit",
            "rule_name": "Habit Building",
            "condition": "Academic Difficulty == 'Lack of regular study'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "warning"
        })
        ai_advice_list.append(rec)

    elif difficulty == "Low attendance":
        rec = "🏫 Class Attendance: Sit in the front row and attend 100% of upcoming classes to cross 75%."
        rules_applied.append({
            "rule_id": "Rule-AttDiff",
            "rule_name": "Attendance Turnaround",
            "condition": "Academic Difficulty == 'Low attendance'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "warning"
        })
        ai_advice_list.append(rec)

    elif difficulty == "No major difficulty":
        rec = "🚀 High Performance: Maintain your 8.5+ CGPA and work on projects and certifications."
        rules_applied.append({
            "rule_id": "Rule-NoDiff",
            "rule_name": "High Performance",
            "condition": "Academic Difficulty == 'No major difficulty'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "success"
        })
        ai_advice_list.append(rec)

    elif difficulty == "Other":
        rec = "🔍 Mentorship: Meet your faculty mentor to resolve specific subject difficulties."
        rules_applied.append({
            "rule_id": "Rule-OtherDiff",
            "rule_name": "Mentorship",
            "condition": "Academic Difficulty == 'Other'",
            "student_value": f"Difficulty: {difficulty}",
            "recommendation": rec,
            "badge_type": "info"
        })
        ai_advice_list.append(rec)

    # --------------------------------------------------------------------------
    # TAILORED BRANCH & YEAR SUGGESTIONS
    # --------------------------------------------------------------------------
    academic_suggestions = get_academic_suggestions(branch, year)
    tech_suggestions = get_technical_suggestions(branch, year)
    practical_suggestions = get_practical_suggestions(branch, year)

    # Career guidance
    if "1st" in year:
        career_guidance = {
            "year_title": "1st Year B.Tech – Foundation & Exploration",
            "focus_areas": [
                "Programming: Build solid logic in C or Python.",
                "Communication: Practice English speaking and presentations.",
                "Engineering Basics: Grasp Mathematics and Physics.",
                "Campus Clubs: Join tech clubs and hackathons."
            ],
            "action_quote": "Your 1st year sets your academic GPA foundation and analytical habits."
        }
    elif "2nd" in year:
        career_guidance = {
            "year_title": "2nd Year B.Tech – Skill Building & Core Specialization",
            "focus_areas": [
                "Data Structures: Master Java/C++ and core algorithmic structures.",
                "Core Engineering: Master departmental subjects and laboratory tests.",
                "Tools & Git: Gain hands-on familiarity with GitHub.",
                "Mini Projects: Build a semester portfolio project."
            ],
            "action_quote": "Your 2nd year is the golden period for acquiring hard technical skills."
        }
    elif "3rd" in year:
        career_guidance = {
            "year_title": "3rd Year B.Tech – Pre-Final & Placement Readiness",
            "focus_areas": [
                "Industry Projects: Develop robust capstone/mini projects.",
                "DSA Practice: Solve coding problem sets for placements.",
                "Internships: Apply for summer internships via LinkedIn.",
                "Resume: Polish your resume, GitHub profile, and LinkedIn.",
                "Core Revision: Revise departmental subjects for technical interviews."
            ],
            "action_quote": "Focus on technical skills, projects, internships, coding, and resume."
        }
    else:
        career_guidance = {
            "year_title": "4th Year B.Tech – Placement & Industry Transition",
            "focus_areas": [
                "Placements: Register on placement portals and attend drives.",
                "Aptitude: Practice quantitative aptitude and reasoning daily.",
                "Mock Interviews: Participate in technical mock interviews.",
                "Major Project: Ensure high engineering quality in your project.",
                "Job Applications: Apply to on-campus and off-campus opportunities."
            ],
            "action_quote": "Focus on placement drives, aptitude, coding, mock interviews, and major project."
        }

    # Recommended Study Plan
    if scaled_percentage < 50:
        study_plan = {
            "title": "Intensive Academic Recovery Plan",
            "daily_study": "2.5 – 3.0 Hours / day",
            "revision": "40 Minutes daily",
            "practice_questions": "5 – 8 Questions / day",
            "strategy": "Focus on clearing doubts, completing textbook examples, and revising high-weightage chapters first."
        }
    elif scaled_percentage < 70:
        study_plan = {
            "title": "Consistency & Growth Study Plan",
            "daily_study": "2.0 Hours / day",
            "revision": "30 Minutes daily",
            "practice_questions": "5 Questions / day",
            "strategy": "Review lost marks in mid-terms, solve previous university papers, and maintain balanced study."
        }
    else:
        study_plan = {
            "title": "Excellence & Distinction Study Plan",
            "daily_study": "1.5 – 2.0 Hours / day",
            "revision": "Regular (20–30 min)",
            "practice_questions": "Weekly mock papers & practice problems",
            "strategy": "Prepare concise summary sheets, explore advanced concepts, and devote time to projects."
        }

    target_analysis = get_target_improvement_analysis(
        mid_marks=mid_marks,
        semester_marks=semester_marks,
        total_marks=total_marks,
        is_first_year_first_sem=is_mid_only_eval,
        cgpa=cgpa if is_cgpa_mode else 0.0
    )

    return {
        "student_info": {
            "name": student_name,
            "branch": branch,
            "year": year,
            "semester": semester
        },
        "metrics": {
            "mid_marks": mid_marks,
            "semester_marks": semester_marks if not is_first_year_first_sem else 0.0,
            "sgpa": sgpa,
            "cgpa": cgpa,
            "is_cgpa_mode": is_cgpa_mode,
            "total_marks": total_marks,
            "scaled_percentage": scaled_percentage,
            "is_first_year_first_sem": is_first_year_first_sem,
            "attendance": attendance,
            "study_performance": study_performance,
            "difficulty": difficulty
        },
        "subject_scores": subject_scores or [],
        "performance_category": perf_category,
        "attendance_category": att_category,
        "rules_applied": rules_applied,
        "ai_advice_list": ai_advice_list,
        "academic_suggestions": academic_suggestions,
        "tech_suggestions": tech_suggestions,
        "practical_suggestions": practical_suggestions,
        "career_guidance": career_guidance,
        "study_plan": study_plan,
        "target_analysis": target_analysis
    }
