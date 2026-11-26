# Requirements of r-migrate-docs

The rows that the skill `r-migrate-docs` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-5"></a>R-5 | Only r-migrate-docs reads the old board | in force | `r-migrate-docs` is the only skill that reads the content of the old board. Other skills only test whether its paths exist, so that one skill owns the move. This applies to both. `r-migrate-docs` owns the read, and `r-github-pipeline` owns the delivery text. |
| <a id="r-29"></a>R-29 | r-migrate-docs scope | in force | `r-migrate-docs` runs when a path of the old board of [R-21](project-setup.md#r-21) exists, when `docs/ROADMAP.md` has the old line form, or when `AGENTS.md` exists. It moves each fact that is still true once. It deletes the old files in the same change, so the new board does not sit beside the old one. [R-53](record.md#r-53) says where a fact goes. This applies to a product repository that still has the old board, and `r-migrate-docs` owns the move. |
