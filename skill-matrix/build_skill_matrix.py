"""Build the Skill Matrix workbook for a furniture shop-drawing team.

Usage:  python3 skill-matrix/build_skill_matrix.py
Output: skill-matrix/furniture_shop_drawing_skill_matrix.xlsx
Requires: openpyxl
"""
import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).with_name("furniture_shop_drawing_skill_matrix.xlsx")
FONT = "Khmer OS Battambang"

ROLES = [
    "Junior Drafter",
    "Drafter",
    "Senior Drafter",
    "CNC / Cut-list Programmer",
    "Team Lead / Checker",
]

# (category, skill in Khmer, skill in English, target level per role in ROLES order)
SKILLS = [
    ("A. ការអាន និងស្តង់ដារប្លង់", "អានប្លង់ស្ថាបត្យកម្ម / ឌីហ្សាញផ្នែកខាងក្នុង", "Read architectural & interior design drawings", (2, 3, 4, 2, 4)),
    ("A. ការអាន និងស្តង់ដារប្លង់", "ស្តង់ដារគំនូរបច្ចេកទេស (ប្រភេទខ្សែ, វិមាត្រ, Title block)", "Drafting standards (line types, dimensioning, title block)", (2, 3, 4, 3, 4)),
    ("A. ការអាន និងស្តង់ដារប្លង់", "ទិដ្ឋភាព Orthographic, ផ្នែកកាត់ (Section) និងលម្អិត (Detail)", "Orthographic views, sections & details", (2, 3, 4, 2, 4)),
    ("A. ការអាន និងស្តង់ដារប្លង់", "Tolerance និងគម្លាតសម្រាប់ដំឡើង", "Tolerances & fitting clearances", (1, 2, 3, 3, 4)),
    ("B. កម្មវិធីកុំព្យូទ័រ", "AutoCAD 2D", "AutoCAD 2D drafting", (3, 3, 4, 3, 4)),
    ("B. កម្មវិធីកុំព្យូទ័រ", "Block, Layer, Template និង Dynamic Block", "Blocks, layers, templates & dynamic blocks", (1, 3, 4, 3, 4)),
    ("B. កម្មវិធីកុំព្យូទ័រ", "គំរូ 3D (SketchUp / SolidWorks / Inventor)", "3D modelling", (1, 2, 3, 2, 3)),
    ("B. កម្មវិធីកុំព្យូទ័រ", "កម្មវិធីផលិតគ្រឿងសង្ហារឹម (Cabinet Vision / imos / Polyboard ...)", "Furniture production software", (0, 2, 3, 4, 3)),
    ("B. កម្មវិធីកុំព្យូទ័រ", "Plot / PDF និងការរៀបចំសំណុំប្លង់", "Plotting, PDF & drawing-set compilation", (2, 3, 4, 3, 4)),
    ("B. កម្មវិធីកុំព្យូទ័រ", "Excel សម្រាប់ BOM / Cut list", "Excel for BOM & cut lists", (1, 2, 3, 4, 3)),
    ("C. សម្ភារៈ និងគ្រឿងបន្លាស់", "បន្ទះឈើឧស្សាហកម្ម (MDF, Particle board, Plywood, HMR)", "Engineered panels", (2, 3, 4, 4, 4)),
    ("C. សម្ភារៈ និងគ្រឿងបន្លាស់", "ឈើធម្មជាតិ និង Veneer", "Solid wood & veneer", (1, 2, 3, 2, 4)),
    ("C. សម្ភារៈ និងគ្រឿងបន្លាស់", "Laminate / HPL / Melamine និង Edge banding", "Laminates & edge banding", (2, 3, 4, 4, 4)),
    ("C. សម្ភារៈ និងគ្រឿងបន្លាស់", "គ្រឿងបន្លាស់ (Hinge, Drawer slide, Handle, Connector)", "Hardware (hinges, slides, handles, connectors)", (2, 3, 4, 4, 4)),
    ("C. សម្ភារៈ និងគ្រឿងបន្លាស់", "ការលាបពណ៌ / Finishing (PU, Lacquer, Paint)", "Finishes", (1, 2, 3, 1, 3)),
    ("C. សម្ភារៈ និងគ្រឿងបន្លាស់", "សម្ភារៈផ្សំ (កញ្ចក់, ថ្ម, ដែក / Stainless)", "Glass, stone & metal integration", (1, 2, 3, 1, 3)),
    ("D. រចនាសម្ព័ន្ធ និងការតភ្ជាប់", "រចនាសម្ព័ន្ធទូ (Carcass) និងប្រព័ន្ធ 32mm", "Cabinet construction & 32mm system", (1, 3, 4, 4, 4)),
    ("D. រចនាសម្ព័ន្ធ និងការតភ្ជាប់", "ប្រភេទតភ្ជាប់ (Dowel, Cam-lock, Mortise-tenon, Biscuit)", "Joinery methods", (1, 3, 4, 3, 4)),
    ("D. រចនាសម្ព័ន្ធ និងការតភ្ជាប់", "ការទ្រទម្ងន់ និងប្រវែងធ្នើ (Span)", "Structural load & shelf span", (0, 2, 3, 2, 4)),
    ("D. រចនាសម្ព័ន្ធ និងការតភ្ជាប់", "គម្លាត Scribe / Filler សម្រាប់ដំឡើងនៅការដ្ឋាន", "Site-fitting allowances (scribe, filler)", (1, 2, 4, 2, 4)),
    ("E. ឯកសារផលិតកម្ម", "វាស់ និងផ្ទៀងផ្ទាត់វិមាត្រនៅការដ្ឋាន", "Site measurement & verification", (1, 3, 4, 1, 4)),
    ("E. ឯកសារផលិតកម្ម", "ប្លង់ទូទៅ Plan / Elevation", "General arrangement plans & elevations", (2, 3, 4, 2, 4)),
    ("E. ឯកសារផលិតកម្ម", "ប្លង់លម្អិតគ្រឿងនីមួយៗ (Part drawing)", "Part / component detail drawings", (2, 3, 4, 3, 4)),
    ("E. ឯកសារផលិតកម្ម", "បញ្ជីកាត់ (Cut list) និង BOM", "Cut list & bill of materials", (1, 3, 4, 4, 4)),
    ("E. ឯកសារផលិតកម្ម", "ឯកសារ CNC / DXF និង Nesting", "CNC / DXF files & nesting", (0, 2, 3, 4, 3)),
    ("E. ឯកសារផលិតកម្ម", "តារាងចោះរន្ធ និង Edge banding", "Drilling & edge-banding schedules", (1, 3, 4, 4, 4)),
    ("E. ឯកសារផលិតកម្ម", "ប្លង់តម្លើង និងដំឡើង (Assembly / Installation)", "Assembly & installation drawings", (1, 2, 4, 2, 4)),
    ("E. ឯកសារផលិតកម្ម", "គ្រប់គ្រងកំណែប្លង់ (Revision control)", "Revision control", (2, 3, 4, 3, 4)),
    ("F. គុណភាព និងការសម្របសម្រួល", "ត្រួតពិនិត្យប្លង់ខ្លួនឯងតាម Checklist", "Self-check against checklist", (2, 3, 4, 3, 4)),
    ("F. គុណភាព និងការសម្របសម្រួល", "សម្របសម្រួលជាមួយ MEP (ព្រីភ្លើង, អំពូល, បំពង់ទឹក)", "MEP coordination", (1, 2, 3, 1, 4)),
    ("F. គុណភាព និងការសម្របសម្រួល", "រៀបចំ Submittal ឲ្យអតិថិជន / អ្នករចនាអនុម័ត", "Submittals for client / designer approval", (1, 2, 3, 1, 4)),
    ("F. គុណភាព និងការសម្របសម្រួល", "ទំនាក់ទំនងជាមួយរោងចក្រ និងក្រុមដំឡើង", "Communication with factory & installers", (2, 3, 4, 3, 4)),
    ("F. គុណភាព និងការសម្របសម្រួល", "គ្រប់គ្រងពេលវេលា និងបំពេញតាមកាលកំណត់", "Time management & deadlines", (2, 3, 4, 3, 4)),
    ("F. គុណភាព និងការសម្របសម្រួល", "បង្វឹក និងណែនាំសមាជិកថ្មី", "Coaching & mentoring", (0, 1, 3, 2, 4)),
]

