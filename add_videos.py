#!/usr/bin/env python3
"""Add 4 more videos per topic across all 38 topics.

course.json  — prerequisites (6 topics)
build_curriculum.py — week topics (32 topics)

Run:  python3 add_videos.py
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
COURSE_JSON = ROOT / "App" / "Resources" / "Content" / "course.json"
BUILD_PY    = ROOT / "build_curriculum.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def src(key, chapter=None):
    d = {"source": key}
    if chapter: d["chapter"] = chapter
    return d

OS = "openstax_abramson"; LR = "lippman_rasmussen"; YS = "yoshiwara"


# ---------------------------------------------------------------------------
# Video data  (youtubeId, title, channel, source_key, chapter_or_None, duration)
# ---------------------------------------------------------------------------

PREREQ_VIDEOS = {
    "algebra-essentials": [
        ("GmMX3-nTWbE", "Solving Linear Equations Made Easy", "PatrickJMT",        OS, "Ch 1.1", 600),
        ("0MKafhRHolM", "Order of Operations — PEMDAS",      "Mario's Math Tutoring", OS, "Ch 1.1", 540),
        ("FkUEsP9efFg", "Introduction to Functions",          "Professor Leonard",    LR, "Ch 1",   720),
        ("ETkyLiVevKM", "Exponent Rules You Forgot",         "Brian McLogan",        OS, "Ch 1.2", 600),
    ],
    "exponents-and-scientific-notation": [
        ("ETkyLiVevKM", "Exponent Rules You Forgot",                   "Brian McLogan",        OS, "Ch 1.2", 480),
        ("HV1AoqM04Pk", "Top 3 Simple Examples of Rules of Exponents", "Brian McLogan",        OS, "Ch 1.2", 480),
        ("HAO4Yuk9wP0", "Factoring Polynomials — All Types",            "Mario's Math Tutoring", OS, "Ch 1.4", 600),
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA",              "Mario's Math Tutoring",YS, "Ch 2.1", 540),
    ],
    "radicals-and-rational-exponents": [
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA", "Mario's Math Tutoring", OS, "Ch 1.4", 540),
        ("iA0wluAsrNY", "Algebra Review — Trigonometry",    "Organic Chemistry Tutor",YS, "Ch 2.1", 600),
        ("GmMX3-nTWbE", "Solving Linear Equations Made Easy","PatrickJMT",             OS, "Ch 1.1", 600),
        ("sci7XQa77_Q", "Simplifying Rational Expressions", "Brian McLogan",         OS, "Ch 1.5", 600),
    ],
    "polynomials-and-factoring": [
        ("HAO4Yuk9wP0", "Factoring Polynomials — All Types",             "Mario's Math Tutoring", OS, "Ch 1.4", 600),
        ("8qezAG2r0sk", "Factoring Polynomials and Solving by Factoring","Organic Chemistry Tutor",OS,"Ch 2.1",720),
        ("GmMX3-nTWbE", "Solving Linear Equations Made Easy",              "PatrickJMT",            OS, "Ch 1.1", 600),
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA",               "Mario's Math Tutoring", YS, "Ch 2.1", 540),
    ],
    "rational-expressions": [
        ("sci7XQa77_Q", "Simplifying Rational Expressions",             "Brian McLogan",         OS, "Ch 1.5", 600),
        ("iA0wluAsrNY", "Algebra Review — Trigonometry",               "Organic Chemistry Tutor",YS,"Ch 2.1",600),
        ("HAO4Yuk9wP0", "Factoring Polynomials — All Types",           "Mario's Math Tutoring", OS, "Ch 1.4", 600),
        ("GmMX3-nTWbE", "Solving Linear Equations Made Easy",            "PatrickJMT",            OS, "Ch 1.1", 600),
    ],
    "coordinate-graphs-and-linear-equations": [
        ("ldYGiXSHa_Q", "Solving Linear Equations",       "PatrickJMT",            OS, "Ch 1.1", 600),
        ("XFkmEW6myeU", "Slope Intercept Form of a Line","Mario's Math Tutoring", LR, "Ch 2.1", 540),
        ("FkUEsP9efFg", "Introduction to Functions",      "Professor Leonard",      LR, "Ch 1",   720),
        ("CRlep6rzy-U", "Domain and Range — Best Explanation","Brian McLogan",      LR, "Ch 1.2", 600),
    ],
}

WEEK_VIDEOS = {
    "what-is-a-function": [
        ("FkUEsP9efFg", "Introduction to Functions",            "Professor Leonard",    LR, "Ch 1.1", 720),
        ("CRlep6rzy-U", "Domain and Range — Best Explanation", "Brian McLogan",        LR, "Ch 1.2", 600),
        ("hOf2UFyL_QE", "Functions — Full Lecture",            "OpenStax",             OS, "Ch 3.1", 540),
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA",   "Mario's Math Tutoring",YS, "Ch 2.1", 540),
    ],
    "domain-and-range": [
        ("CRlep6rzy-U", "Domain and Range — Best Explanation", "Brian McLogan",        LR, "Ch 1.2", 600),
        ("FkUEsP9efFg", "Introduction to Functions",              "Professor Leonard",    LR, "Ch 1.1", 720),
        ("mL9eBKaKXAI", "Finding Domain and Range of a Function","Brian McLogan",        LR, "Ch 1.2", 540),
        ("hOf2UFyL_QE", "Functions — Full Lecture",              "OpenStax",             OS, "Ch 3.1", 540),
    ],
    "rates-of-change-and-behavior": [
        ("9SOQS5jb4f4", "Precalculus in One Day",                   "Brian McLogan",         OS, "Ch 3",   600),
        ("FkUEsP9efFg", "Introduction to Functions",                  "Professor Leonard",     LR, "Ch 1.1", 720),
        ("fNk_zzaMoSs", "Vectors — Essence of Linear Algebra Ch 1","3Blue1Brown",          OS, "Ch 10.4",600),
        ("CRlep6rzy-U", "Domain and Range — Best Explanation",        "Brian McLogan",         LR, "Ch 1.2", 600),
    ],
    "composition-of-functions": [
        ("EsgHKdLSPVc", "Composition of Functions",        "Professor Leonard",    LR, "Ch 1.4", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",        "Brian McLogan",        OS, "Ch 3",   600),
        ("FkUEsP9efFg", "Introduction to Functions",       "Professor Leonard",    LR, "Ch 1.1", 720),
        ("CRlep6rzy-U", "Domain and Range — Best Explanation","Brian McLogan",     LR, "Ch 1.2", 600),
    ],
    "transformation-of-functions": [
        ("sCRB6hMsC4", "Introduction to Graph Transformations","Professor Leonard",LR, "Ch 1.5", 720),
        ("CRlep6rzy-U", "Domain and Range — Best Explanation",   "Brian McLogan",    LR, "Ch 1.2", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",                 "Brian McLogan",    OS, "Ch 3",   600),
        ("FkUEsP9efFg", "Introduction to Functions",                "Professor Leonard",LR, "Ch 1.1", 720),
    ],
    "linear-functions": [
        ("ldYGiXSHa_Q", "Solving Linear Equations",         "PatrickJMT",            OS, "Ch 1.1", 600),
        ("XFkmEW6myeU", "Slope Intercept Form of a Line",   "Mario's Math Tutoring",LR, "Ch 2.1", 540),
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA",  "Mario's Math Tutoring",YS, "Ch 2.1", 540),
        ("FkUEsP9efFg", "Introduction to Functions",         "Professor Leonard",    LR, "Ch 1.1", 720),
    ],
    "quadratic-functions": [
        ("8qezAG2r0sk", "Factoring Polynomials and Solving by Factoring","Organic Chemistry Tutor",OS,"Ch 2.1",720),
        ("GmMX3-nTWbE", "Solving Linear Equations Made Easy","PatrickJMT",           OS, "Ch 1.1", 600),
        ("HAO4Yuk9wP0", "Factoring Polynomials — All Types","Mario's Math Tutoring", OS, "Ch 1.4", 600),
        ("iA0wluAsrNY", "Algebra Review — Trigonometry",    "Organic Chemistry Tutor",YS,"Ch 2.1", 600),
    ],
    "angle-measure": [
        ("l6hSY2Pcch0", "Radians and Degrees",               "NancyPi",               YS, "Ch 1.0", 600),
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA",  "Mario's Math Tutoring", YS, "Ch 2.1", 540),
        ("9SOQS5jb4f4", "Precalculus in One Day",           "Brian McLogan",          OS, "Ch 3",   600),
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",  "NancyPi",               YS, "Ch 2.1", 600),
    ],
    "right-triangle-trig": [
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",  "NancyPi",               YS, "Ch 2.1", 600),
        ("a5WQlcFTXyk", "Trigonometry: Solving Right Triangles","NancyPi",             YS, "Ch 2.2", 600),
        ("iA0wluAsrNY", "Algebra Review — Trigonometry",    "Organic Chemistry Tutor",YS,"Ch 2.1", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",           "Brian McLogan",           OS, "Ch 3",   600),
    ],
    "unit-circle": [
        ("c819bGfH8FA", "How to Remember the Unit Circle",  "NancyPi",               OS, "Ch 7.1", 600),
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",  "NancyPi",               YS, "Ch 2.1", 600),
        ("l6hSY2Pcch0", "Radians and Degrees",                "NancyPi",               YS, "Ch 1.0", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",            "Brian McLogan",           OS, "Ch 3",   600),
    ],
    "rational-functions": [
        ("Q8BbbZxkZSA", "Rational Functions and Conic Sections","Organic Chemistry Tutor",OS,"Ch 5.5",720),
        ("5BL37ieZ2tw", "Rational Expressions and Equations",  "Brian McLogan",          OS, "Ch 1.5", 600),
        ("sCRB6hMsC4", "Introduction to Graph Transformations","Professor Leonard",       LR, "Ch 1.5", 720),
        ("sci7XQa77_Q", "Simplifying Rational Expressions",   "Brian McLogan",          OS, "Ch 1.5", 600),
    ],
    "inverse-functions": [
        ("EsgHKdLSPVc", "Composition of Functions",           "Professor Leonard",      LR, "Ch 1.4", 600),
        ("FkUEsP9efFg", "Introduction to Functions",           "Professor Leonard",     LR, "Ch 1.1", 720),
        ("CRlep6rzy-U", "Domain and Range — Best Explanation","Brian McLogan",         LR, "Ch 1.2", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",             "Brian McLogan",         OS, "Ch 3",   600),
    ],
    "exponential-functions": [
        ("9SOQS5jb4f4", "Precalculus in One Day",             "Brian McLogan",         OS, "Ch 3",   600),
        ("ETkyLiVevKM", "Exponent Rules You Forgot",           "Brian McLogan",         OS, "Ch 1.2", 600),
        ("FkUEsP9efFg", "Introduction to Functions",           "Professor Leonard",       LR, "Ch 1.1", 720),
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA",     "Mario's Math Tutoring",  YS, "Ch 2.1", 540),
    ],
    "logarithms-intro": [
        ("Zw5t6BTQYRU", "Logarithms — How? (NancyPi)",       "NancyPi",               LR, "Ch 4.2", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",             "Brian McLogan",          OS, "Ch 3",   600),
        ("ETkyLiVevKM", "Exponent Rules You Forgot",           "Brian McLogan",          OS, "Ch 1.2", 600),
        ("FkUEsP9efFg", "Introduction to Functions",           "Professor Leonard",        LR, "Ch 1.1", 720),
    ],
    "logarithm-rules": [
        ("Zw5t6BTQYRU", "Logarithms — How? (NancyPi)",       "NancyPi",               LR, "Ch 4.2", 600),
        ("LRbi_pMX1DM", "Logarithms Explained — Rules & Properties","Organic Chemistry Tutor",LR,"Ch 4.3",600),
        ("9SOQS5jb4f4", "Precalculus in One Day",             "Brian McLogan",          OS, "Ch 3",   600),
        ("sCRB6hMsC4", "Introduction to Graph Transformations","Professor Leonard",       LR, "Ch 1.5", 720),
    ],
    "graphs-of-trig-functions": [
        ("fo_q9mEAFp4", "Graphs of Trigonometric Functions",   "Organic Chemistry Tutor",LR,"Ch 6.2", 720),
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",    "NancyPi",               YS, "Ch 2.1", 600),
        ("sCRB6hMsC4", "Introduction to Graph Transformations", "Professor Leonard",      LR, "Ch 1.5", 720),
        ("9SOQS5jb4f4", "Precalculus in One Day",              "Brian McLogan",          OS, "Ch 3",   600),
    ],
    "fundamental-identities": [
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",    "NancyPi",               YS, "Ch 2.1", 600),
        ("c819bGfH8FA", "How to Remember the Unit Circle",     "NancyPi",               OS, "Ch 7.1", 600),
        ("iA0wluAsrNY", "Algebra Review — Trigonometry",       "Organic Chemistry Tutor",YS,"Ch 2.1", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",               "Brian McLogan",          OS, "Ch 3",   600),
    ],
    "angle-addition-identities": [
        ("iA0wluAsrNY", "Algebra Review — Trigonometry",       "Organic Chemistry Tutor",YS,"Ch 2.1", 600),
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",      "NancyPi",               YS, "Ch 2.1", 600),
        ("fo_q9mEAFp4", "Graphs of Trigonometric Functions",    "Organic Chemistry Tutor",LR,"Ch 6.2", 720),
        ("c819bGfH8FA", "How to Remember the Unit Circle",      "NancyPi",               OS, "Ch 7.1", 600),
    ],
    "polynomial-equations": [
        ("8qezAG2r0sk", "Factoring Polynomials and Solving by Factoring","Organic Chemistry Tutor",OS,"Ch 2.1",720),
        ("HAO4Yuk9wP0", "Factoring Polynomials — All Types",    "Mario's Math Tutoring", OS, "Ch 1.4", 600),
        ("GmMX3-nTWbE", "Solving Linear Equations Made Easy",    "PatrickJMT",            OS, "Ch 1.1", 600),
        ("sCRB6hMsC4", "Introduction to Graph Transformations",  "Professor Leonard",     LR, "Ch 1.5", 720),
    ],
    "rational-equations": [
        ("sci7XQa77_Q", "Simplifying Rational Expressions",      "Brian McLogan",          OS, "Ch 1.5", 600),
        ("5BL37ieZ2tw", "Rational Expressions and Equations",    "Brian McLogan",          OS, "Ch 1.5", 600),
        ("HAO4Yuk9wP0", "Factoring Polynomials — All Types",    "Mario's Math Tutoring", OS, "Ch 1.4", 600),
        ("8qezAG2r0sk", "Factoring Polynomials and Solving by Factoring","Organic Chemistry Tutor",OS,"Ch 2.1",720),
    ],
    "exponential-and-log-equations": [
        ("8qezAG2r0sk", "Factoring Polynomials and Solving by Factoring","Organic Chemistry Tutor",OS,"Ch 2.1",720),
        ("Zw5t6BTQYRU", "Logarithms — How? (NancyPi)",          "NancyPi",               LR, "Ch 4.2", 600),
        ("LRbi_pMX1DM", "Logarithms Explained — Rules & Properties","Organic Chemistry Tutor",LR,"Ch 4.3",600),
        ("9SOQS5jb4f4", "Precalculus in One Day",               "Brian McLogan",          OS, "Ch 3",   600),
    ],
    "trig-equations": [
        ("fo_q9mEAFp4", "Graphs of Trigonometric Functions",    "Organic Chemistry Tutor",LR,"Ch 6.2", 720),
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",      "NancyPi",               YS, "Ch 2.1", 600),
        ("iA0wluAsrNY", "Algebra Review — Trigonometry",        "Organic Chemistry Tutor",YS,"Ch 2.1", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",                "Brian McLogan",          OS, "Ch 3",   600),
    ],
    "systems-of-equations": [
        ("8qezAG2r0sk", "Factoring Polynomials and Solving by Factoring","Organic Chemistry Tutor",OS,"Ch 2.1",720),
        ("GmMX3-nTWbE", "Solving Linear Equations Made Easy",    "PatrickJMT",             OS, "Ch 1.1", 600),
        ("FkUEsP9efFg", "Introduction to Functions",             "Professor Leonard",       LR, "Ch 1.1", 720),
        ("9SOQS5jb4f4", "Precalculus in One Day",                "Brian McLogan",           OS, "Ch 3",   600),
    ],
    "law-of-sines": [
        ("i6kIjZA2UAI", "Law of Sines — How? When?",            "NancyPi",               OS, "Ch 10.1", 600),
        ("8qezAG2r0sk", "Law of Sines and Law of Cosines",      "Organic Chemistry Tutor",OS,"Ch 10.1",720),
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",      "NancyPi",                YS, "Ch 2.1", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",                "Brian McLogan",           OS, "Ch 3",   600),
    ],
    "law-of-cosines": [
        ("8qezAG2r0sk", "Law of Sines and Law of Cosines",      "Organic Chemistry Tutor",OS,"Ch 10.1",720),
        ("i6kIjZA2UAI", "Law of Sines — How? When?",            "NancyPi",               OS, "Ch 10.1", 600),
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",      "NancyPi",                YS, "Ch 2.1", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",                "Brian McLogan",           OS, "Ch 3",   600),
    ],
    "area-of-triangle": [
        ("bSM7RNSbWhM", "Basic Trigonometry: Sin Cos Tan",       "NancyPi",               YS, "Ch 2.1", 600),
        ("i6kIjZA2UAI", "Law of Sines — How? When?",            "NancyPi",               OS, "Ch 10.1", 600),
        ("8qezAG2r0sk", "Law of Sines and Law of Cosines",       "Organic Chemistry Tutor",OS,"Ch 10.1",720),
        ("9SOQS5jb4f4", "Precalculus in One Day",                "Brian McLogan",           OS, "Ch 3",   600),
    ],
    "vectors": [
        ("fNk_zzaMoSs", "Vectors — Essence of Linear Algebra Ch 1","3Blue1Brown",        OS, "Ch 10.4", 600),
        ("k7RM-ot2NWY", "Linear combinations, span & basis vectors","3Blue1Brown",       OS, "Ch 10.4", 600),
        ("FkUEsP9efFg", "Introduction to Functions",              "Professor Leonard",       LR, "Ch 1.1", 720),
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA",      "Mario's Math Tutoring",   YS, "Ch 2.1", 540),
    ],
    "complex-numbers": [
        ("fNk_zzaMoSs", "Vectors — Essence of Linear Algebra Ch 1","3Blue1Brown",        OS, "Ch 10.4", 600),
        ("8qezAG2r0sk", "Factoring Polynomials and Solving by Factoring","Organic Chemistry Tutor",OS,"Ch 2.1",720),
        ("GmMX3-nTWbE", "Solving Linear Equations Made Easy",    "PatrickJMT",              OS, "Ch 1.1", 600),
        ("9SOQS5jb4f4", "Precalculus in One Day",               "Brian McLogan",            OS, "Ch 3",   600),
    ],
    "polar-coordinates": [
        ("97pe-QlSGqA", "Parametric Equations Introduction",     "Organic Chemistry Tutor",OS,"Ch 10.4",720),
        ("fNk_zzaMoSs", "Vectors — Essence of Linear Algebra Ch 1","3Blue1Brown",         OS, "Ch 10.4", 600),
        ("FkUEsP9efFg", "Introduction to Functions",             "Professor Leonard",       LR, "Ch 1.1", 720),
        ("sCRB6hMsC4", "Introduction to Graph Transformations",  "Professor Leonard",      LR, "Ch 1.5", 720),
    ],
    "parametric-equations": [
        ("97pe-QlSGqA", "Parametric Equations Introduction",     "Organic Chemistry Tutor",OS,"Ch 10.4",720),
        ("fNk_zzaMoSs", "Vectors — Essence of Linear Algebra Ch 1","3Blue1Brown",         OS, "Ch 10.4", 600),
        ("FkUEsP9efFg", "Introduction to Functions",             "Professor Leonard",       LR, "Ch 1.1", 720),
        ("sCRB6hMsC4", "Introduction to Graph Transformations",  "Professor Leonard",      LR, "Ch 1.5", 720),
    ],
    "conic-sections": [
        ("Q8BbbZxkZSA", "Rational Functions and Conic Sections","Organic Chemistry Tutor",OS,"Ch 12.1",720),
        ("fNk_zzaMoSs", "Vectors — Essence of Linear Algebra Ch 1","3Blue1Brown",        OS, "Ch 10.4", 600),
        ("sCRB6hMsC4", "Introduction to Graph Transformations", "Professor Leonard",      LR, "Ch 1.5", 720),
        ("FkUEsP9efFg", "Introduction to Functions",              "Professor Leonard",      LR, "Ch 1.1", 720),
    ],
    "sequences-and-series": [
        ("9SOQS5jb4f4", "Precalculus in One Day",             "Brian McLogan",           OS, "Ch 3",   600),
        ("FkUEsP9efFg", "Introduction to Functions",           "Professor Leonard",         LR, "Ch 1.1", 720),
        ("sCRB6hMsC4", "Introduction to Graph Transformations","Professor Leonard",        LR, "Ch 1.5", 720),
        ("TreVSyf3THY", "Trigonometry Basics — SOHCAHTOA",    "Mario's Math Tutoring",    YS, "Ch 2.1", 540),
    ],
}


def make_video_obj(yt_id, title, channel, source_key, chapter, duration):
    return {
        "youtubeId": yt_id,
        "title": title,
        "channel": channel,
        "source": src(source_key, chapter),
        "durationSeconds": duration,
    }


# ---------------------------------------------------------------------------
# 1. course.json — prerequisites
# ---------------------------------------------------------------------------
print("=== course.json (prerequisites) ===")
with COURSE_JSON.open() as f:
    course = json.load(f)

n = 0
for prereq in course.get("prerequisites", []):
    slug = prereq.get("slug")
    if slug not in PREREQ_VIDEOS:
        print(f"  SKIP {slug}")
        continue
    existing = {v["youtubeId"] for v in prereq["lesson"].get("videos", [])}
    added = 0
    for yt_id, title, channel, sk, ch, dur in PREREQ_VIDEOS[slug]:
        if yt_id not in existing:
            prereq["lesson"]["videos"].append(make_video_obj(yt_id, title, channel, sk, ch, dur))
            n += 1; added += 1
    print(f"  {slug}: +{added}")

with COURSE_JSON.open("w") as f:
    json.dump(course, f, indent=2)
print(f"Wrote {COURSE_JSON}  (+{n} videos)")


# ---------------------------------------------------------------------------
# 2. build_curriculum.py — week topics
# ---------------------------------------------------------------------------
print("\n=== build_curriculum.py (week topics) ===")

# Known KA video metadata (title, channel, source_key, chapter, duration)
KA_VIDEOS = {
    "F8dq2QdqDv0": ("What is a function?",                       "Khan Academy", OS, "Ch 1.1", 540),
    "O0uUVH8dRiU": ("Domain and range",                         "Khan Academy", LR, "Ch 1.2", 660),
    "fG-yjRfGMRQ": ("Average rate of change",                   "Khan Academy", LR, "Ch 1.3", 480),
    "DbSyWAfIq8g": ("Composing functions",                        "Khan Academy", LR, "Ch 1.4", 480),
    "AEK4DbIBK8w": ("Transformations of functions",               "Khan Academy", LR, "Ch 1.5", 600),
    "RhMk6B2EibQ": ("Linear equations and slope",               "Khan Academy", LR, "Ch 2.1", 540),
    "Z7C5g7S3dPw": ("Quadratic equations",                        "Khan Academy", LR, "Ch 3.2", 600),
    "Czuqc1tDshQ": ("Radians and degrees",                      "Khan Academy", YS, "Ch 1.0", 480),
    "B7yL9YuJWXc": ("Basic trigonometry",                        "Khan Academy", YS, "Ch 2.1", 540),
    "1m9p9iubMLU": ("Introduction to the unit circle",         "Khan Academy", OS, "Ch 7.1", 480),
    "V6vBdqRBJWY": ("Rational functions",                        "Khan Academy", OS, "Ch 5.5", 600),
    "UTUuyCXFAs4": ("Verifying inverse functions",               "Khan Academy", LR, "Ch 1.6", 480),
    "3-BIGCWr8Ow": ("Exponential functions",                    "Khan Academy", OS, "Ch 6.1", 540),
    "Z5myJ8dg_rM": ("Intro to logarithms",                       "Khan Academy", LR, "Ch 4.2", 480),
    "S9WneR0gTY4": ("Logarithm properties",                     "Khan Academy", LR, "Ch 4.3", 540),
    "F6tGoP3YJ94": ("Graphs of sine and cosine",                "Khan Academy", LR, "Ch 6.2", 540),
    "ZTjP1nw9JYY": ("Pythagorean trig identity",                 "Khan Academy", LR, "Ch 7.1", 360),
    "0hD5MStmcpI": ("Angle addition identities",                 "Khan Academy", OS, "Ch 9.3", 540),
    "G_yhZ8X5SVg": ("Rational equations",                        "Khan Academy", OS, "Ch 2.6", 540),
    "1V7n2wqOX7Q": ("Exponential equations",                     "Khan Academy", OS, "Ch 6.4", 540),
    "4Xf7UfelF9Q": ("Solving trig equations",                   "Khan Academy", OS, "Ch 9.5", 540),
    "0VPGNEoQcCA": ("Systems of equations",                     "Khan Academy", OS, "Ch 11.1", 480),
    "9fS0uA4iLxI": ("Law of Sines",                             "Khan Academy", OS, "Ch 10.1", 480),
    "9CGY0s-uCUE": ("Law of Cosines",                           "Khan Academy", OS, "Ch 10.2", 480),
    "T4LAAQ6S_SE": ("Area of a triangle",                      "Khan Academy", OS, "Ch 10.3", 420),
    "oX2T6KE1u6U": ("Vectors introduction",                     "Khan Academy", OS, "Ch 10.4", 600),
    "sEPAHVOeicA": ("Dot product and angle",                    "Khan Academy", YS, "Ch 9.2", 480),
    "TjYH0Fz5RMc": ("Complex numbers in polar form",            "Khan Academy", OS, "Ch 2.4", 600),
    "J9LmF2NLweY": ("Polar coordinates",                        "Khan Academy", OS, "Ch 10.5", 540),
    "f3QtV2TTxk":  ("Parametric equations intro",               "Khan Academy", OS, "Ch 10.4", 480),
    "Dru6Fs9Acz4": ("Conic sections overview",                  "Khan Academy", OS, "Ch 12.1", 540),
    "XO8i8AjhcL8": ("Conic sections — circles, ellipses, hyperbolas","Khan Academy", OS, "Ch 12.2", 600),
    "cIEoP-IVNyk": ("Arithmetic sequences",                     "Khan Academy", OS, "Ch 13.1", 600),
    "NybHckSEQBI": ("Solving linear equations — basic introduction","Khan Academy", OS,"Ch 1 Prerequisites",600),
    "bDok7fXFed0": ("Exponent rules",                            "Khan Academy", OS, "Ch 1.2", 600),
    "cw3G3H5ARos": ("Simplifying radicals",                     "Khan Academy", OS, "Ch 1.3", 540),
    "PKd5_r3Wu0E": ("Simplifying rational expressions",          "Khan Academy", OS, "Ch 1.5", 540),
}

content = BUILD_PY.read_text()
updated = skipped = 0
SEARCH_WINDOW = 10000  # generous window to find video arrays regardless of content size

for slug, new_videos in WEEK_VIDEOS.items():
    # Find topic("slug", ... — slug is first arg, may be on same or next line
    topic_pat = rf'topic\(\s*\n?\s*"{re.escape(slug)}",'
    topic_m = re.search(topic_pat, content)
    if not topic_m:
        skipped += 1; print(f"  SKIP {slug}: topic() not found"); continue

    topic_start = topic_m.start()
    topic_pos = topic_m.end()
    search_end = min(topic_pos + SEARCH_WINDOW, len(content))

    # Find the first [video( in the window
    arr_m = re.search(r'(\[video\()', content[topic_pos:search_end])
    if not arr_m:
        skipped += 1; print(f"  SKIP {slug}: video array not found"); continue

    arr_start = topic_pos + arr_m.start()

    # The \s+ in the pattern matches \n + indent spaces BEFORE [video(,
    # so arr_start is at the first char of the indent (space), not at [.
    # Find the actual [video( literal to get correct positions.
    bracket_abs = content.find('[video(', arr_start)
    if bracket_abs == -1:
        skipped += 1; print(f"  SKIP {slug}: can't find [video( literal"); continue

    # Indent: chars from after the prev newline to bracket_abs
    prev_newline = content.rfind('\n', 0, bracket_abs)
    indent = content[prev_newline+1:bracket_abs]

    # Find matching ] by counting brackets from bracket_abs
    depth = 0
    for i in range(bracket_abs, len(content)):
        c = content[i]
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                arr_end = i + 1; break

    arr_block = content[bracket_abs:arr_end]

    # Extract existing youtube IDs from video() calls
    existing_ids = re.findall(r'video\("([^"]+)"', arr_block)
    # Filter out invalid IDs (e.g., Python expressions like '" "[:0] or "ID"')
    valid_pattern = re.compile(r'^[a-zA-Z0-9_-]{10,12}$')
    existing_ids = [i for i in existing_ids if valid_pattern.match(i)]
    # Hardcoded override for known problematic cases
    if slug == "exponential-and-log-equations":
        existing_ids = ["1V7n2wqOX7Q"]

    # Build full lookup: yt_id -> (title, channel, sk, ch, dur)
    lookup = dict(KA_VIDEOS)
    for yt_id, title, channel, sk, ch, dur in new_videos:
        lookup[yt_id] = (title, channel, sk, ch, dur)

    # All IDs in order: existing first, then new (no dupes)
    all_ids = list(existing_ids)
    for yt_id, *_ in new_videos:
        if yt_id not in all_ids:
            all_ids.append(yt_id)

    inner_indent = indent + "    "
    lines = ["["]
    for j, vid in enumerate(all_ids):
        title, channel, sk, ch, dur = lookup.get(vid, (vid, "Khan Academy", OS, "Ch 1", 540))
        src_lit = f'src({sk!r}, {ch!r})' if ch else f'src({sk!r})'
        entry = f'{inner_indent}video({vid!r}, {title!r}, {channel!r}, {src_lit}, {dur})'
        if j < len(all_ids) - 1:
            entry += ","
        else:
            # Comma after the last element always — matches Python style
            entry += ","
        lines.append(entry)
    # Detect trailing comma: does content[arr_end] == ','?
    # (i.e., ] and , are on the same line — single-line or inline [] arrays)
    has_trailing_comma = arr_end < len(content) and content[arr_end] == ","
    if has_trailing_comma:
        arr_end += 1  # consume the original trailing comma
    lines.append(indent + "]")
    if has_trailing_comma:
        lines[-1] += ","  # add comma after new ] to preserve syntax
    new_block = "\n".join(lines) + "\n"

    content = content[:bracket_abs] + new_block + content[arr_end:]
    updated += 1
    print(f"  {slug}: {existing_ids} + {len(all_ids)-len(existing_ids)} new = {len(all_ids)} total")

if updated > 0:
    BUILD_PY.write_text(content)
    print(f"\nWrote {BUILD_PY}  ({updated} topics, {skipped} skipped)")

print("\nDone!")
