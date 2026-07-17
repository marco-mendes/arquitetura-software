import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.12.2/+esm";
mermaid.initialize({ startOnLoad: false, securityLevel: "loose", theme: "neutral" });
document$.subscribe(() => mermaid.run({ querySelector: ".mermaid" }));
