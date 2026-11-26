# Requirements of r-component-upgrade

The rows that the skills `r-component-upgrade`, `r-upgrade-node-components`, `r-upgrade-python-components`, `r-upgrade-java-components`, and `r-upgrade-go-components` own. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-104"></a>R-104 | Upgrade one component | in force | `r-component-upgrade` updates one component to a newer version in one slice, with the gates run before and after the change of the one pin. A pin names an exact version. If a gate fails, the pin returns to the old version and a roadmap row of the kind `defect` records it. This applies to a product repository that installs the skill. `r-component-upgrade` owns the procedure, and each `r-upgrade-<language>-components` skill owns where its language pins versions. |
