# Requirements of node

The rows that the skill `r-node` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-36"></a>R-36 | Node and TypeScript | in force | `r-node` applies the Node rules when it is installed and the files are JavaScript or TypeScript. The package manager runs only through Make targets, never in a workflow step. This applies to a product repository that installs `r-node`, and `r-node` owns these rules. |
