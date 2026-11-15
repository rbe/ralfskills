# Gradle

The Gradle wrapper is the Gradle the project runs. Versions live in the version catalog. `make build` and `make test` call the wrapper. A workflow step calls `make`, not the wrapper. `make format` runs google-java-format through Spotless (`spotlessCheck`). `make lint` runs Checkstyle (`checkstyleMain`). `make coverage` runs JaCoCo's XML through diff-cover.
