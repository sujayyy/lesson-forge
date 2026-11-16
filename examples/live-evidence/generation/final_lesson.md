# Introduction to Retrieval‑Augmented Generation (RAG)

## Start here
Retrieval‑Augmented Generation, called RAG, is a way to get better answers from an AI. First we have a question. Then we look in our own notes for a short piece of text that may help. We give that text and the question to a language model – a computer program that can write sentences after learning from many examples. The model uses the text to write an answer. This whole process is called RAG because we **retrieve** (find) useful text and then **generate** (write) an answer [S1].

AI means software that can do tasks that usually need human thinking, like answering questions. A language model is a type of AI that has read lots of written material and learned how words fit together. Its learning is called *training* – it looks at many examples and remembers patterns. The model’s original training does not contain our personal notes, so we bring those notes in at the time of answering [S1].

## What it means
In simple words, RAG means “use our own notes to help the AI answer”. We do not change the AI’s brain. We only give it extra information at the moment we need an answer. This extra information can be a sentence, a paragraph, or any short passage that we think is useful.

## Why it helps
When the AI only relies on its earlier learning, it may miss recent facts or private details. By adding a fresh passage, we give the model something it definitely knows. Experiments show that this often makes answers more factual, though it does not guarantee every answer is correct [S2].

## How it works
RAG follows four easy steps:
1. **Prepare readable notes** – write short, clear sentences that anyone can read.
2. **Find useful text** – when a question arrives, scan the notes and pick the passage that looks most relevant.
3. **Give the text and the question to the language model** – the model sees both together.
4. **Write the answer** – the model combines the passage with its own knowledge to produce a response.

We say “search the notes” instead of “query an index” and “use the supplied text” instead of talking about complex tools. The model does not learn again from the passage; it only uses it for this answer [S1][S3].

## A worked example
**Fictional example:** A notice posted on the wall of **Lotus College** library reads:

> "Lotus College library opens at 9 am and closes at 5 pm on weekdays."

A student named Ravi asks: **"When does the library close on weekdays?**"

1. **Prepare notes** – the notice itself is the note.
2. **Find useful text** – the phrase *"closes at 5 pm on weekdays"* directly answers the question.
3. **Give to model** – we show the model the passage and Ravi’s question.
4. **Write answer** – the model replies: *"The library closes at 5 pm on weekdays."* This answer is supported by the note.

Ravi then asks: **"What is the library's phone number?**"
The notice contains no phone number, so step 2 finds no relevant passage. We must tell Ravi that the note does not provide the answer, rather than making one up. A correct response is: *"The notice does not provide a phone number for the library.*"

## Limits
RAG is not magic. The retrieved passage may be outdated, wrong, or unrelated. The model can still add mistakes even when the passage is correct. If the notes lack the needed information, we must say so. RAG does not guarantee perfect answers, only that evidence can improve reliability [S2][S3].

## Try it yourself
1. **How does the four‑step RAG process help the model give a better answer?**
   *Answer:* It gives the model fresh, reliable text that it can use, reducing reliance on old knowledge.
2. **What should you do if your notes do not contain the answer to a question?**
   *Answer:* State that the notes do not provide the answer, instead of inventing information.

## Recap
RAG stands for Retrieval‑Augmented Generation. We first write clear notes, then find a short passage that matches a question, give both to a language model, and finally write an answer. The method can make answers more factual, but it can still be wrong, and missing evidence must be reported honestly.

## Sources
- [S1] https://aws.amazon.com/what-is/retrieval-augmented-generation/
- [S2] https://arxiv.org/abs/2005.11401
- [S3] https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview