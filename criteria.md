# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
I chose 4 out of 5 because each of my questions has an answer in the documents I selected, so I expect the system to retrieve the correct information most of the time. I still allowed for one question to be missed because retrieval may not always return the best chunk.
---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
I chose every answer because my system is supposed to answer questions using the documents in my corpus. Naming a source for every answer lets the user know where the information came from and makes the answer easier to verify.
---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
 I chose 4 out of 5 because the system should recognize and reject most questions that have nothing to do with my documents. I allowed one mistake because the relevance gate may occasionally find an unrelated chunk that appears similar to the question.
---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

At least 4 of the 5 sampled chunks should read as a complete thought without important information being cut off.

**Why this target:**

I chose 4 out of 5 because the campus life documents are short and usually explain their main information in only a few sentences. I want the chunks to keep enough of those sentences together so they make sense on their own, while allowing for one chunk that may not split perfectly.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

For at least 4 of my 5 test questions, the source named in the answer should actually contain the information used to answer the question.

**Why this target:**
I chose 4 out of 5 because naming a source is only useful if that source actually supports the answer. I expect the system to connect most answers to the correct document, but I allowed for one mistake in case it retrieves similar information from another document.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
## Unit 9 Capstone Criteria

1. **Warm end-to-end latency on `/ask` stays under 2.0 seconds for at least 9 of 10 uncached in-corpus requests.**
   - *Why this target:* Across my initial 10 uncached runs, average latency was `1,460 ms`, with 9 of 10 finishing between `605 ms` and `1,648 ms` and one Gemini API spike reaching `4,437 ms`. Setting a 2.0-second ceiling at `9 of 10` absorbs occasional upstream Gemini API jitter while catching genuine regressions or cold-start delays on warm requests without making the bar so loose (`5 seconds`) that every run passes automatically.

2. **Every `/ask` request writes a complete, valid JSONL record to `logs/runs.jsonl` with all 14 required fields (`timestamp`, `corpus`, `question`, `status`, `http_status`, `refused`, `answer`, `sources`, `best_distance`, `latency_ms`, `prompt_tokens`, `output_tokens`, `total_tokens`, `error`) in 10 of 10 runs.**
   - *Why this target:* Observability only works if no request disappears silently or writes malformed JSON. A `10 of 10` target is strict because file-append logging in `serve.py` is deterministic and any missing record or missing key would break post-run log analysis.

3. **Token instrumentation in `logs/runs.jsonl` reports non-zero `prompt_tokens`, `output_tokens`, and `total_tokens` (`prompt_tokens + output_tokens == total_tokens`) on 5 of 5 uncached in-corpus `/ask` calls, and `0` tokens on 5 of 5 gate-refused out-of-scope calls.**
   - *Why this target:* My cost measurement depends on `generate.token_counts()` deltas accurately capturing Gemini API usage when a call reaches the model and confirming zero model spend when `gate.py` refuses an out-of-scope query at the `0.5` cutoff. Anything less than `5 of 5` means token accounting or the gate bypass is broken.

4. **Failure path — Bad or missing input on `POST /ask` (empty JSON `{}`, blank `{"question": "   "}`, or non-JSON body) returns HTTP `400` with an `error` message and appends a `status: "bad_request"` record to `logs/runs.jsonl` in 5 of 5 requests.**
   - *Why this target:* Client input errors should never trigger an unhandled Python exception (`HTTP 500`) or go unlogged. `5 of 5` is required because input validation in `serve.py` runs before retrieval or model generation and should handle every malformed payload predictably.

5. **Out-of-scope queries on `POST /ask` are refused (`refused: true`, `http_status: 200`, `best_distance > 0.5`) with the standard refusal string in 5 of 5 requests.**
   - *Why this target:* Wrapping the RAG pipeline in Flask/Gunicorn must preserve the `0.5` relevance gate tuned in Unit 2 so off-topic HTTP requests do not hallucinate answers or waste Gemini tokens. `5 of 5` matches my baseline gate performance while verifying zero regression in the HTTP wrapper.