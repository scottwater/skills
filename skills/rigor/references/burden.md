# Reduce the burden

- **Subtract first.** Within the evidenced problem boundary, remove dead paths, obsolete adapters, redundant validation, and unsupported scope that would otherwise survive beside the replacement.
- **Minimize reader load.** Reduce both the layers a maintainer must trace and the hidden mutable state they must remember. A wrapper or abstraction earns its place by owning a real invariant, hiding meaningful complexity, or serving genuine callers.

**Complete when:** the resulting design carries fewer concepts, layers, or hidden state without moving the same burden behind a larger interface.