LEVELS = [
    (0, "មិនទាន់មាន", "No knowledge", "មិនទាន់បានរៀន ឬមិនធ្លាប់ធ្វើ", "FFFFFF"),
    (1, "កំពុងរៀន", "Learning", "ដឹងទ្រឹស្តីខ្លះ ត្រូវការការណែនាំជាប់ជានិច្ច", "F8CBAD"),
    (2, "ធ្វើបានដោយមានជំនួយ", "Supervised", "ធ្វើការងារធម្មតាបាន ប៉ុន្តែត្រូវការការត្រួតពិនិត្យ", "FFE699"),
    (3, "ធ្វើបានដោយឯករាជ្យ", "Independent", "ធ្វើបានត្រឹមត្រូវ ទាន់ពេល ដោយមិនត្រូវការជំនួយ", "C6E0B4"),
    (4, "អ្នកជំនាញ / គ្រូបង្វឹក", "Expert / Trainer", "ដោះស្រាយករណីស្មុគស្មាញ និងអាចបង្រៀនអ្នកដទៃ", "70AD47"),
]

# Example team — replace names/roles with real ones.
MEMBERS = [
    ("បុគ្គលិក ១", "Team Lead / Checker"),
    ("បុគ្គលិក ២", "Senior Drafter"),
    ("បុគ្គលិក ៣", "Drafter"),
    ("បុគ្គលិក ៤", "Drafter"),
    ("បុគ្គលិក ៥", "Junior Drafter"),
    ("បុគ្គលិក ៦", "CNC / Cut-list Programmer"),
]

