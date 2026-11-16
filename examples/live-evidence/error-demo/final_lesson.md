# Introduction to Retrieval‑Augmented Generation (RAG)

## Start here
Artificial Intelligence (AI) is software that can do tasks that normally need human thinking, such as answering questions. A language model is a type of AI that writes text after learning patterns from many examples. Training means the model looked at many sentences and learned how words usually follow each other. Retrieval‑Augmented Generation, or RAG, is a way to get better answers from a language model. First we look for useful text in our own notes. Then we give that text together with a question to the language model, which uses the text to help write its answer [S1].

## What it means
RAG stands for Retrieval‑Augmented Generation. *Retrieval* means finding a short piece of text, called a passage, that may contain the answer. *Augmented* means we add this passage to the model’s input. *Generation* means the model creates the final answer. The model does not learn new facts during this step; it only reads the supplied passage while answering [S1].

## Why it helps
If the model’s original learning does not include a recent fact, the retrieved passage can fill the gap. Experiments show that using retrieved information makes answers more factual than using the model alone, but it does not guarantee every answer is right [S2]. RAG also lets us keep private notes separate from the model, so we do not have to retrain the model for each new piece of information.

## How it works
RAG follows four simple steps:
1. **Prepare readable notes** – write short, clear sentences about the topics you care about.
2. **Find useful text** – when a question arrives, search the notes for a passage that may answer it. Simple word matching is enough [S3].
3. **Give the passage and the question to the language model** – the model reads both together.
4. **Write the answer** – the model produces a response and can cite the passage as evidence.
Looking up a passage does not change the model’s training; it only supplies extra information at answer time [S1].

## A worked example
Imagine a notice posted at **Lotus College**:
> *Lotus College library opens at 9 am and closes at 5 pm on weekdays.*

A student asks: **“When does the library close on weekdays?”**
We search the notice and find the sentence that says *closes at 5 pm*. We give the model the passage and the question. The model replies:
> *The library closes at 5 pm on weekdays.*
The answer matches the passage, so we can cite the notice as evidence.

Another student asks: **“What is the library’s phone number?”**
We search the notice again but find no phone number. Because the required information is missing, we must tell the student that the notice does not contain the answer. A correct reply is:
> *The notice does not provide the library’s phone number.*
This shows how RAG handles both answered and unanswered queries.

## Limits
RAG can only be as good as the notes you provide. If the notes are old, wrong, or missing, the model may give a wrong answer or have to say it does not know. The model itself can still make mistakes even when the passage is correct. RAG does not automatically search the whole internet; it only looks at the notes you give it [S3].

## Try it yourself
1. **Question:** How does the model use the retrieved passage?
   - **Answer:** The model reads the passage together with the question and bases its answer on that information. This follows step 3 of the four‑step process.
2. **Question:** What should you do if the notes do not contain the answer?
   - **Answer:** Tell the asker that the notes do not have the needed information, instead of making up an answer. This follows the principle that a reference shows where information came from and you should not invent facts [S3].

## Recap
RAG = Retrieval‑Augmented Generation. It combines a simple search of our own notes with a language model that writes answers. The four steps are: prepare notes, find a passage, give passage + question to the model, and write the answer. RAG can improve factuality but it still depends on the quality of the notes, and the model may err.

## Sources
- [S1] https://aws.amazon.com/what-is/retrieval-augmented-generation/
- [S2] https://arxiv.org/abs/2005.11401
- [S3] https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview