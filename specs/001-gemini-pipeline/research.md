# Research for GEMINI Code Analysis and PRD Generator

This document outlines the research tasks to resolve ambiguities and make key technical decisions for the project.

## 1. Identity & Uniqueness Rules for Artifacts

**Task**: Define a strict, non-ambiguous format for the stable identifier of a code artifact.

**Decision**: The stable identifier for a code artifact will be a composite key of the format: `{project_name}:{file_path_from_root}:{symbol_name}`.
- `{project_name}`: The name of the project as provided by the user.
- `{file_path_from_root}`: The relative path of the file from the `JAVA_SOURCE_DIR`.
- `{symbol_name}`: The name of the specific artifact within the file (e.g., class name, method name, JSP form ID). For files that are themselves the artifact, this can be the file name.

**Rationale**: This format is unambiguous, ensures uniqueness across projects and within a project, and is easy to construct and parse. It removes the ambiguity of the "e.g." in the original spec.

**Alternatives considered**: Using UUIDs was considered, but they are not human-readable and make debugging harder. Using only file path and symbol name is not sufficient as it could lead to collisions if the same code is analyzed under different project names.

## 2. Performance Goals

**Task**: Define a concrete performance target for the PRD generation pipeline.

**Decision**: The pipeline should be able to process a 1 million line of code repository and generate a PRD in under 30 minutes on a standard developer machine (e.g., MacBook Pro with M1 chip, 16GB RAM).

**Rationale**: "Hours or less" is too vague. A concrete target of 30 minutes for a 1M LoC repository provides a measurable goal for performance testing and optimization. The clarification from the user on scalability to 10M LoC suggests that performance is a key concern.

**Alternatives considered**: A target of 1 hour was considered, but 30 minutes provides a better user experience and a more challenging engineering goal.

## 3. Compliance & Regulatory Constraints

**Task**: Research any potential compliance or regulatory constraints for a code analysis tool.

**Decision**: There are no specific compliance or regulatory constraints for a code analysis tool that runs on a local machine and does not transmit code to external services. The user's decision to "ignore secrets" simplifies this, but the tool's documentation should clearly state that it is the user's responsibility to ensure compliance with their own organization's policies, especially when handling sensitive codebases.

**Rationale**: The tool is essentially a sophisticated local search and text generation utility. As long as it doesn't store or transmit code, standard compliance frameworks like SOC2, GDPR, etc., are not directly applicable to the tool itself, but rather to how the user operates it.

**Alternatives considered**: Implementing features for data masking or anonymization was considered, but this was implicitly rejected by the user's choice to ignore secrets, and would add significant complexity.

## 4. Protocol/Versioning for Dependencies

**Task**: Define a strategy for handling versions of external dependencies like Weaviate and Ollama.

**Decision**: The project will target specific major versions of Weaviate and the Ollama API. These versions will be documented in the `quickstart.md` and checked for at runtime.
- **Weaviate**: The project will target the latest stable Weaviate version at the time of development (e.g., v1.23.x). The `docker-compose.yml` will be pinned to this version.
- **Ollama**: The project will assume the latest stable version of Ollama and its API. Since the Ollama API is not yet versioned, the project will need to be tested against new Ollama releases. The documentation will state the version of Ollama the tool was last tested with.

**Rationale**: Pinning versions ensures a stable and reproducible environment. Runtime checks for versions will provide clear error messages to the user if their environment is incompatible. This is better than letting the tool fail with cryptic errors.

**Alternatives considered**: Supporting multiple versions of dependencies would add significant testing and maintenance overhead. Not specifying versions at all would lead to a poor user experience and debugging challenges.