TRAINING_METHODS = ["OJT (រៀនតាមការងារ)", "Mentoring (គូបង្វឹក)", "វគ្គផ្ទៃក្នុង", "វគ្គខាងក្រៅ", "វគ្គ Online", "ទស្សនកិច្ចរោងចក្រ / ការដ្ឋាន"]
STATUSES = ["មិនទាន់ចាប់ផ្តើម", "កំពុងដំណើរការ", "បានបញ្ចប់", "ផ្អាក"]

# ---------------------------------------------------------------- styles
thin = Side(style="thin", color="A6A6A6")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HEAD_FILL = PatternFill("solid", fgColor="1F4E78")
SUB_FILL = PatternFill("solid", fgColor="DDEBF7")
CAT_FILL = PatternFill("solid", fgColor="F2F2F2")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)


def f(size=10, bold=False, color="000000"):
    return Font(name=FONT, size=size, bold=bold, color=color)


def title(ws, text, sub, width_cols):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=width_cols)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=width_cols)
    ws["A1"].value, ws["A1"].font, ws["A1"].alignment = text, f(16, True, "1F4E78"), LEFT
    ws["A2"].value, ws["A2"].font, ws["A2"].alignment = sub, f(9, False, "595959"), LEFT
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 32


def head(cell, text):
    cell.value, cell.font, cell.fill, cell.alignment, cell.border = text, f(10, True, "FFFFFF"), HEAD_FILL, CENTER, BORDER


def box(cell, value=None, align=CENTER, font=None, fill=None, fmt=None):
    if value is not None:
        cell.value = value
    cell.font = font or f()
    cell.alignment = align
    cell.border = BORDER
    if fill:
        cell.fill = fill
    if fmt:
        cell.number_format = fmt


def level_colors(ws, rng):
    for lvl, *_, color in LEVELS:
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[str(lvl)], fill=PatternFill("solid", fgColor=color)))


def setup_print(ws, landscape=True):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = ws.page_margins.right = 0.3


# ---------------------------------------------------------------- workbook
wb = Workbook()
N, M = len(SKILLS), len(MEMBERS)
FIRST = 6                      # first skill row on matrix / target / gap sheets
LAST = FIRST + N - 1
MC1 = 5                        # first member column (E)
MCL = MC1 + M - 1              # last member column
mcol = lambda i: get_column_letter(MC1 + i)

# ---- Sheet 1: level definitions
lv = wb.active
lv.title = "1_Levels"
title(lv, "កម្រិតជំនាញ (Skill Levels 0 – 4)", "ប្រើលេខ 0–4 ពេលវាយតម្លៃក្នុង Sheet 2_SkillMatrix។ វាយតម្លៃដោយ Team Lead រួមជាមួយបុគ្គលិកម្នាក់ៗ រៀងរាល់ ៦ ខែម្តង។", 5)
for c, h in enumerate(["កម្រិត", "ឈ្មោះកម្រិត", "Level name", "ការពិពណ៌នា / ភស្តុតាងដែលត្រូវឃើញ", "ពណ៌"], 1):
    head(lv.cell(4, c), h)
