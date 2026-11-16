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

---

# Unit 2

## How I Use AI

1. I used AI to help me organize and interpret my Unit 2 testing results, but I made the final decisions based on the actual output from my system.  Since all 5 criteria passed, there was not a failed stage to fix. Instead, I used the measured gap between the in-corpus distances of about 0.209–0.386 and the out-of-scope distances of about 0.825–0.934 to decide on a stricter relevance gate. AI suggested a few possible changes, including changing the prompt or retrieval settings so I checked the actual code in `config.py`, `store.py`, and `generate.py` before choosing anything. I decided to make only one system change by lowering the relevance threshold from 0.6 to 0.5. I then ran the full evaluation again instead of assuming the change helped. The after results showed that all 5 in-corpus questions still passed in all 3 runs and all 5 out-of-scope questions were still refused. 

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Named source contains the information used | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |


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

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All 5 test questions retrieved chunks containing the expected information in all three runs, which is above my target of 4 out of 5. |
| 2 | Every answer names a source | MET | All 5 answers named at least one source document in all three runs, meeting my target of 5 out of 5. |
| 3 | Gate stops out-of-corpus questions | MET | The relevance gate refused all 5 out-of-scope questions, which is above my target of 4 out of 5. |
| 4 | Sampled chunks read as complete thoughts | MET | All 5 sampled chunks kept the important information together and could be understood on their own, which is above my target of 4 out of 5. |
| 5 | Named source contains the information used | MET | For all 5 test questions, the source named in the answer contained the information used to answer the question, which is above my target of 4 out of 5. |

## Diagnoses

No criteria were missed during the baseline evaluation, so there was no failed pipeline stage to diagnose. All 5 in-corpus questions passed in all 3 runs, and the relevance gate also refused all 5 out-of-scope questions. Looking at the results, some of my original targets were probably a little safe. Criteria 1, 4, and 5 only required 4 out of 5 even though the system achieved 5 out of 5 during testing. If I were making the criteria stricter, I would tighten Criterion 1 from 4 out of 5 to 5 out of 5 because retrieving the correct information is necessary before the model can generate a grounded answer.
Even though nothing failed, the retrieval distances still give me something useful to examine. The 5 in-corpus questions had best distances between about 0.209 and 0.386, while the out-of-scope questions had distances between about 0.825 and 0.934. This left a large gap around the current 0.6 relevance cutoff.

## The Improvement

**What I changed:**

I lowered the relevance threshold from 0.6 to 0.5 in `config.py`.

**Why I picked it:**

My baseline testing showed that the highest in-corpus distance was around like 0.386, while the lowest out-of-scope distance was about 0.825. Since there was a large gap between the 2 groups, I made the relevance gate more conservative by lowering the cutoff to 0.5 while still leaving room above every in-corpus test question.


### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Named source contains the information used | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

The stricter 0.5 relevance threshold preserved the same results as the baseline. All five in-corpus questions passed in all three runs, and the gate refused all five out-of-scope questions.

Results file: `results/run_2026-09-25_1815_after.md`

**Did it help?**

Yes it helped, the change made the relevance gate stricter without reducing performance on my test set. Before and after this change, all 5 in-corpus questions passed in all 3 runs and all 5 out-of-scope questions werent accepted. The improvement did not increase the number of criteria met because the baseline already met all 5 criteria, but it made the system more like conservative about answering questions with weaker retrieval matches.

## What's Still Broken

None of my five acceptance criteria were still missed after the improvement but this doesn't mean the system will work perfectly for every possible question. My evaluation only uses five in-corpus questions and five out-of-scope questions, so there could still be questions that fall closer to the 0.5 relevance threshold or retrieve a related document that does not actually contain enough information to answer correctly so I stopped after the one threshold change because Unit 2 had asked for one diagnosis-driven improvement, and the after evaluation showed that the stricter gate preserved the performance of the baseline system.

## What I'd Do Differently

If I started over, I would probably make my original acceptance criteria a little more stricter because a lot of my targets were lower than what the system consistently achieved. For example, I would require Criterion 1 to retrieve the answer for 5 out of 5 test questions instead of 4 out of 5. I would also test more questions near the relevance boundary instead of just only using questions that were clearly in-scope or clearly out-of-scope. This would give me better evidence for choosing the relevance threshold and help reveal cases where a question is related to campus life but the retrieved documents do not have enough info to answer it.


## Capstone

**What This Extends**

This extends my Project 1 system, **The Unofficial Guide** (`ai201-project1-unofficial-guide-starter-v2026`), a RAG question-answering pipeline over the 88-document `campus_life` corpus that embeds one full post per chunk (`chunker.py`), filters out-of-scope queries using a 0.5 distance cutoff (`config.py`, `store.py`), and generates source-cited answers (`generate.py`). The extension wraps `ask_pipeline` in a Gunicorn/Flask HTTP service (`serve.py`) with `/health`, `/ask`, and `/logs` endpoints, structured JSONL logging to `logs/runs.jsonl`, and per-request latency and token instrumentation.

