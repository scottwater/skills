# Source control and code review

## Evidence

- commit messages, dates, authors, and diffs;
- review descriptions, comments, and linked issues;
- inline comments, decision records, tests, changelogs, and release notes;
- co-changes and earlier versions of the same symbol or literal.

## Search

Start from the code anchor and inspect:

```bash
git log --follow --oneline -- <file>
git log -S '<literal>' -- <file>
git log -G '<pattern>' -- <file>
git blame -L <start>,<end> <file>
git show <commit>
```

Read substantive changes and their review discussion through the available forge interface. Follow rename history, linked change IDs, tickets, and nearby tests or comments. Search for previous names and copied versions of the pattern.

## Strong evidence

A review or commit explicitly states the problem, constraint, rejected alternative, or incident. A nearby comment can provide direct evidence when it records intent rather than restating mechanics. Tests can support an edge-case inference but rarely establish motivation alone.

## Pitfalls

- squash merges can hide intermediate reasoning;
- terse messages may misdescribe a behavioral change;
- copied patterns may inherit an earlier rationale;
- automated changes usually provide weak intent evidence;
- current code cannot prove why it was written.

## Return

Quote decisive text with commit, review, or `file:line`, author, and date. Record history searches that ended without rationale and any forge discussion that was inaccessible.

**Complete when:** every commit identified by blame, literal history, or rename history in the target window has been classified as relevant, irrelevant, or inaccessible.
