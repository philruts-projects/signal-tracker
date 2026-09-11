# LinkedIn post — draft

I built a thing, and I'd genuinely like you to try and break it.

It's called Signal Tracker. It watches a list of UK companies on the free Companies House register and warns you, in plain English, when one of them looks like it might be heading for trouble. The people who'd use it, in credit or procurement or key-account teams, do this by hand today when they get to it at all, even though the warning signs usually sit in the public filings for months before anyone acts. Nobody's watching them, so I built something that does.

Two ideas do the heavy lifting. First, the rules decide and the AI only explains: deterministic logic sets the risk verdict so it stays auditable, and the Claude API is kept to writing the plain-English briefing, which is the thing language models are actually good at. Second, it treats distress as a pattern rather than a single event. One director leaving is noise; a finance chief walking out and then, a few weeks later, a cluster of new charges as the company scrambles for secured cash, that's a signal, and you only catch it by reading across the filings instead of one at a time.

The part I'm most pleased with isn't a feature. It's the evaluation. It scores the tool against companies that actually went under, Carillion and Greensill among them, and it writes down where it falls short instead of hiding it. At one point I handed the whole thing to a different AI model and told it to review my work as a sceptical expert. It found real weaknesses. Fixing those in the open turned out to be half the story.

It's early, and still narrow. I'm adding one data source at a time, because the interesting bit is what happens when you combine them: something that no single register tells you on its own.

Code's on GitHub: https://github.com/philruts-projects/signal-tracker

Have a poke around, run it, tell me where it's wrong, or take the idea and build your own. I'd like to hear from anyone working in credit, risk, data or AI.
