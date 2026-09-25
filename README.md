# The Unofficial Guide

**Rebecca Yanni — Corpus: `campus_life`**

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

I used the campus_life corpus, which contains short posts about university life, including courses, housing, dining, and administrative information. My system takes a question from the user, searches the corpus for relevant chunks, and uses those chunks to generate an answer. It can answer questions such as how much time a course takes each week, how a course is assessed, or when students should start a project. If the retrieved information is not relevant enough to the question, the system returns that it does not have enough information instead of just trying to guess.

## Chunking Strategy

**Chunk size:** One complete document per chunk
**Overlap:** 0
I chose to keep each document as one chunk because the campus_life corpus is made up of short posts that usually focus on one topic. The 88 documents average about 317 characters, and even the longest document is only 549 characters. When I looked through the documents, the useful information was usually contained within the short post, so splitting them into smaller pieces could separate information from its context. Keeping each post together made more sense for my corpus and allowed each chunk to contain a complete thought without needing overlap.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`
```
On the add/drop deadline
You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology
I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.
Expect 9 to 11 hours a week, the heaviest first-year course by reputation.
The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```
**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History
People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.
It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall
Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.
Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```


**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like
Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.
The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.
The bad: no air conditioning, which matters for the first three weeks of September.
Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** How many hours per week outside of class should students expect to spend on CS 210?


**Answer:**

```
Students should expect to spend 8 to 10 hours a week outside of class on CS 210.
Sources: `course_cs_210_workload.txt` and `course_cs_210.txt`
```

**My relevance cutoff:**

0.6 -- I kept the relevance cutoff at 0.6 after testing all five in-corpus questions and all five out-of-scope questions. The in-corpus distances ranged from 0.209 to 0.386, while the out-of-scope distances ranged from 0.825 to 0.932. There was a large gap between the highest in-corpus distance, 0.386, and the lowest out-of-scope distance, 0.825, so 0.6 sits safely between the two groups.

| Question | In corpus? | Best distance |
|---|---|---|
| How many hours per week outside of class should students expect to spend on CS 210? | Yes | 0.281 |
| How many hours per week should students expect to spend on PHYS 130 during lab weeks? | Yes | 0.249 |
| How are students assessed in MATH 220 Linear Algebra? | Yes | 0.386 |
| How many hours per week outside of class should students expect to spend on STAT 150? | Yes | 0.263 |
| When should students start the term project for CS 340 Databases? | Yes | 0.209 |
| What is the capital of Mongolia? | No | 0.825 |
| What happens if I put oil in a diesel engine? | No | 0.932 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen? | No | 0.832 |
| How do I write a for loop in Rust? | No | 0.896 |

## How I Used AI

1. I asked AI to explain the starter chunker.py code and give me a few possible chunking strategies for the campus_life corpus. It suggested keeping each short post as one chunk because most of the documents were already small and focused on one topic. Instead of just using the suggestion, I checked the corpus statistics and printed 5 sample chunks. After seeing that the documents averaged about 317 characters and the samples were complete thoughts, I decided to use one document per chunk with no overlap. Another time is also when I asked AI to help me interpret the retrieval distances I recorded while testing my relevance cutoff. It suggested comparing the highest distance from my in-corpus questions with the lowest distance from my out-of-scope questions instead of changing the cutoff just because it was the starter value. My in-corpus results ranged from 0.209–0.386 and my out-of-scope results ranged from 0.825–0.932. Based on those results, I decided not to change the 0.6 cutoff because it already fell clearly between the 2 groups.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Named source contains the information used | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |


<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Real Output — Before

**Results file:** `results/run_2026-09-23_2034_before.md`  
**Scoring function:** `judge()` in `scorer.py`

**Criterion 1 — Retrieved chunks contain the answer**

For the CS 210 question, the system retrieved `course_cs_210.txt` and `course_cs_210_workload.txt` with a best distance of 0.2814.

> Students should expect to spend 8 to 10 hours a week outside of class on CS 210.

All five test questions retrieved a chunk containing the expected answer in each run.

**Criterion 2 — Every answer names a source**

For the PHYS 130 question, the system produced:

> Students should expect to spend 10 hours a week on PHYS 130 during lab weeks (7 hours a week, plus 3 on lab weeks).
>
> Source: `course_phys_130.txt` and `course_phys_130_workload.txt`

All five answers named at least one source in each run.

**Criterion 3 — Gate stops out-of-corpus questions**

The relevance gate produced:

```text
refused (best distance 0.825) What is the capital of Mongolia?
refused (best distance 0.934) How do I change the oil in a diesel engine?
refused (best distance 0.886) Who won the 1994 World Cup?
refused (best distance 0.844) What is the recommended dosage of ibuprofen for a headache?
refused (best distance 0.896) How do I write a for loop in Rust?
```

The gate refused 5 of 5 out-of-scope questions.

**Criterion 4 — Sampled chunks read as complete thoughts**

The sampled chunks kept the relevant information together without cutting off the information needed to understand the chunk. All 5 sampled chunks read as complete thoughts, which matched the complete-document chunking strategy from Unit 1.

**Criterion 5 — Named source contains the information used**

For the CS 340 question, the system produced:

> Students should start the term project in week three, not week eight (`course_cs_340.txt` and `course_cs_340_exams.txt`).

The named sources contained the information used in the answer for all five test questions.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All 5 test questions retrieved chunks containing the expected information in all three runs, which is above my target of 4 out of 5. |
| 2 | Every answer names a source | MET | All 5 answers named at least one source document in all three runs, meeting my target of 5 out of 5. |
| 3 | Gate stops out-of-corpus questions | MET | The relevance gate refused all 5 out-of-scope questions, which is above my target of 4 out of 5. |
| 4 | Sampled chunks read as complete thoughts | MET | All 5 sampled chunks kept the important information together and could be understood on their own, which is above my target of 4 out of 5. |
| 5 | Named source contains the information used | MET | For all 5 test questions, the source named in the answer contained the information used to answer the question, which is above my target of 4 out of 5. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->
     No criteria were missed during the baseline evaluation, so there was no failed pipeline stage to diagnose. All 5 in-corpus questions passed in all 3 runs, and the relevance gate also refused all 5 out-of-scope questions.

     Looking at the results, some of my original targets were probably a little safe. Criteria 1, 4, and 5 only required 4 out of 5 even though the system achieved 5 out of 5 during testing. If I were making the criteria stricter, I would tighten Criterion 1 from 4 out of 5 to 5 out of 5 because retrieving the correct information is necessary before the model can generate a grounded answer.

     Even though nothing failed, the retrieval distances still give me something useful to examine. The 5 in-corpus questions had best distances between about 0.209 and 0.386, while the out-of-scope questions had distances between about 0.825 and 0.934. This left a large gap around the current 0.6 relevance cutoff.

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
