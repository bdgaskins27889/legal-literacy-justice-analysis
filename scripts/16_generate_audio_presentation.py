"""
Script: 16_generate_audio_presentation.py
Purpose: Generate professional narrated audio for all 16 presentation slides
         using Google Text-to-Speech (gTTS), then combine into a single MP3 file.
Author: Barbara D. Gaskins
Project: The Scales of Justice — DSC 680 Capstone
"""

import os
import time
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment

# ── Configuration ──────────────────────────────────────────────────────────────
OUTPUT_DIR = Path("/home/ubuntu/legal_literacy_justice_project/outputs/audio")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LANG = "en"       # English
TLD  = "com"      # US English accent (com = standard American)

# ── Slide Scripts ──────────────────────────────────────────────────────────────
SLIDES = [
    (1, "title",
     "Good morning, afternoon, or evening. My name is Barbara Gaskins, and I am presenting "
     "my capstone project for DSC 680. This project, titled The Scales of Justice, uses "
     "federal sentencing data to ask a deceptively simple question: does the type of lawyer "
     "you have actually change the outcome of your case? The answer, as the data will show, "
     "is a resounding yes. The implications reach far beyond the courtroom, touching on "
     "fundamental questions of fairness and equity in our justice system. We will explore "
     "how data science can illuminate these critical issues and offer pathways toward a "
     "more just system."),

    (2, "central_question",
     "The Sixth Amendment guarantees every defendant the right to an attorney. But the "
     "right to an attorney is not the same as the right to an equally resourced attorney. "
     "Public defenders are among the most dedicated lawyers in the country, but they are "
     "systematically overworked and underfunded. The American Bar Association recommends "
     "a maximum of 150 felony cases per year per attorney. Studies show many public "
     "defenders carry two to three times that load. This study uses data science to ask "
     "whether that resource gap translates into a sentencing gap. We are asking if the "
     "type of legal representation predicts the severity of a federal sentence. This "
     "question is central to understanding whether our ideal of equal justice under law "
     "is truly realized in practice. To answer this, we turn to a robust and publicly "
     "available dataset."),

    (3, "dataset",
     "The dataset powering this analysis comes directly from the U.S. Sentencing Commission. "
     "This is the independent federal agency responsible for establishing sentencing policies "
     "for the federal courts. This data is publicly available, fully anonymized, and updated "
     "annually, making it ideal for reproducible research. From the over 27,000 available "
     "variables, I selected 23 that are most relevant to our research question. The most "
     "critical variable records whether a defendant was represented by a private attorney, "
     "a public defender, or represented themselves. This comprehensive dataset allows us "
     "to build a strong conceptual framework for our analysis."),

    (4, "conceptual_framework",
     "Before diving into the numbers, it is important to understand the conceptual model "
     "guiding this research. I am not simply asking whether race predicts sentencing. "
     "That relationship is well-documented in the literature. I am asking whether legal "
     "representation mediates that relationship. In other words, does part of the reason "
     "Black and Hispanic defendants receive harsher sentences operate through the fact "
     "that they are more likely to have court-appointed counsel? This framework illustrates "
     "that pathway. The analysis tests for both a direct effect of race on sentencing and "
     "an indirect effect operating through the type of legal representation. Disentangling "
     "these two pathways is the core analytical challenge of this project, and it leads "
     "us to our first significant finding."),

    (5, "finding_racial_disparities",
     "This chart presents one of the most striking findings of the exploratory analysis. "
     "When we look at the raw prison sentence rates by race and ethnicity, we see a "
     "20-percentage-point gap between White, non-Hispanic defendants and Hispanic defendants. "
     "Nearly 93 out of every 100 Hispanic defendants in federal court in fiscal year 2024 "
     "received a prison sentence, compared to roughly 72 out of 100 White defendants. "
     "It is critical to note that this is a descriptive finding. It does not yet control "
     "for offense severity, criminal history, or type of representation. That is exactly "
     "what the modeling phase does. But this raw disparity is the starting point, and it "
     "demands explanation. This finding sets the stage for understanding how attorney type "
     "further influences these outcomes."),

    (6, "finding_representation_gap",
     "While the previous slide showed racial disparities in prison sentences, this slide "
     "reveals perhaps the most policy-relevant finding: the profound impact of attorney "
     "type on sentence length. When we look at average sentence length broken down by the "
     "type of attorney, the differences are dramatic. Defendants with private attorneys "
     "averaged 53.2 months in prison. Defendants with public defenders averaged 78.4 months, "
     "a difference of over two years. Defendants who represented themselves averaged 88.1 "
     "months, nearly three years longer than those with private counsel. A critical thinker "
     "will immediately ask: is this just because wealthier defendants who can afford "
     "private attorneys also tend to commit less serious crimes? That is a fair challenge, "
     "and it is precisely what the regression models are designed to address by controlling "
     "for offense severity and criminal history. Now, let us explore the methodology we "
     "used to answer that question."),

    (7, "methodology",
     "To rigorously test these relationships, we developed three distinct models, each "
     "designed to answer a slightly different question. The Logistic Regression is our "
     "workhorse baseline; it gives us a clean, interpretable view of the relationships "
     "between demographics, attorney type, and sentencing. The Multilevel Model is more "
     "sophisticated. It recognizes that federal sentencing does not happen in a vacuum. "
     "A case in the Southern District of New York is processed in a very different "
     "environment than a case in the Eastern District of Texas. By adding a random "
     "intercept for each district, the model accounts for this geographic variation. "
     "Finally, the Mediation Analysis is the most theoretically interesting. It directly "
     "tests the hypothesis that legal representation is the mechanism through which racial "
     "disparities in sentencing operate. So, how did these models perform?"),

    (8, "model_performance",
     "In terms of raw predictive performance, all three models are strong. An AUC-ROC "
     "above 0.80 is generally considered a good model; above 0.85 is considered very good. "
     "The Multilevel Model leads with an AUC of 0.88 and an accuracy of 77.8 percent, "
     "meaning it correctly predicts the sentencing outcome for more than three out of every "
     "four cases. However, accuracy alone is an insufficient standard for a model that "
     "could be used in a justice context. A model could be highly accurate overall while "
     "being systematically wrong for a particular racial group. That is why the fairness "
     "audit is not an afterthought; it is the central evaluation criterion. Let us see "
     "how they fared on fairness."),

    (9, "fairness_analysis",
     "This is the most important slide in the presentation. The 80 percent rule, originally "
     "developed by the Equal Employment Opportunity Commission for employment discrimination "
     "cases, provides a clear, defensible threshold for evaluating whether a model has a "
     "disparate impact on a protected group. The standard Logistic Regression model fails "
     "this test with a ratio of 0.706, meaning the model is significantly more likely to "
     "predict prison for Black and Hispanic defendants than for White defendants, even "
     "after controlling for other factors. The Multilevel Model, by contrast, passes with "
     "a ratio of 0.816. This is not a marginal improvement. The Multilevel Model is "
     "dramatically better across all fairness metrics. Now, let us unpack why this model "
     "is so much fairer."),

    (10, "why_fairer",
     "Why does the Multilevel Model perform so much better on fairness? The answer lies "
     "in what statisticians call omitted variable bias. Federal districts are not racially "
     "neutral environments. Some districts have historically higher incarceration rates; "
     "some have more resources for public defenders; some have different prosecutorial "
     "cultures. When a standard model ignores these district-level differences, it "
     "inadvertently attributes to race what is actually a function of geography. By "
     "explicitly modeling the district as a random effect, the Multilevel Model separates "
     "these two sources of variation. The result is a model that is both more accurate "
     "and more fair, a rare and important outcome that demonstrates that fairness and "
     "accuracy are not inherently in tension."),

    (11, "discussion",
     "Let me step back from the numbers for a moment and discuss what this all means. "
     "Three conclusions stand out. First, legal representation is not just symbolically "
     "important; it is quantifiably important. Even after we control for what you did, "
     "your criminal history, and where you were sentenced, who represents you still "
     "predicts how long you will be incarcerated. Second, this study is a cautionary "
     "tale for anyone who believes that algorithms are inherently neutral. The standard "
     "logistic regression model, built from real data, learned and reproduced the biases "
     "embedded in that data. Third, and most importantly, this study offers a path "
     "forward. The Multilevel Model shows that with more thoughtful modeling choices, "
     "we can build tools that are both accurate and fair. This leads us directly to "
     "some actionable policy recommendations."),

    (12, "policy_implications",
     "This research is not just an academic exercise. It points toward three concrete "
     "policy recommendations. First, the most direct intervention is also the most "
     "straightforward: fund public defenders adequately. The data shows a clear "
     "correlation between representation quality and outcomes. Second, any jurisdiction "
     "considering the use of predictive analytics in sentencing or bail decisions must "
     "require a fairness audit as a condition of deployment. The tools exist; the will "
     "to use them must be mandated. Third, the modeling community should adopt multilevel "
     "approaches as a standard for justice applications. The improvement in fairness is "
     "significant, the computational cost is minimal, and the ethical stakes are too "
     "high to use less rigorous methods. Of course, no study is without its limitations, "
     "and it is important to acknowledge those."),

    (13, "limitations",
     "Good science is honest about its limitations. This study uses federal court data, "
     "which covers a relatively small and specialized slice of the American criminal "
     "justice system. The vast majority of criminal cases, over 95 percent, are handled "
     "in state courts, where the dynamics may be quite different. Additionally, while "
     "the statistical controls are rigorous, this is an observational study. We cannot "
     "randomly assign defendants to different attorney types, so we cannot claim "
     "causation with certainty. Future work should extend this framework to state-level "
     "data, incorporate earlier stages of the process like charging and plea bargaining, "
     "and explore the compounding effects of race, gender, and socioeconomic status "
     "together. These limitations, however, do not diminish the core findings."),

    (14, "conclusion",
     "I want to close with a reflection on why this work matters. The criminal justice "
     "system is one of the most consequential institutions in American life. Decisions "
     "made within it affect not just individuals, but families and communities for "
     "generations. Data science cannot solve the deep structural inequities in this "
     "system. But it can illuminate them with a precision and scale that was not "
     "previously possible. It can hold models accountable to fairness standards. And "
     "it can provide policymakers with the evidence they need to act. The scales of "
     "justice are not perfectly balanced today. But with rigorous, responsible data "
     "science, we can understand exactly where the imbalance lies, and that is the "
     "first step toward correcting it. Thank you."),

    (15, "qa",
     "I have prepared answers to each of the questions you see on this slide. I will "
     "address them as they arise during the question and answer period. But I want to "
     "briefly acknowledge the most important one: is it ethical to use a model that "
     "still has some bias? My answer is: it depends on the alternative. If the "
     "alternative is a human decision-maker who is also biased, and the research on "
     "judicial bias is extensive, then a model that is more transparent, auditable, "
     "and demonstrably fairer may be the more ethical choice. The goal is not a "
     "perfect model. The goal is a more just system."),

    (16, "references",
     "One of the core commitments of this project is full transparency and "
     "reproducibility. Every figure, every statistic, and every model result in this "
     "presentation can be independently verified. The data is freely available from "
     "the U.S. Sentencing Commission. The code is documented and available on GitHub. "
     "The random seed is fixed. I invite anyone who questions a finding to run the "
     "analysis themselves. That is what responsible data science looks like. "
     "Thank you for your time and attention."),
]


