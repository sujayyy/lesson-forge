# Introduction to Retrieval‑Augmented Generation (RAG)

## Start here
Retrieval‑Augmented Generation, or RAG, is a way to get better answers from an AI system. First we look for useful text in our own notes. Then we give that text together with a question to a language model, which is software that writes text after learning from many examples. The model uses the supplied text to help it answer. This is one sentence that defines RAG for the first time [S1].

## What it means
RAG means *Retrieval‑Augmented Generation*. Retrieval is the act of finding a short piece of text (a passage) that may contain the answer. Augmented means we add this passage to the model’s input. Generation is the model writing the final answer. A language model is a program that produces words after being trained on large collections of text. Training is simply learning patterns from examples, not remembering every fact forever [S1].

## Why it helps
When the model’s original learning does not contain the latest fact, the retrieved passage can fill the gap. Studies show that using retrieved information makes answers more factual than relying on the model alone, although it does not guarantee every answer is correct [S2]. It also lets us keep private notes separate from the model, so the model does not need to be re‑trained for each new piece of information.

## How it works
RAG follows four easy steps:
1. **Prepare readable notes** – write short, clear sentences about the topics you care about.
2. **Find useful text** – when a question appears, search the notes for a passage that may answer it.
3. **Give the passage and the question to the language model** – the model reads both.
4. **Write the answer** – the model produces a response, citing the passage if needed.
The search can be as simple as looking for matching words; no complex tools are required [S3]. The model does not learn from this lookup; it only uses the passage at answer time [S1].

## A worked example
Imagine a notice posted at **Lotus College**:
> *Lotus College library opens at 9 am and closes at 5 pm on weekdays.*
A student asks: **"When does the library close on weekdays?"**
We search the notice and find the exact sentence that says *closes at 5 pm*. We give the model the passage and the question. The model replies:
> *The library closes at 5 pm on weekdays.*
The answer matches the passage, so we can cite the notice as evidence.
Now another student asks: **"What is the library's phone number?"**
We search the notice again but find no phone number. Because the required information is missing, we must tell the student that the notice does not contain the answer. A correct reply is:
> *The notice does not provide the library’s phone number.*
This shows how RAG handles both answered and unanswered queries.

## Limits

RAG guarantees that every answer is correct.
RAG can only be as good as the notes you provide. If the notes are old, wrong, or missing, the model may give a wrong answer or have to say it does not know. The model itself can still make mistakes even when the passage is correct. RAG does not search the whole internet unless you deliberately add web pages to your notes [S3].

## Try it yourself
1. **Question:** How does the model use the retrieved passage?
   - **Answer:** The model reads the passage together with the question and bases its answer on that information. This follows step 3 of the four‑step process.
2. **Question:** What should you do if the notes do not contain the answer?
   - **Answer:** Tell the asker that the notes do not have the needed information, instead of making up an answer. This follows the principle that a reference shows where information came from and you should not invent facts [S3].

## Recap
RAG stands for Retrieval‑Augmented Generation. It combines a simple search of our own notes with a language model that writes answers. The four steps are: prepare notes, find a passage, give passage + question to the model, and write the answer. It helps make answers more accurate, but it works only as well as the notes we have, and the model can still err.

## Sources
- [S1] https://aws.amazon.com/what-is/retrieval-augmented-generation/
- [S2] https://arxiv.org/abs/2005.11401
- [S3] https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview