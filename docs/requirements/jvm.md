# Requirements of jvm

The rows that the skill `r-jvm` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-39"></a>R-39 | JVM languages | in force | `r-jvm` applies the JVM rules when it is installed and the files are Java, Groovy, Grails, or Gradle. The Make targets run Gradle, and the workflow never calls Gradle itself. The references of the skill hold the rules of each language. This applies to a product repository that installs `r-jvm`, and `r-jvm` owns these rules. |
| <a id="r-116"></a>R-116 | Gradle in Podman reaches Podman | in force | Gradle runs in a container, so the host needs no Java toolchain. A Gradle task that starts containers reaches the Podman socket of the host through `$(GRADLE_PODMAN)`. This applies to a product repository that installs `r-jvm`, and `r-jvm` owns this rule. |