def generate_slide_audio(slide_num: int, slug: str, text: str) -> Path:
    """Generate TTS audio for a single slide using gTTS."""
    output_path = OUTPUT_DIR / f"slide_{slide_num:02d}_{slug}.mp3"
    print(f"  [{slide_num:02d}/16] Generating: {slug}...")
    tts = gTTS(text=text, lang=LANG, tld=TLD, slow=False)
    tts.save(str(output_path))
    size_kb = output_path.stat().st_size / 1024
    print(f"         ✓ Saved ({size_kb:.0f} KB)")
    return output_path


def combine_audio_files(audio_files: list, output_path: Path):
    """Combine all MP3 audio files into a single polished MP3."""
    print(f"\n  Combining {len(audio_files)} segments into final presentation...")
    combined = AudioSegment.silent(duration=800)   # brief intro silence

    for i, audio_file in enumerate(audio_files):
        segment = AudioSegment.from_mp3(str(audio_file))
        # Normalize volume to -18 dBFS for consistent loudness
        target_dBFS = -18.0
        change_in_dBFS = target_dBFS - segment.dBFS
        segment = segment.apply_gain(change_in_dBFS)
        combined += segment
        combined += AudioSegment.silent(duration=2200)  # 2.2s pause between slides

    combined += AudioSegment.silent(duration=800)   # brief outro silence

    combined.export(
        str(output_path),
        format="mp3",
        bitrate="128k",
        tags={
            "title":  "The Scales of Justice — Narrated Presentation",
            "artist": "Barbara D. Gaskins",
            "album":  "DSC 680 Capstone Project, Bellevue University",
            "year":   "2026",
            "comment": "Generated for Milestone 3 submission"
        }
    )

    duration_min = len(combined) / 1000 / 60
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ Final file: {output_path.name}")
    print(f"  ✓ Duration  : {duration_min:.1f} minutes")
    print(f"  ✓ File size : {size_mb:.1f} MB")
    return duration_min


