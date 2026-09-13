---
title: "The Compiler Nobody Read, Part 2: Born Dead"
date: 2026-09-12
tags: compilers, verification, ai
description: Peter Naur said you can't have a program without understanding it. He was right; now it's a bigger problem.
---

*Part 2 of 3. Part 1, [What Naur Said](/the-compiler-nobody-read-1/), is a one-page reading of the paper this rests on. Next: [Part 3: The Spec Is the Theory](/the-compiler-nobody-read-3/).*

*Peter Naur said you can’t have a program without understanding it. He was right; now it’s a bigger problem.*

In February 2026, Nicholas Carlini at Anthropic [pointed sixteen Claude agents at a blank directory](https://www.anthropic.com/engineering/building-c-compiler) and came back two weeks later with a C compiler: a hundred thousand lines of Rust that builds Linux 6.9 on three architectures, compiles QEMU, FFmpeg, SQLite and PostgreSQL, passes 99% of the GCC torture tests, and cost about $20,000 in tokens. Nobody has read it: there is now a compiler that builds Linux and no human who could say why any function in it is the way it is.

Two months later, [four agents at Basis Research](https://www.basis.ai/blog/verified-compiler/) tried something harder: a JavaScript-to-WebAssembly compiler in Lean, with a proof that it’s correct. Fourteen days, 93,516 lines, 3,026 commits — and it did not verify: fourteen goals unproved, seventeen axioms unjustified.

Then I did a third one. A swarm of agents wrote an [ALGOL 68 compiler in Lean 4](https://github.com/zvikinoza/algol68-lean) generating LLVM, with the correctness theorems stated in Lean and checked by the Lean kernel. I have not read the implementation. I know the semantics of ALGOL 68 and what the theorems say; the machine knows the rest.

Three compilers. One works and nobody understands it. One was supposed to be proved correct and couldn’t be. One is proved correct and nobody understands it either. Peter Naur, who edited the ALGOL 60 report and led one of the first ALGOL compilers, argued in 1985 that none of this should be possible.

## What Naur actually said

The paper is [Programming as Theory Building](https://pages.cs.wisc.edu/~remzi/Naur.pdf) ([read the real one](https://stuartmarks.wordpress.com/2026/02/24/naurs-theory-building-as-internet-samizdat/)). His claim is about what programming *produces*, and his answer is: not the code, which is a residue. What comes out is a theory — an understanding, held in the heads of particular people, of how the problem is being solved by running the program. A person who holds it can do three things documentation can’t: **relate** the code to the world it’s for, **justify** why each part is the way it is and not otherwise, and **extend** the program for a request nobody anticipated so that it still makes sense.

Then the famous part: the theory can’t be written down, a program dies when the people who hold its theory leave, and reviving it from documentation is “strictly impossible.” A dead program still runs; you find out it’s dead when someone asks for a change and nobody can answer intelligently. His evidence: a group inherits a compiler with full documentation, annotated source and the original authors’ advice, and still proposes changes that ignore structure the documentation describes at length. Ten years on, “the original powerful structure was still visible, but made entirely ineffective by amorphous additions of many different kinds.”

Everything since has gone his way: developers spend [58% of their time understanding code and 5% editing it](https://doi.org/10.1109/TSE.2017.2734091); a team’s knowledge of its own system [halves in about four months](https://doi.org/10.1145/3510457.3513082). So why don’t we care more?

## The assumption he never wrote down

Because of something so obvious in 1985 that Naur never stated it: *you could not get the program without building the theory.* Somebody had to decide, line by line, what each part should be and why, so the theory came free with the labour. Every knowledge metric the field has — truck factor, degree-of-authorship, degree-of-knowledge — reads understanding off authorship.

That assumption is now false. For the first time in the history of programming, a working program can exist without anyone, ever, having held a theory of it. Carlini’s compiler is a hundred thousand lines of it. Naur even said why the theory can’t be written down: it rests on similarities that “cannot be expressed in terms of criteria, no more than the similarities of… human faces, tunes, or tastes of wine.” Every one of those is now a solved machine-learning problem — and a model that recognizes faces hasn’t *expressed* anything you could read. It makes the judgment instead of you: fluently, with explanations, indistinguishable from the work of someone who holds the theory. That fluency removes the only thing that ever forced a human to understand: that otherwise nothing got written.

## How a theory gets built

If “theory” is a real thing and not a metaphor, it should be built by a process you can watch. The cleanest result in the neuroscience of learning is that the brain’s activity *while you encode* something predicts whether you’ll remember it. Two 1998 *Science* papers showed it: scan people while they study, test them later, sort the encoding trials by outcome, and the remembered items show more activation — left inferior prefrontal and medial temporal for [words](https://doi.org/10.1126/science.281.5380.1188), right prefrontal and parahippocampal for [pictures](https://doi.org/10.1126/science.281.5380.1185). It’s the subsequent memory effect; a [meta-analysis of 74 fMRI studies](https://doi.org/10.1016/j.neuroimage.2010.09.045) finds the same regions every time.

Two things drive it. **Mismatch**: memory forms preferentially when something violates what you expected. [Five experiments on scene-object pairs](https://doi.org/10.1016/j.jml.2016.11.001) found learning strongest when a pairing contradicted a prior, and [a follow-up](https://doi.org/10.1101/lm.053410.121) found a violated prediction yields more detailed memory only when the prediction was strong. You have to have guessed — which is why a programmer’s deepest knowledge of a system is a scar from something that failed (speaking from experience :)). **Generation**: producing an answer beats being handed it by about [0.4 standard deviations across 86 studies](https://doi.org/10.3758/BF03193441). Even wrong answers help ([guessing first](https://doi.org/10.1037/a0015729), [confident errors](https://doi.org/10.1146/annurev-psych-010416-044022)), and it’s physical: [pupils dilate more when you generate than when you read](https://doi.org/10.3758/s13421-025-01791-0), retrieval [strengthens hippocampal–prefrontal coupling](https://doi.org/10.1016/j.neuropsychologia.2013.04.004), [activity during a practice test predicts recall a week later](https://doi.org/10.1016/j.neuroimage.2013.03.071), and controlling what you look at helps [unless your hippocampus is damaged](https://doi.org/10.1038/nn.2693).

So the loop is: predict, get it wrong, feel the mismatch, encode. A few thousand times over a codebase and what you have is Naur’s theory — not mystical, just the residue of a specific kind of effort, and that effort shows up on a scanner.

![The theory-building loop: predict, mismatch, encode](/static/img/theory-loop.png)

## How it doesn’t get built

Now hand the same person an assistant that answers before they’ve guessed. No prediction, nothing to be wrong about; no mismatch, nothing to encode. The loop doesn’t close. The effort that was doing the work has a name in cognitive load theory: germane load, the part that builds the schema rather than fighting the interface.

Give students a science problem with an LLM instead of a search engine and germane load drops by [more than a standard deviation, and that drop fully mediates the drop in the quality of their reasoning](https://doi.org/10.1016/j.chb.2024.108386). Not correlates. Mediates. And the person doesn’t notice: [search access makes people believe they personally understand what they just looked up](https://doi.org/10.1037/xge0000070), and across [10,462 people](https://doi.org/10.1093/pnasnexus/pgaf316) those who learned from an LLM synthesis came away with shallower knowledge and sparser, less original advice than those who searched — and didn’t know it.

The body agrees. [Burelli et al.](https://arxiv.org/abs/2606.20598), a registered report with hypotheses locked before data, gave sixty programmers two Java tasks, one with a chat assistant and one without: engagement index down, blink rate up, and skin conductance — the body’s effort signal — tracked performance without the assistant and stopped tracking it with. Effort came unhooked from result. Their summary: “AI-assisted programming is not a faster version of solo coding but a cognitively distinct activity.” The widely shared [MIT essay study](https://arxiv.org/abs/2506.08872) is a preprint whose connectivity numbers are [between-group contrasts](https://arxiv.org/abs/2601.00856) (“55% less brain” is a misreading), but its behavioural result is solid: 83% of people who wrote with a model couldn’t quote their own essay afterward, against 11% of those who didn’t.

The outcomes all have the same shape. High-schoolers with a stock ChatGPT interface did [48% better on practice and 17% worse on the unassisted exam](https://doi.org/10.1073/pnas.2422633122) (Wow). Professional developers, mostly senior, learning a new library with AI [scored 17% lower afterward and saved no time](https://arxiv.org/abs/2601.20245). People who built software with an unrestricted assistant [got it working 92% of the time and could fix an injected bug 23% of the time](https://arxiv.org/abs/2602.20206); people who wrote it themselves fixed it 69% of the time. [Better essays, no gain in knowledge or transfer](https://doi.org/10.1111/bjet.13544). The artifact improves. The understanding doesn’t move. (The bridge from the learning literature to the AI results is a mechanism, not yet a measurement.)

## I want to tell you it “shrinks” your brain

I believed it. I can’t. Less activity doesn’t mean less thinking — Poldrack’s [whole thesis](https://doi.org/10.1016/j.dcn.2014.06.001) is that “neural efficiency” as an explanation is empty — and in program comprehension less activation is what expertise looks like ([meaningful names](https://doi.org/10.1145/3106237.3106268), [experts reading code like prose](https://doi.org/10.1109/ICSE.2017.24)). Offloading to a knowledge assistant even [lowers prefrontal activation while the people with the biggest drop remember more](https://doi.org/10.1038/s41598-023-39540-5).

But the two readings of “engagement went down” predict different things. If it’s efficiency, performance holds when you take the tool away; if it’s disengagement, it drops. Activation can’t tell you which; what happens after the assistant is gone can, and every number in the previous section is that measurement. Disengagement (and the efficiency effect [reverses for hard tasks](https://doi.org/10.1016/j.neubiorev.2009.04.001) anyway).

Atrophy is another matter: the adult brain does regress without practice — [juggling grows grey matter in three months and it shrinks back in three more](https://doi.org/10.1038/427311a); [two weeks in a cast thins the matching cortex](https://doi.org/10.1212/WNL.0b013e31823fcd9c) — but nobody has ever measured brain structure as a function of using any cognitive tool: not GPS, not calculators, not AI. The study everyone cites for GPS and the hippocampus [collected no imaging at all](https://doi.org/10.1038/s41598-020-62877-0), and in the juggling study [the grey matter went back down while the participants could still juggle](https://doi.org/10.1371/journal.pone.0002669). Anyone who tells you language models shrink your brain has zero evidence — and here’s why it doesn’t matter much.

## Born dead

Atrophy assumes something was there to waste. Look at every result above: the students never had the theory, the developers were learning a new library, the bug-fixers had never written the code. Nothing wasted away; it never formed. The worry is that AI makes experienced people forget; the evidence is that it stops inexperienced-at-this-thing people from ever learning — and with respect to any particular system, everybody is inexperienced-at-this-thing on day one. That’s how theories start. Now they don’t.

Here Naur’s picture is too gentle: his death condition is an event — the team “is dissolved” — and assumes the theory once lived. Now it needn’t have. The program is *born dead*: not dead because the people who understood it left, but because there never were such people. Correct on arrival, deployed on arrival, understood by no one at any moment of its existence.

“Nobody understands the code” isn’t new; nobody understands the output of gcc -O3 or the contents of node_modules either. The difference is where it sits: compiler output lives below a stable interface, and a package has a maintainer, a version and ten thousand other users hammering on it. Generated code lands at the exact surface where change requests arrive — your repo, your name on the commit, no contract, no owner. Old generated code was born dead where nobody would need to touch it. New generated code is born dead exactly where they will.

And Naur’s alarm is disconnected. Route a change request to a model and it *is* answered, plausibly and often correctly, and the loop still doesn’t close for anyone. Across 302,600 AI-authored commits, [22.7% of the issues introduced were still there at the latest revision](https://arxiv.org/abs/2603.28592). What nobody understands doesn’t get fixed, and nobody notices, because everything still runs. We’re even losing the ability to measure this: METR found experienced maintainers [19% slower with AI while believing they were 20% faster](https://arxiv.org/abs/2507.09089), then tried to rerun the study and [gave up](https://metr.org/blog/2026-02-24-uplift-update/), partly because “30% to 50% of developers told us that they were choosing not to submit some tasks because they did not want to do them without AI.” The control group is walking out of the experiment.


*Continued in [Part 3: The Spec Is the Theory](/the-compiler-nobody-read-3/).*
