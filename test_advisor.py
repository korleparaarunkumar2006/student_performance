import sys
import rules

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("==================================================")
print("TEST: Subject-Wise Marks Entry (Auto Calculation)")
print("==================================================")

subjects = [
    {"name": "Engineering Mathematics - I", "mid": 12.0, "sem": 0.0},
    {"name": "Engineering Physics", "mid": 26.0, "sem": 0.0},
    {"name": "Programming in C", "mid": 28.0, "sem": 0.0},
    {"name": "Basic Electrical Engineering", "mid": 14.0, "sem": 0.0},
    {"name": "Engineering Graphics", "mid": 22.0, "sem": 0.0}
]

res = rules.analyze_performance(
    student_name="Karthik",
    branch="CSE – Computer Science and Engineering",
    year="1st Year",
    semester="1st Semester",
    attendance=82,
    study_performance="Good",
    difficulty="Difficulty in mathematics",
    subject_scores=subjects
)

print(f"Student: {res['student_info']['name']} ({res['student_info']['year']} {res['student_info']['semester']})")
print(f"Calculated Average Mid: {res['metrics']['mid_marks']} / 30")
print(f"Scaled Equivalent: {res['metrics']['scaled_percentage']}%")
print(f"Performance Category: {res['performance_category']['badge']}")
print("\nRules Triggered:")
for r in res['rules_applied']:
    print(f"• {r['rule_name']} ({r['rule_id']}) -> {r['condition']}")

print("\nAI Advice Generated:")
for idx, adv in enumerate(res['ai_advice_list'], 1):
    print(f"{idx}. {adv}")

print("\nNext Target:")
print(f"• {res['target_analysis']['target_name']} (Needed: +{res['target_analysis']['marks_needed']})")

print("\n==================================================")
print("TEST: Overall Marks Mode (SGPA & CGPA)")
print("==================================================")

res_cgpa = rules.analyze_performance(
    student_name="Ananya",
    branch="ECE – Electronics and Communication Engineering",
    year="3rd Year",
    semester="1st Semester",
    attendance=88,
    study_performance="Good",
    difficulty="No major difficulty",
    sgpa=8.8,
    cgpa=8.2
)

print(f"Student: {res_cgpa['student_info']['name']} ({res_cgpa['student_info']['year']})")
print(f"SGPA: {res_cgpa['metrics']['sgpa']} / 10.0, CGPA: {res_cgpa['metrics']['cgpa']} / 10.0")
print(f"Scaled Percentage: {res_cgpa['metrics']['scaled_percentage']}%")
print(f"Performance Category: {res_cgpa['performance_category']['badge']}")
print("\nRules Triggered:")
for r in res_cgpa['rules_applied']:
    print(f"• {r['rule_name']} ({r['rule_id']}) -> {r['condition']}")

print("\nAI Advice Generated:")
for idx, adv in enumerate(res_cgpa['ai_advice_list'], 1):
    print(f"{idx}. {adv}")

print("\nNext Target:")
print(f"• {res_cgpa['target_analysis']['target_name']} (Needed: +{res_cgpa['target_analysis']['marks_needed']})")

