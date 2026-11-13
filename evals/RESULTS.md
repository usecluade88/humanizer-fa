# Evaluation record / گزارش ارزیابی

Date: 2026-11-13 (Asia/Tehran). Candidate skill metadata: 2.0.0. Baseline: the local 1.0.0 skill frozen before editing. Model: the current session's inherited model configuration, without an explicit model override; exact model/effort telemetry was not captured and is not guessed here.

This is a small developer-authored language-task evaluation. It is not a public benchmark, a human-origin test, a detector score or evidence of universal superiority. Separate agents produced outputs from the same fixed requests; a separate model editor reviewed unlabeled A/B pairs with varied ordering. The reviewer did not receive the mapping to versions. This is model review, not a panel of human editors or a statistical study.

## Development round 1

18 cases. Both sets passed the explicit machine-checkable constraints. The blind editor preferred baseline on 5 cases, tied 13 and preferred the first candidate on none. No clear serious semantic error was reported, but the candidate used more impersonal phrasing in some support/marketing cases. Both versions used repetition in the exact-40-word case.

The result was treated as a failed quality improvement, not hidden. Candidate instructions were revised to emphasize direct ownership when the speaker is known, a useful opening, natural requests from the correct speaker, deeper paragraph reconstruction and avoiding duplicated time disclaimers. Examples used other domains. The 18 cases became a development set; a later result on them is not out-of-sample evidence.

## Development round 2 and fresh cases

22 pairs were executed: the 18 development cases plus four fresh cases in [holdout.json](holdout.json). The second blind reviewer preferred baseline on 4, candidate on 2, and tied 16. On the four fresh cases alone: 2 candidate preferences, 1 baseline preference and 1 tie. The candidate was not tuned to those four results before that run; they are now disclosed and should not be treated as hidden future tests.

Both output sets passed the explicit machine-checkable constraints across all 22 cases. The editor nevertheless identified two candidate semantic issues on development cases: inferring that an unspecified scented product was perfume, and changing an unknown response time into a time not yet determined. These are important examples of why string/count checks cannot prove fidelity. Baseline had no serious semantic failure reported in this pass. A separate style weakness was that one candidate support reply became generic rather than naming the known problem.

The candidate received a targeted fidelity patch distinguishing unknown state from non-occurrence and prohibiting unsupported product inference/cross-case context leakage. A targeted post-patch regression is recorded below. The whole 22-case comparison was not rerun after this final patch, so its preference counts are not claimed as final-patch benchmark results.

The two additional preset smoke outputs cover persuasive and literary voices. Their writer accidentally saw the scenario criteria before producing text; these are openly treated as unblinded demonstrations, not additional blind-comparison evidence. Both preserve the supplied facts in manual review.

## Post-patch regression

The post-patch run covers the two failing development requests and two fresh paraphrases of unknown-state/unspecified-product conditions. All four were actually rewritten by a new writer that had not seen the earlier outputs/reviews. Explicit fragment/count checks and maintainer semantic review found the targeted failures resolved: the product remains unspecified and unknown time is no longer rewritten as time not set. The 40-word case was counted after the final text. This targeted review was not blind and is not a new full-corpus comparison. [Requests](regressions.json), [outputs](artifacts/fidelity-regression-outputs.json) and [review](artifacts/fidelity-regression-review.json) are included.

## Interpretation

These runs do **not** establish blanket writing-quality superiority over 1.0.0. Version 2 adds an explicit tone/control contract, clearer task/role routing, public documentation and reproducible evaluation tooling. The comparison exposed real regressions, which were addressed rather than hidden. Broader multi-run testing and Persian-speaking human editorial review remain necessary before general quality claims.

Raw outputs, the blind reviewer decisions and the later-unsealed label maps are retained in [artifacts](artifacts/v1-outputs.json). The [baseline prompt text](artifacts/baseline-instructions.txt) and [snapshot notes](artifacts/snapshots.json) document the local comparison source. Example outputs in README/examples are separately labeled as illustrative.

## Long-form self-review: 2.0.1

Five new synthetic cases were written, frozen, rewritten and reviewed by the same writer: a detailed customer-support email, furniture-workshop website copy, a formal project report, a technical tutorial and a fictional first-person narrative. This was requested self-review, not another independent comparison. The full sources and finals appear in [long-form.md](long-form.md); [JSON artifacts](artifacts/long-form-self-review.json) retain first-pass outputs and the specific corrections.

Source/final whitespace word counts: support 277/228, website 288/255, formal 272/247, technical 275/236, narrative 262/232. All ten texts exceed 200 words. Protected URL/code fragments were checked for exact preservation. Unicode and punctuation checks were advisory, not automated proof of naturalness.

First-pass review found an unsupported payment-information explanation, an imprecise image/object construction, unnecessary inferred report commentary, a local polarity error involving confirmation receipt, and a new narrative event. These were corrected in the final texts. The prompt received two narrow clarifications: checking local negation/pronoun reference after restructuring and avoiding new narrative events or feelings during editing. The previous 22-pair language comparison was not rerun after this patch; no new blind-comparison claim is made.

## Tool checks and limitations

The checker only tests explicit fragments, raw JSON structure, unchanged text and whitespace word counts. It cannot detect all meaning changes. Apparent injection resistance cannot be concluded from a rewritten string alone; the bounded writers were allowed only local test read/write/count actions and no actual customer or filesystem operations requested by quoted data.

Executed tooling checks: package validation passed; 11 unit tests passed; the bundled skill-creator structural validator and separate YAML checks passed. No real website, customer conversation, model API integration, other agent host or GitHub publication is tested here.
