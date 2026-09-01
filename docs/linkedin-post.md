# LinkedIn post — draft

I did something slightly masochistic with my latest project: I asked a different AI model to tear it apart.

Some context. I've been building **Signal Tracker** — a tool that watches a list of UK companies on the free Companies House register and gives an early, plain-English warning when one looks like it's heading for trouble. It's the sort of thing credit, procurement and account-management teams do by hand today, if they get to it at all. For me it's a portfolio project: take a real commercial problem, build something end to end that solves it, and — the part I care about most — measure honestly whether it works.

So instead of polishing the demo, I wrote a detailed brief and asked an independent model to review the whole thing as a sceptical credit-risk expert. No encouragement. Just: *where is this weak?*

It found real things.

→ My dashboard ranked companies by their registered status but quietly ignored the filing-level signals underneath — so a freshly-detected serious event could sit on a company still showing green.

→ Failed API calls were being treated as "no news" — which, for a risk tool, means a company can look healthiest exactly when you can't actually see it.

→ And my headline "accuracy" number was really a regression check wearing a performance claim's clothes.

None of that was fun to read. All of it was right.

So I fixed them, one commit at a time — and the fixes, not the original build, are the part I'm now proudest of. Serious filings drive the headline. Missing data reads as "Unknown," never "fine." The evaluation runs from committed fixtures anyone can reproduce, with the look-ahead leak closed.

The wider lesson I'm taking into AI-enablement work: the highest-value way to use these models often isn't to *generate* — it's to *critique*. An honest adversarial review is cheap, fast, and worth more than another feature.

Happy to share the write-up if it's useful to anyone building in this space.
