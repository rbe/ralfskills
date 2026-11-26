# Requirements of performance

The rows that the skill `r-performance` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-103"></a>R-103 | Performance questions | in force | `r-performance` applies when the change reads, parses, imports, or aggregates data, or claims a gain in speed, size, or quality. A claim about speed, size, or model output quality needs a baseline from the same session. `r-plan` asks three questions. What is the largest input that the change must handle? How many times does the change read each file or row? Where does the data live, and where does the aggregation run? `r-review` checks four things. Each file or row is read once for each request, not once for each loop step. An import or a parse runs in one pass. Aggregation runs where the data is, not in a client that must first fetch all of it. A claim that a change is faster or slower states a measured baseline from before the change and a measurement after it, from the same machine and the same session. This applies to both, when the skill is installed. `r-performance` owns the questions. |