def generate_timing_guide(audio_files: list, output_path: Path):
    """Generate a slide timing guide for the presenter."""
    lines = [
        "# Slide Timing Guide — The Scales of Justice\n\n",
        "**Presenter**: Barbara D. Gaskins | **Course**: DSC 680 | **Date**: March 2026\n\n",
        "| Slide | Title | Start Time |\n",
        "|:------|:------|:-----------|\n"
    ]
    cumulative = 0.8  # 0.8s intro silence
    for audio_file, (slide_num, slug, _) in zip(audio_files, SLIDES):
        seg = AudioSegment.from_mp3(str(audio_file))
        duration_sec = len(seg) / 1000
        m = int(cumulative // 60)
        s = int(cumulative % 60)
        title = slug.replace("_", " ").title()
        lines.append(f"| {slide_num} | {title} | {m:02d}:{s:02d} |\n")
        cumulative += duration_sec + 2.2

    with open(str(output_path), "w") as f:
        f.writelines(lines)
    print(f"  ✓ Timing guide: {output_path.name}")


def main():
    print("=" * 65)
    print("  THE SCALES OF JUSTICE — AUDIO PRESENTATION GENERATOR")
    print("  Barbara D. Gaskins | DSC 680 Capstone | March 2026")
    print("=" * 65)
    print(f"\n  Engine : Google Text-to-Speech (gTTS)")
    print(f"  Output : {OUTPUT_DIR}\n")

    # ── Step 1: Generate individual slide audio ────────────────────────────────
    print("STEP 1: Generating individual slide narrations")
    print("-" * 65)
    audio_files = []
    for slide_num, slug, text in SLIDES:
        audio_path = generate_slide_audio(slide_num, slug, text)
        audio_files.append(audio_path)
        time.sleep(0.5)   # polite delay between API calls

    print(f"\n  ✓ All {len(audio_files)} slide narrations generated.\n")

    # ── Step 2: Combine into single presentation audio ─────────────────────────
    print("STEP 2: Combining into single narrated presentation")
    print("-" * 65)
    final_output = OUTPUT_DIR / "Scales_of_Justice_Narrated_Presentation_Gaskins.mp3"
    duration = combine_audio_files(audio_files, final_output)

    # ── Step 3: Timing guide ───────────────────────────────────────────────────
    print("\nSTEP 3: Generating presenter timing guide")
    print("-" * 65)
    timing_path = OUTPUT_DIR / "slide_timing_guide.md"
    generate_timing_guide(audio_files, timing_path)

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  AUDIO PRESENTATION COMPLETE")
    print("=" * 65)
    print(f"\n  Main audio file : {final_output.name}")
    print(f"  Total duration  : {duration:.1f} minutes")
    print(f"  Timing guide    : {timing_path.name}")
    print(f"  Individual files: {len(audio_files)} MP3 files in outputs/audio/")
    print("\n  Ready for Milestone 3 submission.\n")


if __name__ == "__main__":
    main()
