---
title: "The Compiler Nobody Read, Part 3: The Spec Is the Theory"
date: 2026-09-12
tags: compilers, verification, ai
description: If nobody holds the theory, correctness had better not depend on anybody holding it. What proof moves, what it can't, and what I'd measure.
---

*Part 3 of 3. [Part 1: What Naur Said](/the-compiler-nobody-read-1/) · [Part 2: Born Dead](/the-compiler-nobody-read-2/). Part 2 ended with programs that are born dead: correct on arrival, understood by no one. This part is about what to do instead.*

## Why “better models” is the wrong answer

The standard response — more capable, better aligned, more faithful to what you meant — answers a different question. Alignment is about whether the system does what it was asked; the problem here is whether anyone knows what should have been asked, and whether anyone can answer the *next* request. A perfectly aligned model writing perfectly correct code to a perfectly stated intent leaves a born-dead program exactly as dead. So the answer is forced: if nobody holds the theory, correctness had better not depend on anybody holding it.

Every other way of knowing a program is correct has a lifetime — a human theory halves every four months, documentation is stale immediately, tests cover the cases somebody thought of. A machine-checked proof re-runs, every build, forever, by a kernel that doesn’t forget. The proofs of the TLS handshake in Amazon’s s2n have been [replayed 956 times since November 2016 and needed three manual updates](https://doi.org/10.1007/978-3-319-96142-2_26). When AWS built Cedar against a Lean model, the proof [found four validator bugs that had gotten past review and tests](https://arxiv.org/abs/2407.01688). After [more than 325 bugs were found in every C compiler tested](https://doi.org/10.1145/1993498.1993532), the one exception was CompCert, the verified one. Even partial verification works at scale: memory-safety bugs went from [76% of Android vulnerabilities to 24%](https://security.googleblog.com/2024/09/eliminating-memory-safety-vulnerabilities-Android.html) as new code moved to Rust. None of these guarantees care whether anybody understands the code — the property a born-dead program needs.

Ten years ago the obstacle was cost: seL4’s proof took [20 person-years against 2.2 for the kernel](https://doi.org/10.1145/2560537), 48 lines of proof per line of code. But models now close proof obligations — [over 90% of a set of Verus proofs](https://arxiv.org/abs/2409.13082), [proofs for 23 previously-unproven functions merged into a real kernel](https://arxiv.org/abs/2605.03822), [a 7B model re-proving half of seL4’s theorems](https://arxiv.org/abs/2602.08384). On real open goals from live Lean projects the honest number is [about a third, not the 90% on math benchmarks](https://arxiv.org/abs/2603.02668). A third is a lot more than zero.

## Three compilers, again

Now the Basis result. Their own diagnosis of why 93,516 lines didn’t verify: the agents “could not reason at depth.” They couldn’t generalize a relation that was too weak, or hold a negative constraint across sessions. They “wrote semantics that passed tests but were opaque to proof.”

Read that next to relate, justify, extend. Semantics that pass tests but can’t be proved: code that works and nobody can say why. A relation that can’t be generalized: a change that can’t be made constructively. A constraint that doesn’t survive the session: a theory never held. The loop in the diagram never ran, because an agent reset every session has nowhere to encode to. And the tests passed the whole time — which should worry you about Carlini’s compiler, tested and not proved: 99% on the torture suite is a statement about the cases someone thought of.

So why did mine work? Partly because ALGOL 68’s semantics are unusually rigorously specified, so the theorems had something exact to say; mostly because I didn’t ask for a compiler and then a proof. I gave the agents the theorem, and the compiler was whatever satisfied it; the kernel rejected everything else, every time. Every agentic-proof result has the same shape: [agents are good at closing obligations](https://arxiv.org/abs/2607.06341) and bad at deciding what should be proved. That’s not a capability gap the next model closes. It’s the theory, and it’s still the human’s.

## The catch

Write W for what the world needs from a program, S for its specification, and C for the code. Then

(C ⊨ S) ∧ (S ⊨ W) ⟹ the program does what the world needs.

The left half is machine-checkable. The right half isn’t, and never will be — Naur’s whole argument is about the right half. So verification doesn’t remove the theory; it moves it. Call the theory burden B = |S| / |C|, the fraction a human still has to hold in their head. Without verification B = 1, and increasingly nobody holds it. Ironclad’s trusted spec is [3,546 lines against about 7,000 of implementation](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/hawblitzel), B ≈ 0.5; Cedar’s Lean model is [1,673 lines against 24,915 of Rust](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/), B ≈ 0.07.

That’s the proposal: proof moves the theory out of a large, implicit, generated codebase into a small, explicit, reviewable specification — smaller, so the irreducible human part is bounded; more stable, because it changes when the world changes, not when the implementation does; and the one artifact a machine refuses to proceed without. Naur observed that nobody writes the rationale down. The spec *is* the rationale, and the kernel won’t let you skip it.

The bad news is crisp. Across 946 problems, models turn a description into [code 92% of the time, a specification 48%, a proof 14%, and all the way through 5%](https://arxiv.org/abs/2605.08553). [A large fraction of verifier-accepted specs are “incorrect or incomplete… in ways invisible to the verifier”](https://arxiv.org/abs/2604.00280) — one benchmark’s 87% verification rate drops to 2% once you grade the specs — and some models [game the checker with vacuous postconditions](https://arxiv.org/abs/2509.22908). Models are good at the half a machine can check and bad at the half only a human can. B shrinks; it doesn’t hit zero. Lean’s creator Leonardo de Moura wrote in February that “someone has to read the theorem statements and confirm they capture the intended mathematics. This is the human contract that no amount of automation can eliminate.” Naur said it forty-one years earlier in [the companion paper](https://doi.org/10.1007/3-540-15199-0_5): whether a specification matches “the matters of the world that are of concern to the user” is a question “that can only be ascertained intuitively.” He meant it as a limit. Read it now and it’s a design brief.

## Naur’s remedy, finally affordable

Naur offered two ways out. Apprenticeship — put the new person “in close contact with the programmers who already possess the theory” — is closing: [junior developer employment is down about 20% from its 2022 peak](https://digitaleconomy.stanford.edu/app/uploads/2025/11/CanariesintheCoalMine_Nov25.pdf). The other was radical: throw the text away and let a new team solve the problem fresh. Nobody could afford that; it’s about to become the cheapest option there is.

But regeneration without theory is just Naur’s story at scale — “amorphous additions” arriving in bulk — *unless the rebuild has to satisfy the same theorem the last one did*. Then throwing the code away is safe. The spec is what you keep; the code is a proof-carrying cache of it, regenerated whenever you like — new model, new backend, new performance target — as long as the kernel says yes. That inverts Naur: he said the theory keeps the program alive, but a verified program has a life that doesn’t need a theory-holder — born dead and, in the only sense that matters for maintenance, immortal.

Hence GPU kernels. CUDA, Triton, Pallas, cuTile: small, hot, rewritten constantly, increasingly model-generated, and checked by [running them, a weak oracle](https://arxiv.org/abs/2606.20128). But their specs are short and mathematical, which is where verification has always worked. [Kuiper already does it in F*](https://doi.org/10.1145/3808280) with cuBLAS-competitive matmul and proofs; what’s missing is the bottom of the stack — Kuiper’s extraction to CUDA is trusted, [there’s no verified LLVM backend](https://doi.org/10.1145/3453483.3454030), and bounded validation on AArch64 [found 45 miscompilations](https://doi.org/10.1145/3763147). “Lean, compiled verifiably to LLVM” is a research program; [CakeML](https://doi.org/10.1145/2535838.2535841) shows the shape.

My own compiler’s theorems are checked by the Lean kernel — a real guarantee, the one Basis couldn’t get — but not “the binary is correct.” [Lean’s own FAQ](https://lean-lang.org/faq/) says the trusted base at runtime includes the Lean compiler, runtime, code generator and whatever you linked in; the kernel itself is unverified, and [the project to verify a reimplementation](https://arxiv.org/abs/2403.14064) found a soundness bug on the way. Agent-written proofs are safe at all only because the kernel checks every one, so [a model can’t get an unsound one past it](https://arxiv.org/abs/2605.30106). What it can do is prove the wrong theorem — the spec problem, which is Naur’s problem. I don’t hold the theory of my compiler. I hold the theory of ALGOL 68 and of what the theorems say, and that is small enough that I actually can.

## What I’d measure

Every test needs an unassisted phase, because you can’t measure theory with the assistant in the room, and a delay, because [immediate measurement understates and can invert the effect](https://doi.org/10.1111/j.1467-9280.2006.01693.x). Then: give two groups an unfamiliar verified system, one with code plus docs, one with spec plus proof, and a week later ask both to relate, justify and extend. If the spec group doesn’t win, specifically on justify and extend, the relocation story is wrong. And to settle the scanner question: encode with and without an assistant, same people, test a week later. If the assisted trials show the same subsequent-memory signal and the same recall, I’m wrong about the loop. I don’t think I am, and I intend to run it on myself.

Naur was right. The theory is the product, you can’t get it back from the artifact, and a program whose theory-holders leave is dead however well it runs. What he couldn’t have seen is a world where the artifact arrives first and the theory never comes — the loop that builds understanding skipped by design, for everyone, on every program, and the programs born dead. The only reasonable way I’ve found to live in it is to stop pretending the theory lives in the code and put it somewhere small enough to hold, because I can’t hold it from raw code myself.

*Thanks to Claude Fable 5.1, which wrote a compiler I’ll never read, for a couple of billion tokens.*

*End of the series. Back to [Part 1](/the-compiler-nobody-read-1/) · [Part 2](/the-compiler-nobody-read-2/).*
