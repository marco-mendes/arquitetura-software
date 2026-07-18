from pathlib import Path
import re
import unittest

from tests.course_assertions import assert_module_contract, navigation_section_paths


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-6-nuvem"


class ModuleSixTest(unittest.TestCase):
    def test_workshop_explains_complete_runtime_before_executable_commands(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
        presentation = (
            "## Leia antes de executar comandos",
            "O `Dockerfile` descreve",
            "O arquivo `infra/kind/cluster.yaml` instrui",
            "Os manifestos expressam o estado inicial",
            "As probes deixam a condição observável",
        )
        commands = (
            "kubectl apply",
            "docker build -t hospital-api:1.0.0 .",
            "docker image inspect hospital-api:1.0.0",
            "kind get clusters",
            "kind create cluster --name hospital-local",
            "kind load docker-image hospital-api:1.0.0 --name hospital-local",
            "kubectl config current-context",
            "curl --fail --silent http://127.0.0.1:18080/health/ready",
            "python -m pytest tests/test_k8s_manifests.py -q",
        )

        presentation_positions = [workshop.index(item) for item in presentation]
        self.assertEqual(presentation_positions, sorted(presentation_positions))
        self.assertLess(
            max(presentation_positions),
            min(workshop.index(command) for command in commands),
        )

    def test_unit_six_distinguishes_service_models_and_runtime_mechanisms(self):
        text = (
            (MODULE / "conceitos.md").read_text(encoding="utf-8")
            + (MODULE / "padroes-e-decisoes.md").read_text(encoding="utf-8")
        )
        for term in (
            "IaaS",
            "PaaS",
            "SaaS",
            "on-premise",
            "contêiner",
            "orquestração",
            "readiness",
            "liveness",
        ):
            self.assertIn(term, text)

    def test_content_contract(self):
        assert_module_contract(
            self,
            "modulo-6-nuvem",
            (
                "IaaS",
                "PaaS",
                "SaaS",
                "região",
                "zona",
                "elasticidade",
                "resiliência",
                "contêiner",
                "orquestração",
                "readiness",
                "liveness",
                "rollback",
                "Docker",
                "kind",
                "Kubernetes",
            ),
        )

    def test_module_has_eight_pages_navigation_and_accessible_diagrams(self):
        self.assertEqual(
            sorted(path.name for path in MODULE.glob("*.md")),
            sorted(
                (
                    "index.md", "conceitos.md", "padroes-e-decisoes.md",
                    "exemplo-arquitetural.md", "estudo-de-caso.md",
                    "oficina-de-ferramentas.md", "exercicios.md",
                    "sintese-e-referencias.md",
                )
            ),
        )
        section = navigation_section_paths("Módulo 6 — Nuvem")
        self.assertEqual(
            {f"modulo-6-nuvem/{page}" for page in sorted(path.name for path in MODULE.glob("*.md"))},
            set(section),
        )
        corpus = "\n".join(path.read_text(encoding="utf-8") for path in MODULE.glob("*.md"))
        words = re.findall(r"\b[^\W_]+(?:[-'][^\W_]+)*\b", corpus)
        self.assertGreaterEqual(len(words), 5000)
        self.assertLessEqual(len(words), 8500)
        self.assertGreaterEqual(corpus.count("```mermaid"), 3)
        # Diagramas Mermaid e infográficos gerados possuem leitura textual.
        # Os infográficos acrescentam equivalências além das exigidas pelos Mermaid.
        self.assertGreaterEqual(
            corpus.count("**Leitura textual da figura:**"),
            corpus.count("```mermaid"),
        )

    def test_workshop_is_cross_platform_and_proves_safe_rollback(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
        for fragment in (
            "kind create cluster --name hospital-local --config infra/kind/cluster.yaml",
            "kind load docker-image hospital-api:1.0.0 --name hospital-local",
            "kubectl rollout status deployment/hospital-api -n hospital",
            "kubectl rollout undo deployment/hospital-api -n hospital",
            "kind delete cluster --name hospital-local",
            "/health/ready", "/health/live", "kubectl apply --dry-run=client",
            "imagem propositalmente ausente", "Docker", "Kubernetes",
        ):
            self.assertIn(fragment, workshop)

    def test_workshop_applies_namespace_before_namespaced_resources(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
        self.assertNotIn("kubectl apply -f infra/k8s\n", workshop)
        namespace_apply = "kubectl apply -f infra/k8s/namespace.yaml"
        namespaced_apply = (
            "kubectl apply -f infra/k8s/configmap.yaml "
            "-f infra/k8s/deployment.yaml -f infra/k8s/service.yaml "
            "-f infra/k8s/hpa.yaml"
        )
        self.assertEqual(workshop.count(namespace_apply), 2)
        self.assertEqual(workshop.count(namespaced_apply), 2)
        self.assertLess(
            workshop.index(namespace_apply), workshop.index(namespaced_apply)
        )


if __name__ == "__main__":
    unittest.main()
