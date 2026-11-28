# Requirements of jvm

The rows that the skill `r-jvm` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-39"></a>R-39 | JVM languages | in force | `r-jvm` applies the JVM rules when it is installed and the files are Java, Groovy, Grails, or Gradle. The Make targets run Gradle, and the workflow never calls Gradle itself. The references of the skill hold the rules of each language. This applies to a product repository that installs `r-jvm`, and `r-jvm` owns these rules. |
| <a id="r-116"></a>R-116 | Gradle in Podman reaches Podman | in force | Gradle runs in a container, so the host needs no Java toolchain. A Gradle task that starts containers reaches the Podman socket of the host through `$(GRADLE_PODMAN)`. This applies to a product repository that installs `r-jvm`, and `r-jvm` owns this rule. |
| <a id="r-128"></a>R-128 | Maven mirror on request | in force | If Maven Central answers HTTP 429, the owner sets `MAVEN_MIRROR` to another Maven Central URL, and Gradle reads from it. The build files of the project stay as they are. If the settings file declares no plugin repository, plugin dependencies also come from the mirror. An empty `MAVEN_MIRROR` keeps Maven Central, so a run without it behaves as before. This applies to a product repository that installs `r-jvm`, and `r-jvm` owns this rule. |
| <a id="r-156"></a>R-156 | JaCoCo paths from the repository root | in force | `jacoco_repo_paths.py` of `r-project-report` writes a copy of a JaCoCo XML report in which each source file has its path from the repository root. diff-cover reads that copy. The reason is that diff-cover joins one source root with the package name, which misses the files of a second module or a Groovy tree. odisee26 kept its own copy of this script. |
| <a id="r-157"></a>R-157 | JaCoCo coverage summary | in force | `jacoco_summary.py` of `r-project-report` writes `build/summaries/coverage.md` with the line, instruction, branch, and method counters of `jacocoTestReport.xml`. Without a report it deletes the summary. The reason is that the report job reads `build/summaries/`, and erechnung kept its own copy of this script. |