for r, (lvl, kh, en, desc, color) in enumerate(LEVELS, 5):
    box(lv.cell(r, 1), lvl, font=f(12, True))
    box(lv.cell(r, 2), kh, LEFT, f(10, True))
    box(lv.cell(r, 3), en, LEFT)
    box(lv.cell(r, 4), desc, LEFT)
    box(lv.cell(r, 5), "", fill=PatternFill("solid", fgColor=color))
    lv.row_dimensions[r].height = 34
notes = [
    "របៀបប្រើ:",
    "1) កែឈ្មោះ និងតួនាទីបុគ្គលិកនៅជួរ 4–5 ក្នុង Sheet 2_SkillMatrix (តួនាទីជ្រើសពីបញ្ជី)។",
    "2) វាយលេខកម្រិត 0–4 សម្រាប់ជំនាញនីមួយៗ — ពណ៌នឹងប្តូរដោយស្វ័យប្រវត្តិ។",
    "3) Sheet 4_Gap គណនាគម្លាត = កម្រិតបច្ចុប្បន្ន − កម្រិតតម្រូវតាមតួនាទី (Sheet 3_RoleTarget)។ លេខក្រហម = ត្រូវបណ្តុះបណ្តាល។",
    "4) ចម្លងគម្លាតធំៗទៅ Sheet 5_TrainingPlan ហើយកំណត់វិធីបណ្តុះបណ្តាល អ្នកបង្វឹក និងកាលកំណត់។",
    "5) ជួរ 'ហានិភ័យ' ក្នុង 2_SkillMatrix បង្ហាញ ⚠ ពេលមានមនុស្សតិចជាង 2 នាក់ដែលធ្វើបានឯករាជ្យ (≥3) — ត្រូវបង្វឹកអ្នកបម្រុង។",
    "ចំណាំ: លេខក្នុងឯកសារនេះជាឧទាហរណ៍ — សូមជំនួសដោយការវាយតម្លៃពិតប្រាកដ។",
]
for i, t in enumerate(notes):
    c = lv.cell(12 + i, 1, t)
    c.font = f(10, i == 0 or i == len(notes) - 1, "C00000" if i == len(notes) - 1 else "000000")
    lv.merge_cells(start_row=12 + i, start_column=1, end_row=12 + i, end_column=5)
    c.alignment = LEFT
    lv.row_dimensions[12 + i].height = 22
for col, w in zip("ABCDE", (9, 26, 18, 60, 10)):
    lv.column_dimensions[col].width = w
setup_print(lv, landscape=False)

# ---- Sheet 2: skill matrix
sm = wb.create_sheet("2_SkillMatrix")
STAT1 = MCL + 1
title(sm, "Skill Matrix — ក្រុមការងារប្លង់ផលិត (Furniture Shop Drawing)",
      "វាយលេខ 0–4 (មើល 1_Levels)។ ជួរ 4 = ឈ្មោះបុគ្គលិក, ជួរ 5 = តួនាទី (ជ្រើសពីបញ្ជី)។   ការវាយតម្លៃចុងក្រោយ: ____ / ____ / ______   អ្នកវាយតម្លៃ: ______________",
      STAT1 + 2)
for c, h in enumerate(["ល.រ", "ក្រុមជំនាញ", "ជំនាញ", "Skill (EN)"], 1):
    head(sm.cell(4, c), h)
    sm.merge_cells(start_row=4, start_column=c, end_row=5, end_column=c)
for i, (name, role) in enumerate(MEMBERS):
    head(sm.cell(4, MC1 + i), name)
    box(sm.cell(5, MC1 + i), role, font=f(8, True, "1F4E78"), fill=SUB_FILL)
for j, h in enumerate(["មធ្យមក្រុម", "ចំនួនអ្នក ≥3", "ហានិភ័យ"]):
    head(sm.cell(4, STAT1 + j), h)
    sm.merge_cells(start_row=4, start_column=STAT1 + j, end_row=5, end_column=STAT1 + j)
sm.row_dimensions[4].height = 30
sm.row_dimensions[5].height = 30

