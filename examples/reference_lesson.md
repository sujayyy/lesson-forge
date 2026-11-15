# Introduction to RAG: Help an AI answer with notes

## Start here

Imagine asking a college helper, "When does the library close?"
The helper guesses, "At six."
But the latest notice says five.
A clear answer can still be wrong.

Now give the helper the notice before asking.
The helper can check it and answer using the right information.
This is the main idea we will learn.
You do not need to know coding to understand it.

AI means artificial intelligence.
It is software that does tasks which often need human intelligence.
A language model is a kind of AI trained on text to produce text.
For example, it can write an answer to a question. [S1]
It may not know your college's latest notice.

## What it means

RAG stands for Retrieval-Augmented Generation.
The name sounds difficult, but its three parts are simple.
Retrieval means finding useful information.
Augmented means given extra help.
Generation means creating an answer.

RAG finds useful information and gives it to a language model.
The model then uses that information to write an answer. [S1]
Think of a student answering with a textbook open.
The textbook helps, but the student must still read it correctly.
This comparison explains the idea; a model is not a human student.

## Why it helps

A model's training may not include new information or private documents. [S1]
For example, a college may change its library hours today.
A system using the updated notice can help students find the new hours.
It can also show the notice used for the answer.
That makes the answer easier to check. [S3]

RAG does not need to search the whole internet.
It can search only the documents a college gives it. [S3]
This is useful when the answer is inside a small, trusted collection.

## How it works

First, prepare the documents.
Collect the notices, make their text readable, and organise them for search.
Long documents can be split into smaller pieces called passages.

Next, a student asks a question.
The system searches the documents for useful passages.
Searching by words is one option; more advanced methods are also possible. [S3]

Then, the system sends the question and the selected passages to the language model.
These passages are extra information the model can use for this answer.
Finally, the model writes an answer using them. [S1]

The order is: prepare notes, find useful text, give it to the model, then answer.
Looking up a notice does not itself retrain the model. [S1]
The system is supplying information for the current question.

## A worked example

This is a fictional example from an Indian college.
The college, notice and times are invented for practice.

Source note: "Lotus College library opens at 9 am and closes at 5 pm on weekdays."

Meena asks: "When does the library close on weekdays?"

The search finds this passage: "closes at 5 pm on weekdays."
The system gives this passage and Meena's question to the model.

A supported answer is: "It closes at 5 pm on weekdays, according to the library notice."
The answer matches the note.
Meena can check the note herself.

Now Meena asks: "Is the library open on Sunday?"
The note says nothing about Sunday.
A careful answer is: "This notice does not give Sunday hours. Please check with the library."
The system should not turn weekday hours into a Sunday answer.

## Limits

RAG can still give wrong answers. [S2]
The search may miss the right passage.
The notice itself may be old.
The model may misunderstand a passage or add an unsupported detail. [S3]

So, check that the source is suitable and the answer matches it.
A reference helps you check; it is not a promise that every claim is true. [S3]
When the notes do not answer the question, the system should say so.
An honest gap is better than a confident guess.

## Try it yourself

Question one: Why must the system find a passage before writing the answer?

Answer: The model needs useful evidence for this question.
Finding the passage first gives it information to use when writing.

Question two: A notice says the library opens at 9 am on weekdays.
Can we use that notice to say it opens at 9 am on Sunday?

Answer: No.
Sunday is not covered by the notice.
Say that the notice does not give the answer, and ask the library.

## Recap

RAG helps a language model answer using information found in documents.
Remember the order: find useful text, supply it with the question, and write an answer.
Good notes help, but they do not remove every possible mistake.
Always check the evidence and admit when it is missing.

## Sources

[S1] AWS: What is Retrieval-Augmented Generation?
https://aws.amazon.com/what-is/retrieval-augmented-generation/

[S2] Lewis and colleagues: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
https://arxiv.org/abs/2005.11401

[S3] Microsoft Learn: Retrieval augmented generation overview
https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