**The Shape**

Shape A — Deploy and instrument (Path B: Local with logs). I am adding a lightweight HTTP wrapper around the existing `campus_life` RAG pipeline so it runs outside my editor via Gunicorn, writes a structured JSON record for every request (including 400 and 500 failures), and measures per-run token consumption and end-to-end latency across repeated trials.

Out of scope:
- I am not changing the one-document-per-chunk strategy in `chunker.py`, the vector store in `store.py`, or the 0.5 relevance threshold in `config.py`.
- I am not altering the generation prompt templates or adding new retrieval strategies in `generate.py`.
- I am not building a custom frontend interface or adding automated retry/fallback loops beyond logging failures when they occur.

**Running It**

Path B — Local with logs. See `RUNNING.md` for the Python version requirement (`3.11`–`3.13`), pinned dependencies (`requirements.txt`), bundled ONNX embedding model details (`all-MiniLM-L6-v2`, ~80 MB), clean-checkout setup steps, and the single command to index and start Gunicorn (`python app.py index && gunicorn serve:app --workers 1 --bind 127.0.0.1:5000`).

**Instrumentation**

Each request appends one JSON record to `logs/runs.jsonl` (and can also be queried via `GET /logs`) with the following named fields: `timestamp`, `corpus`, `question`, `status`, `http_status`, `refused`, `answer`, `sources`, `best_distance`, `latency_ms`, `prompt_tokens`, `output_tokens`, `total_tokens`, and `error`.

Logged entries from a live Gunicorn session (10 uncached `/ask` calls plus 1 malformed-input `400` bad request):

```json
{"timestamp": "2026-11-16T20:53:52.330667+00:00", "corpus": "campus_life", "question": "", "status": "bad_request", "http_status": 400, "refused": null, "answer": null, "sources": [], "best_distance": null, "latency_ms": 0.02, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0, "error": "Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}"}
{"timestamp": "2026-11-16T20:55:28.495226+00:00", "corpus": "campus_life", "question": "How many hours per week outside of class should students expect to spend on CS 210?", "status": "ok", "http_status": 200, "refused": false, "answer": "Students should expect to spend 8 to 10 hours a week outside of class on CS 210 (course_cs_210_workload.txt and course_cs_210.txt).", "sources": ["course_cs_210.txt", "course_cs_210_workload.txt", "course_cs_340.txt", "course_econ_101_workload.txt", "course_stat_150_workload.txt"], "best_distance": 0.2814, "latency_ms": 1647.99, "prompt_tokens": 617, "output_tokens": 47, "total_tokens": 664, "error": null}
{"timestamp": "2026-11-16T20:55:30.149153+00:00", "corpus": "campus_life", "question": "How many hours per week should students expect to spend on PHYS 130 during lab weeks?", "status": "ok", "http_status": 200, "refused": false, "answer": "Students should expect to spend 7 hours a week, plus an additional 3 hours on lab weeks (totaling 10 hours), on PHYS 130 (source: `course_phys_130_workload.txt` and `course_phys_130.txt`).", "sources": ["course_biol_160.txt", "course_biol_160_workload.txt", "course_phys_130.txt", "course_phys_130_workload.txt", "course_stat_150_workload.txt"], "best_distance": 0.2488, "latency_ms": 1079.16, "prompt_tokens": 593, "output_tokens": 63, "total_tokens": 656, "error": null}
{"timestamp": "2026-11-16T20:55:31.233859+00:00", "corpus": "campus_life", "question": "How are students assessed in MATH 220 Linear Algebra?", "status": "ok", "http_status": 200, "refused": false, "answer": "Students in MATH 220 Linear Algebra are assessed through two midterms and a cumulative final, which is curved to a B- median. \n\nSource: course_math_220.txt (also mentioned in course_math_220_exams.txt)", "sources": ["course_cs_210.txt", "course_cs_210_exams.txt", "course_math_220.txt", "course_math_220_exams.txt", "course_math_220_workload.txt"], "best_distance": 0.3863, "latency_ms": 4436.88, "prompt_tokens": 573, "output_tokens": 58, "total_tokens": 631, "error": null}
{"timestamp": "2026-11-16T20:55:35.676252+00:00", "corpus": "campus_life", "question": "How many hours per week outside of class should students expect to spend on STAT 150?", "status": "ok", "http_status": 200, "refused": false, "answer": "Students should expect to spend 5 to 6 hours a week outside of class on STAT 150 (source: course_stat_150.txt and course_stat_150_workload.txt).", "sources": ["course_cs_210_workload.txt", "course_cs_340.txt", "course_econ_101_workload.txt", "course_stat_150.txt", "course_stat_150_workload.txt"], "best_distance": 0.2628, "latency_ms": 914.19, "prompt_tokens": 604, "output_tokens": 48, "total_tokens": 652, "error": null}
{"timestamp": "2026-11-16T20:55:36.595501+00:00", "corpus": "campus_life", "question": "When should students start the term project for CS 340 Databases?", "status": "ok", "http_status": 200, "refused": false, "answer": "Students should start the term project in week three, not week eight. \n\nSource documents: `course_cs_340_exams.txt` and `course_cs_340.txt`", "sources": ["course_cs_210_exams.txt", "course_cs_210_workload.txt", "course_cs_340.txt", "course_cs_340_exams.txt", "course_cs_340_workload.txt"], "best_distance": 0.2093, "latency_ms": 1299.65, "prompt_tokens": 560, "output_tokens": 44, "total_tokens": 604, "error": null}
{"timestamp": "2026-11-16T20:55:37.899625+00:00", "corpus": "campus_life", "question": "What is the add/drop deadline and when does a drop show as a W?", "status": "ok", "http_status": 200, "refused": false, "answer": "You can add a course through the end of the second week, and dropping ends at the end of week six. A drop shows as a W on your transcript if it happens after week two. \n\nSource: admin_add_drop_deadline.txt", "sources": ["admin_add_drop_deadline.txt", "admin_grade_appeals.txt", "admin_pass_fail_option.txt", "admin_withdrawal_deadline.txt", "course_cs_340_workload.txt"], "best_distance": 0.3042, "latency_ms": 839.77, "prompt_tokens": 526, "output_tokens": 52, "total_tokens": 578, "error": null}
{"timestamp": "2026-11-16T20:55:38.741274+00:00", "corpus": "campus_life", "question": "How many hours a week does BIOL 160 Cell Biology take?", "status": "ok", "http_status": 200, "refused": false, "answer": "BIOL 160 Cell Biology takes 9 to 11 hours a week. \n\nSource: course_biol_160.txt (and course_biol_160_workload.txt)", "sources": ["course_biol_160.txt", "course_biol_160_exams.txt", "course_biol_160_workload.txt", "course_engl_205_workload.txt", "course_phys_130_workload.txt"], "best_distance": 0.2529, "latency_ms": 714.94, "prompt_tokens": 553, "output_tokens": 49, "total_tokens": 602, "error": null}
{"timestamp": "2026-11-16T20:55:39.461487+00:00", "corpus": "campus_life", "question": "How much reading per week is required for HIST 118 Modern World History?", "status": "ok", "http_status": 200, "refused": false, "answer": "For HIST 118 Modern World History, you can expect a lot of reading, about 120 pages a week (course_hist_118.txt and course_hist_118_workload.txt).", "sources": ["course_engl_205.txt", "course_engl_205_workload.txt", "course_hist_118.txt", "course_hist_118_exams.txt", "course_hist_118_workload.txt"], "best_distance": 0.2157, "latency_ms": 1532.67, "prompt_tokens": 598, "output_tokens": 50, "total_tokens": 648, "error": null}
{"timestamp": "2026-11-16T20:55:40.999222+00:00", "corpus": "campus_life", "question": "When should I eat at Pellew Dining Hall to avoid peak wait times?", "status": "ok", "http_status": 200, "refused": false, "answer": "To avoid peak wait times at Pellew Dining Hall, you should go before 11:45 (from `dining_pellew_dining_hall_followup.txt`).", "sources": ["dining_halden_hall_followup.txt", "dining_kestrel_commons_followup.txt", "dining_pellew_dining_hall.txt", "dining_pellew_dining_hall_followup.txt", "dining_the_ridgeway_cafe_followup.txt"], "best_distance": 0.2006, "latency_ms": 605.27, "prompt_tokens": 712, "output_tokens": 39, "total_tokens": 751, "error": null}
{"timestamp": "2026-11-16T20:55:41.608140+00:00", "corpus": "campus_life", "question": "What is Innisfree Hall like and how much does laundry cost?", "status": "ok", "http_status": 200, "refused": false, "answer": "According to `housing_innisfree_hall.txt`, Innisfree Hall was built in 1991 and renovated in 2022. It features double rooms arranged as pairs that share one bathroom between two rooms, and it has no air conditioning. \n\nLaundry at Innisfree Hall costs $1.75 to wash and $1.75 to dry, and it is app-based (`housing_innisfree_hall.txt` and `housing_innisfree_hall_laundry.txt`).", "sources": ["housing_aldridge_hall.txt", "housing_calder_annexe.txt", "housing_innisfree_hall.txt", "housing_innisfree_hall_laundry.txt", "housing_morrow_house.txt"], "best_distance": 0.2365, "latency_ms": 1532.31, "prompt_tokens": 763, "output_tokens": 113, "total_tokens": 876, "error": null}