random.seed(7)
sample = {}  # (skill idx, member idx) -> level, reused for the training plan
for s, (cat, kh, en, targets) in enumerate(SKILLS):
    r = FIRST + s
    shade = CAT_FILL if cat[0] in "ACE" else None
    box(sm.cell(r, 1), s + 1, fill=shade)
    box(sm.cell(r, 2), cat, LEFT, f(9, True), shade)
    box(sm.cell(r, 3), kh, LEFT, fill=shade)
    box(sm.cell(r, 4), en, LEFT, f(9, False, "595959"), shade)
    for i, (_, role) in enumerate(MEMBERS):
        t = targets[ROLES.index(role)]
        val = max(0, min(4, t + random.choice((-1, 0, 0, 0, 0, 1))))
        sample[(s, i)] = val
        box(sm.cell(r, MC1 + i), val, font=f(11, True))
    rng = f"{mcol(0)}{r}:{mcol(M - 1)}{r}"
    box(sm.cell(r, STAT1), f"=IFERROR(AVERAGE({rng}),\"\")", fmt="0.0")
    box(sm.cell(r, STAT1 + 1), f"=COUNTIF({rng},\">=3\")")
    box(sm.cell(r, STAT1 + 2), f"=IF({get_column_letter(STAT1 + 1)}{r}<2,\"⚠ ខ្វះអ្នកបម្រុង\",\"OK\")", font=f(9, True))
    sm.row_dimensions[r].height = 30

# merge category cells
start = FIRST
for s in range(1, N + 1):
    if s == N or SKILLS[s][0] != SKILLS[s - 1][0]:
        if FIRST + s - 1 > start:
            sm.merge_cells(start_row=start, start_column=2, end_row=FIRST + s - 1, end_column=2)
        start = FIRST + s

# per-member summary rows
sum_rows = [
    ("ពិន្ទុសរុប", lambda c: f"=SUM({c}{FIRST}:{c}{LAST})", "0"),
    ("ពិន្ទុមធ្យម", lambda c: f"=AVERAGE({c}{FIRST}:{c}{LAST})", "0.00"),
    ("ចំនួនជំនាញ ≥3", lambda c: f"=COUNTIF({c}{FIRST}:{c}{LAST},\">=3\")", "0"),
    ("% ត្រូវតាមតម្រូវការតួនាទី", lambda c: f"=IFERROR(COUNTIF('4_Gap'!{c}{FIRST}:{c}{LAST},\">=0\")/COUNT('4_Gap'!{c}{FIRST}:{c}{LAST}),\"\")", "0%"),
]
for k, (label, fn, fmt) in enumerate(sum_rows):
    r = LAST + 2 + k
    sm.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    box(sm.cell(r, 1), label, Alignment(horizontal="right", vertical="center"), f(10, True), SUB_FILL)
    for col in range(2, 5):
        sm.cell(r, col).border = BORDER
    for i in range(M):
        box(sm.cell(r, MC1 + i), fn(mcol(i)), font=f(10, True), fill=SUB_FILL, fmt=fmt)
PCT_ROW = LAST + 5
sm.conditional_formatting.add(f"{mcol(0)}{PCT_ROW}:{mcol(M - 1)}{PCT_ROW}",
                              CellIsRule(operator="lessThan", formula=["0.8"], font=Font(name=FONT, bold=True, color="C00000")))

matrix_rng = f"{mcol(0)}{FIRST}:{mcol(M - 1)}{LAST}"
level_colors(sm, matrix_rng)
risk_col = get_column_letter(STAT1 + 2)
sm.conditional_formatting.add(f"{risk_col}{FIRST}:{risk_col}{LAST}",
                              FormulaRule(formula=[f'LEFT({risk_col}{FIRST},1)="⚠"'], fill=PatternFill("solid", fgColor="F8CBAD"), font=Font(name=FONT, bold=True, color="C00000")))

dv_lvl = DataValidation(type="whole", operator="between", formula1="0", formula2="4", allow_blank=True,
                        errorTitle="កម្រិតមិនត្រឹមត្រូវ", error="សូមវាយលេខ 0 ដល់ 4", showErrorMessage=True)
dv_lvl.add(matrix_rng)
dv_role = DataValidation(type="list", formula1=f"='3_RoleTarget'!$E$5:${get_column_letter(4 + len(ROLES))}$5", allow_blank=True)
dv_role.add(f"{mcol(0)}5:{mcol(M - 1)}5")
sm.add_data_validation(dv_lvl)
sm.add_data_validation(dv_role)

for col, w in zip("ABCD", (5, 18, 42, 30)):
    sm.column_dimensions[col].width = w
for i in range(M):
    sm.column_dimensions[mcol(i)].width = 12
for j, w in enumerate((10, 10, 15)):
    sm.column_dimensions[get_column_letter(STAT1 + j)].width = w
sm.freeze_panes = sm.cell(FIRST, MC1)
setup_print(sm)
sm.print_title_rows = "4:5"

# ---- Sheet 3: role targets
rt = wb.create_sheet("3_RoleTarget")
RC1, RCL = 5, 4 + len(ROLES)
title(rt, "កម្រិតតម្រូវតាមតួនាទី (Target Level by Role)",
      "កំណត់កម្រិតអប្បបរមាដែលតួនាទីនីមួយៗត្រូវមាន។ ឈ្មោះតួនាទីក្នុងជួរ 5 ត្រូវតែដូចគ្នានឹងតួនាទីក្នុង 2_SkillMatrix។ អាចកែលេខ ឬប្តូរឈ្មោះតួនាទីតាមក្រុមហ៊ុន។",
      RCL)
for c, h in enumerate(["ល.រ", "ក្រុមជំនាញ", "ជំនាញ", "Skill (EN)"], 1):
    head(rt.cell(4, c), h)
    rt.merge_cells(start_row=4, start_column=c, end_row=5, end_column=c)
rt.merge_cells(start_row=4, start_column=RC1, end_row=4, end_column=RCL)
head(rt.cell(4, RC1), "តួនាទី (Role)")
for j, role in enumerate(ROLES):
    box(rt.cell(5, RC1 + j), role, font=f(9, True, "1F4E78"), fill=SUB_FILL)
rt.row_dimensions[5].height = 34
for s, (cat, kh, en, targets) in enumerate(SKILLS):
    r = FIRST + s
    box(rt.cell(r, 1), f"='2_SkillMatrix'!A{r}")
    box(rt.cell(r, 2), f"='2_SkillMatrix'!B{r}", LEFT, f(9, True))
    box(rt.cell(r, 3), f"='2_SkillMatrix'!C{r}", LEFT)
    box(rt.cell(r, 4), f"='2_SkillMatrix'!D{r}", LEFT, f(9, False, "595959"))
    for j, t in enumerate(targets):
        box(rt.cell(r, RC1 + j), t, font=f(11, True))
    rt.row_dimensions[r].height = 30
level_colors(rt, f"E{FIRST}:{get_column_letter(RCL)}{LAST}")
rt.add_data_validation(dv_lvl2 := DataValidation(type="whole", operator="between", formula1="0", formula2="4"))
dv_lvl2.add(f"E{FIRST}:{get_column_letter(RCL)}{LAST}")
for col, w in zip("ABCD", (5, 18, 42, 30)):
    rt.column_dimensions[col].width = w
for j in range(len(ROLES)):
    rt.column_dimensions[get_column_letter(RC1 + j)].width = 14
rt.freeze_panes = rt.cell(FIRST, RC1)
setup_print(rt)

# ---- Sheet 4: gap analysis
gp = wb.create_sheet("4_Gap")
title(gp, "ការវិភាគគម្លាតជំនាញ (Gap Analysis)",
      "គម្លាត = កម្រិតបច្ចុប្បន្ន − កម្រិតតម្រូវតាមតួនាទី។   ក្រហម (< 0) = ត្រូវបណ្តុះបណ្តាល,  បៃតង (≥ 0) = ត្រូវតាមតម្រូវការ។  Sheet នេះគណនាដោយស្វ័យប្រវត្តិ — មិនបាច់វាយបញ្ចូល។",
      MCL + 1)
for c, h in enumerate(["ល.រ", "ក្រុមជំនាញ", "ជំនាញ", "Skill (EN)"], 1):
    head(gp.cell(4, c), h)
    gp.merge_cells(start_row=4, start_column=c, end_row=5, end_column=c)
for i in range(M):
    c = mcol(i)
    head(gp.cell(4, MC1 + i), f"='2_SkillMatrix'!{c}4")
    box(gp.cell(5, MC1 + i), f"='2_SkillMatrix'!{c}5", font=f(8, True, "1F4E78"), fill=SUB_FILL)
