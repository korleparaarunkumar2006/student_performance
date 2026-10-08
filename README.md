# 🎓 B.Tech Student Performance Advisor
> **Rule-Based AI System for Academic Performance Analysis and Personalized Student Guidance**

An explainable, deterministic **Rule-Based AI / Expert System** tailored for B.Tech engineering students. The system analyzes mid-examination marks, semester/end-examination marks, attendance percentage, internal assessments, and study habits to provide actionable academic guidance, year-specific career roadmaps, and custom study plans.

---

## 📌 Table of Contents
1. [Project Objective & Problem Statement](#-project-objective--problem-statement)
2. [Expert System Architecture](#-expert-system-architecture)
3. [Technology Stack](#-technology-stack)
4. [Knowledge Base & IF–THEN Rules](#-knowledge-base--ifthen-rules)
5. [Inference Mechanism (Forward Chaining)](#-inference-mechanism-forward-chaining)
6. [Explainable AI (XAI) Audit Trail](#-explainable-ai-xai-audit-trail)
7. [Installation & How to Run](#-installation--how-to-run)
8. [Sample Test Cases & Viva Demonstration](#-sample-test-cases--viva-demonstration)
9. [Future Enhancements](#-future-enhancements)

---

## 🎯 Project Objective & Problem Statement

### Problem Statement
Undergraduate B.Tech students often face academic challenges such as:
- Struggling to balance internal continuous evaluations (Mid exams, assignments, labs) with high-weightage University End-Semester exams.
- Low attendance leading to sudden semester condonation fines or examination hall-ticket detention.
- Lack of personalized, branch-specific, and year-specific technical skill guidance (e.g. 1st year foundation vs. 3rd year internship/placement readiness).
- "Black-box" machine learning solutions that cannot clearly explain *why* an academic recommendation was made.

### Objective
To build a transparent, beginner-friendly **Rule-Based Expert System** using pure Python logical rules and Streamlit that:
1. Gathers key student parameters without requiring manual total mark calculations.
2. Applies a declarative knowledge base of engineering academic rules.
3. Delivers actionable, personalized advice along with an **Explainable AI (XAI)** audit log.
4. Complies with standard B.Tech grading scales (Mid: 30 Marks, Semester: 70 Marks, Total: 100 Marks).

---

## 🧩 Expert System Architecture

```text
  +-----------------------------------------------------------+
  |                   STUDENT INPUT FACTS                     |
  |  (Mid Marks /30, Sem Marks /70, Attendance %, Branch,     |
  |   Year, Internal Assessment, Study Habits, Difficulty)    |
  +-----------------------------+-----------------------------+
                                |
                                v
  +-----------------------------------------------------------+
  |              INFERENCE ENGINE (Forward Chaining)          |
  |             Evaluates inputs against Knowledge Base       |
  +-----------------------------+-----------------------------+
                                |
        +-----------------------+-----------------------+
        |                                               |
        v                                               v
+-------------------------------+               +-------------------------------+
|         KNOWLEDGE BASE        |               |      EXPLAINABLE AI (XAI)     |
|   14+ Core IF-THEN Rules      |               |  Rule IDs, Evaluated Logic,   |
|   Thresholds & Branch Configs |               |  Fact Trace & Recommendations |
+-------------------------------+               +-------------------------------+
                                |
                                v
  +-----------------------------------------------------------+
  |                   PERSONALIZED DASHBOARD                  |
  |  - Performance Category (🌟 Excellent / 👍 Good / etc.)  |
  |  - Attendance Warning (if < 75%)                          |
  |  - 4 Key Metrics Cards (/30, /70, /100, Attendance %)     |
  |  - AI Academic Advice                                     |
  |  - Transparent "Why Did the System Give This Advice?"     |
  |  - Customized Daily Study Plan                            |
  |  - B.Tech Year-Wise Career Roadmap (1st to 4th Year)      |
  +-----------------------------------------------------------+
```

---

## 💻 Technology Stack

- **Language:** Python 3.8+ (Compatible with Python 3.10, 3.11, 3.12)
- **Framework:** [Streamlit](https://streamlit.io/) (Clean, modern light-theme UI)
- **AI Paradigm:** Pure Rule-Based AI / Expert System (Forward Chaining)
- **No Machine Learning / No Deep Learning:** 100% deterministic, verifiable, and free of training biases or hallucinated advice.
- **Storage:** Standalone declarative knowledge base in `rules.py`.

---

## 📖 Knowledge Base & IF–THEN Rules

The system implements 14+ standardized domain rules:

| Rule ID | Rule Name | IF Condition | THEN Action / Advice |
| :--- | :--- | :--- | :--- |
| **Rule 1** | Excellent Performance | `Total Marks >= 85 AND Attendance >= 85% AND Internal == "Excellent"` | Outstanding performance. Maintain consistency and prepare early for university distinctions. |
| **Rule 2** | Good Performance | `Total Marks >= 70 AND Total Marks < 85 AND Attendance >= 75%` | Good standing. Focus on challenging subjects, revise regularly, and practice past papers. |
| **Rule 3** | Average Performance | `Total Marks >= 50 AND Total Marks < 70` | Average performance. Increase daily study time, revise core units, and solve practice questions. |
| **Rule 4** | Low Marks Alert | `Total Marks < 50` | Marks need immediate improvement. Adopt a strict study timetable and consult professors. |
| **Rule 5** | Low Mid Marks | `Mid Marks < 15 / 30` | Mid exam marks low. Identify lost marks and revise those units before external exams. |
| **Rule 6** | Mid vs. Sem Imbalance | `Mid Marks >= 20 AND Semester Marks < 40` | Internal preparation is strong, but semester exam strategy needs improvement. Solve timed papers. |
| **Rule 7** | Semester Resilience | `Mid Marks < 15 AND Semester Marks >= 50` | Strong final exam performance, but improve continuous internal assessments and semester regularity. |
| **Rule 8** | Low Attendance | `Attendance < 75%` | Below university 75% criteria. Attend classes regularly to avoid detention or condonation fines. |
| **Rule 9** | Critical Attendance | `Attendance < 65%` | Critical attendance shortage! Immediate departmental intervention required to prevent detention. |
| **Rule 10**| Good Marks, Poor Habits | `Total Marks >= 70 AND Study Performance == "Poor"` | Good natural grasp, but inconsistent habits. Establish a daily routine to prevent future score drops. |
| **Rule 11**| Programming Difficulty | `Difficulty == "Difficulty in programming"` | Practice coding daily: start with fundamentals, move to arrays, strings, functions, and DSA. |
| **Rule 12**| Mathematics Difficulty | `Difficulty == "Difficulty in mathematics"` | Revisit mathematical formulas, practice standard textbook derivations, and solve 5 questions daily. |
| **Rule 13**| Poor Time Management | `Difficulty == "Poor time management"` | Create a balanced weekly timetable allocating dedicated slots for theory, coding, and revision. |
| **Rule 14**| Tech Coding Mastery | `Branch in [CSE, CST, IT, AI&ML, DS] AND Difficulty == "Difficulty in programming"` | Crucial for technical placement: spend daily time solving coding exercises and building mini projects. |

---

## ⚡ Inference Mechanism (Forward Chaining)

The inference mechanism in `rules.py` works via **forward chaining**:
1. **Fact Collection:** Takes current student inputs (marks, attendance, selections).
2. **Derived Facts:** Computes `total_marks = mid_marks + semester_marks`.
3. **Sequential Rule Matching:** Evaluates all conditional statements.
4. **Conflict & Multi-Rule Accumulation:** Since a student can face multiple simultaneous challenges (e.g. low attendance + low mid marks + time management), all matching rules fire and accumulate into an ordered advice list and audit trail.
5. **Synthesis:** Produces a cohesive performance classification, customized study timetable, and year-specific career roadmap.

---

## 🧠 Explainable AI (XAI) Audit Trail

In academic mini-projects and viva voce examinations, explaining **why** an AI system reached a decision is critical.

Every recommendation rendered in the UI contains:
- **Rule Applied & ID:** (e.g., `Rule 8 - Low Attendance Rule`)
- **Evaluated Condition:** (e.g., `Attendance < 75%`)
- **Student Actual Value:** (e.g., `Attendance: 68%`)
- **Resulting Actionable Advice:** Transparently displayed in a dedicated card.

---

## 🚀 Installation & How to Run

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Step-by-Step Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd student-performance-advisor
   ```

2. **(Optional but recommended) Create a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Web Application:**
   ```bash
   streamlit run app.py
   ```

5. The application will automatically open in your default browser at:
   ```text
   http://localhost:8501
   ```

---

## 🧪 Sample Test Cases & Viva Demonstration

### Primary Test Case (From Section 22):
- **Student Name:** Arun
- **Branch:** CST – Computer Science and Technology
- **Year & Semester:** 3rd Year • Semester 3-1
- **Mid Exam Marks:** `12 / 30`
- **Semester Exam Marks:** `42 / 70`
- **Total Marks (Calculated):** `54 / 100`
- **Attendance:** `68%`
- **Study Habits:** Poor
- **Academic Difficulty:** Poor time management

#### Expected Analysis:
- **Classification:** `📈 Average`
- **Attendance Warning:** Prominently displayed (68% < 75%).
- **Rules Triggered:**
  1. `Rule 3` – Average Performance Rule
  2. `Rule 5` – Low Mid Marks Rule
  3. `Rule 8` – Low Attendance Rule
  4. `Rule-SP` – Poor Study Performance Rule
  5. `Rule 13` – Poor Time Management Rule
- **Career Phase:** 3rd Year Pre-Final & Placement Readiness (internships, advanced DSA, mini-projects, resume polishing).
- **Study Plan:** Consistency & Growth Plan (2 hours/day study, 30 min revision, 5 practice questions/day).

*(Tip: In the left sidebar, click **"📌 Sample Case (Arun - 3rd Yr)"** to populate and run this test case in one click during your viva demonstration!)*

---

## 🔮 Future Enhancements

1. **Multi-Subject Aggregator:** Extend from single-subject evaluation to semester-wide SGPA/CGPA multi-course tracking.
2. **Subject Credit Weightage:** Incorporate 3-credit and 4-credit course weighting.
3. **PDF Grade & Advice Report Export:** Allow students to download a signed PDF academic performance summary.
4. **Faculty & Mentor Dashboard:** Enable professors to batch-evaluate class batches and identify students requiring remedial classes.

---

**Developed for B.Tech Academic Demonstration & Rule-Based AI Mini-Projects.**
