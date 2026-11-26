# Requirements of r-api-design

The rows that the skill `r-api-design` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-10"></a>R-10 | API shape questions | in force | `r-api-design` makes `r-plan` ask what a route or an export is, and makes `r-review` check that the change matches the answers. The reason is that the contract and the handler change together, and a caller relies only on what the answers named. The route catalogue stays in the product, as [R-52](collection.md#r-52) says. This applies to both, when the skill is installed, and `r-api-design` owns the questions. |