head(gp.cell(4, MCL + 1), "ចំនួនអ្នកខ្វះ")
gp.merge_cells(start_row=4, start_column=MCL + 1, end_row=5, end_column=MCL + 1)
role_hdr = f"'3_RoleTarget'!$E$5:${get_column_letter(RCL)}$5"
for s in range(N):
    r = FIRST + s
    box(gp.cell(r, 1), f"='2_SkillMatrix'!A{r}")
    box(gp.cell(r, 2), f"='2_SkillMatrix'!B{r}", LEFT, f(9, True))
    box(gp.cell(r, 3), f"='2_SkillMatrix'!C{r}", LEFT)
    box(gp.cell(r, 4), f"='2_SkillMatrix'!D{r}", LEFT, f(9, False, "595959"))
    for i in range(M):
        c = mcol(i)
        formula = (f"=IF(OR('2_SkillMatrix'!{c}$5=\"\",'2_SkillMatrix'!{c}{r}=\"\"),\"\","
                   f"'2_SkillMatrix'!{c}{r}-INDEX('3_RoleTarget'!$E{r}:${get_column_letter(RCL)}{r},MATCH('2_SkillMatrix'!{c}$5,{role_hdr},0)))")
        box(gp.cell(r, MC1 + i), formula, font=f(11, True), fmt="+0;-0;0")
    box(gp.cell(r, MCL + 1), f"=COUNTIF({mcol(0)}{r}:{mcol(M - 1)}{r},\"<0\")", font=f(10, True))
    gp.row_dimensions[r].height = 30
gap_rng = f"{mcol(0)}{FIRST}:{mcol(M - 1)}{LAST}"
gp.conditional_formatting.add(gap_rng, CellIsRule(operator="lessThan", formula=["-1"], fill=PatternFill("solid", fgColor="FF7C80"), font=Font(name=FONT, bold=True, color="9C0006")))
gp.conditional_formatting.add(gap_rng, CellIsRule(operator="equal", formula=["-1"], fill=PatternFill("solid", fgColor="FFC7CE"), font=Font(name=FONT, bold=True, color="9C0006")))
gp.conditional_formatting.add(gap_rng, FormulaRule(formula=[f'AND(ISNUMBER({mcol(0)}{FIRST}),{mcol(0)}{FIRST}>=0)'], fill=PatternFill("solid", fgColor="C6EFCE"), font=Font(name=FONT, color="006100")))
r = LAST + 2
gp.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
box(gp.cell(r, 1), "ចំនួនជំនាញដែលខ្វះ (គម្លាត < 0)", Alignment(horizontal="right", vertical="center"), f(10, True), SUB_FILL)
for i in range(M):
    box(gp.cell(r, MC1 + i), f"=COUNTIF({mcol(i)}{FIRST}:{mcol(i)}{LAST},\"<0\")", font=f(10, True), fill=SUB_FILL)
for col, w in zip("ABCD", (5, 18, 42, 30)):
    gp.column_dimensions[col].width = w
for i in range(M):
    gp.column_dimensions[mcol(i)].width = 12
gp.column_dimensions[get_column_letter(MCL + 1)].width = 11
gp.freeze_panes = gp.cell(FIRST, MC1)
setup_print(gp)
# category merges on gap & target sheets mirror the matrix
start = FIRST
for s in range(1, N + 1):
    if s == N or SKILLS[s][0] != SKILLS[s - 1][0]:
        if FIRST + s - 1 > start:
            for ws in (rt, gp):
                ws.merge_cells(start_row=start, start_column=2, end_row=FIRST + s - 1, end_column=2)
        start = FIRST + s

# ---- Sheet 5: training plan
tp = wb.create_sheet("5_TrainingPlan")
cols = [("ល.រ", 5), ("បុគ្គលិក", 14), ("ជំនាញដែលត្រូវអភិវឌ្ឍ", 42), ("កម្រិតបច្ចុប្បន្ន", 10), ("កម្រិតគោលដៅ", 10),
        ("គម្លាត", 8), ("វិធីបណ្តុះបណ្តាល", 22), ("អ្នកបង្វឹក / ស្ថាប័ន", 18), ("ថ្ងៃចាប់ផ្តើម", 12),
        ("កាលកំណត់", 12), ("ស្ថានភាព", 16), ("ភស្តុតាង / កំណត់ចំណាំ", 30)]
title(tp, "ផែនការបណ្តុះបណ្តាល (Training Plan)",
      "ជ្រើសជំនាញដែលមានគម្លាតធំបំផុតពី 4_Gap (ផ្តោតលើ ⚠ ខ្វះអ្នកបម្រុង មុនគេ)។ ជួរខាងក្រោមជាឧទាហរណ៍ — កែតាមជាក់ស្តែង។",
      len(cols))
