# Requirements of privacy

The rows that the skill `r-privacy` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-32"></a>R-32 | Privacy questions | in force | `r-privacy` applies when the change stores, logs, exports, or shows personal data. `r-plan` asks what personal data is handled and who asked for the export. `r-review` checks that logs and errors hold none and that an export is one the user asked for. It checks that real data is not in the tree. This applies to both, when the skill is installed, and `r-privacy` owns the questions. |
| <a id="r-136"></a>R-136 | Outside text stays in the log | in force | `r-privacy` makes `r-review` check that text from outside the code goes to the log. A parser, a provider, and the network are outside the code. The error that the user sees is text that the code wrote. The reason is that outside text can quote user data, a URL, or a key. This applies to a product repository that installs `r-privacy`, and `r-privacy` owns this rule. |
| <a id="r-137"></a>R-137 | Refused import row is named by line | in force | `r-privacy` makes `r-review` check that a message about a refused row of an import names the row by its line number. The message never names the row by its content. The reason is that the row can hold personal data. This applies to a product repository that installs `r-privacy`, and `r-privacy` owns this rule. |
