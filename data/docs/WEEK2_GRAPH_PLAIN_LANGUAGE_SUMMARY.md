# Week 2 Graph Summary (Plain Language)

## What we built in Week 2
In Week 2, we built our first **attack-target graph**.  
The basic idea was simple: each line (edge) shows a sponsor attacking a person or group mentioned in ads.

## Why we built it
We wanted to move beyond just counting ads or money.  
This graph helps answer: **who is attacking whom most often?**

## What was different after Week 2
Our Week 2 version was intentionally broad, so it captured a lot of possible targets.  
That gave us good coverage, but it also included noise (generic terms, ambiguous names, weak connections).

So after Week 2, we made a stricter Week 3 version:
- removed low-quality or generic entities
- tightened target rules (higher confidence only)
- kept only stronger edges

## Why we made those choices
We chose stricter rules because we wanted the graph to be more trustworthy.  
It is better to keep fewer edges that are more believable than many edges that are questionable.

## Why the newer graph is better
The newer graph is cleaner and easier to interpret:
- fewer misleading “targets”
- stronger sponsor-target relationships
- clearer patterns for analysis and visualization

## What we can still improve
There is still important work left:
- manual validation of a sample (to measure accuracy)
- better handling of ambiguous names
- richer time-based views (how attacks change over weeks/months)
- stronger spending analysis by edge and by target
- export-ready figures for write-up/final presentation