for c, (h, w) in enumerate(cols, 1):
    head(tp.cell(4, c), h)
    tp.column_dimensions[get_column_letter(c)].width = w
tp.row_dimensions[4].height = 34
gaps = []
for (s, i), val in sample.items():
    target = SKILLS[s][3][ROLES.index(MEMBERS[i][1])]
    if val < target:
        gaps.append((val - target, i, s, val, target))
gaps.sort()
mentor_for = {}
for s in range(N):
    best = max(range(M), key=lambda i: sample[(s, i)])
    mentor_for[s] = MEMBERS[best][0] if sample[(s, best)] >= 3 else "វគ្គខាងក្រៅ"
example = gaps[:10]
ROWS = 30
for k in range(ROWS):
    r = 5 + k
    for c in range(1, len(cols) + 1):
        box(tp.cell(r, c), align=LEFT if c in (2, 3, 7, 8, 11, 12) else CENTER)
    tp.cell(r, 1).value = k + 1
    tp.cell(r, 6).value = f'=IF(OR(D{r}="",E{r}=""),"",D{r}-E{r})'
    tp.cell(r, 6).number_format = "+0;-0;0"
    tp.cell(r, 9).number_format = tp.cell(r, 10).number_format = "dd/mm/yyyy"
    tp.row_dimensions[r].height = 26
    if k < len(example):
        _, i, s, val, target = example[k]
        mentor = mentor_for[s] if mentor_for[s] != MEMBERS[i][0] else "វគ្គខាងក្រៅ"
        tp.cell(r, 2).value = MEMBERS[i][0]
        tp.cell(r, 3).value = SKILLS[s][1]
        tp.cell(r, 4).value = val
        tp.cell(r, 5).value = target
        tp.cell(r, 7).value = TRAINING_METHODS[3] if mentor == "វគ្គខាងក្រៅ" else TRAINING_METHODS[1]
        tp.cell(r, 8).value = mentor
        tp.cell(r, 11).value = STATUSES[0]
TL = 4 + ROWS
tp.conditional_formatting.add(f"F5:F{TL}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=FONT, bold=True, color="C00000")))
tp.conditional_formatting.add(f"K5:K{TL}", CellIsRule(operator="equal", formula=[f'"{STATUSES[2]}"'], fill=PatternFill("solid", fgColor="C6EFCE")))
tp.conditional_formatting.add(f"K5:K{TL}", CellIsRule(operator="equal", formula=[f'"{STATUSES[1]}"'], fill=PatternFill("solid", fgColor="FFEB9C")))
level_colors(tp, f"D5:E{TL}")

# hidden list sheet for dropdowns
ls = wb.create_sheet("Lists")
for k, v in enumerate(TRAINING_METHODS, 1):
    ls.cell(k, 1, v)
for k, v in enumerate(STATUSES, 1):
    ls.cell(k, 2, v)
for k, (name, _) in enumerate(MEMBERS, 1):
    ls.cell(k, 3, f"='2_SkillMatrix'!{mcol(k - 1)}4")
for k in range(N):
    ls.cell(k + 1, 4, f"='2_SkillMatrix'!C{FIRST + k}")
ls.sheet_state = "hidden"
for rng, src in ((f"G5:G{TL}", f"=Lists!$A$1:$A${len(TRAINING_METHODS)}"),
                 (f"K5:K{TL}", f"=Lists!$B$1:$B${len(STATUSES)}"),
                 (f"B5:B{TL}", f"=Lists!$C$1:$C${M}"),
                 (f"C5:C{TL}", f"=Lists!$D$1:$D${N}")):
    dv = DataValidation(type="list", formula1=src, allow_blank=True, showErrorMessage=False)
    dv.add(rng)
    tp.add_data_validation(dv)
dv_tp = DataValidation(type="whole", operator="between", formula1="0", formula2="4", allow_blank=True)
dv_tp.add(f"D5:E{TL}")
tp.add_data_validation(dv_tp)
tp.freeze_panes = "C5"
setup_print(tp)

# signature block
r = TL + 2
for c, text in ((2, "រៀបចំដោយ (Team Lead): ____________"), (7, "ត្រួតពិនិត្យដោយ (Manager): ____________"), (11, "ថ្ងៃទី: ___ / ___ / ______")):
    tp.cell(r, c, text).font = f(10, True)

wb.active = 1
wb.save(OUT)
print(f"wrote {OUT}")
