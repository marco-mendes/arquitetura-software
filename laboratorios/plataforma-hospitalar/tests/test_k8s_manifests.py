from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
K8S = ROOT / "infra" / "k8s"
KIND = ROOT / "infra" / "kind" / "cluster.yaml"


def load(name):
    return yaml.safe_load((K8S / name).read_text(encoding="utf-8"))


def test_kubernetes_manifests_define_a_safe_hospital_api_rollout():
    namespace = load("namespace.yaml")
    deployment = load("deployment.yaml")
    service = load("service.yaml")
    configmap = load("configmap.yaml")
    hpa = load("hpa.yaml")

    assert namespace == {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {"name": "hospital", "labels": {"app": "hospital-api"}},
    }
    assert deployment["apiVersion"] == "apps/v1"
    assert deployment["kind"] == "Deployment"
    assert deployment["metadata"]["namespace"] == "hospital"
    assert deployment["metadata"]["labels"]["app"] == "hospital-api"
    assert deployment["spec"]["replicas"] == 2
    assert deployment["spec"]["strategy"]["type"] == "RollingUpdate"
    assert deployment["spec"]["selector"]["matchLabels"] == {"app": "hospital-api"}
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    assert container["name"] == "hospital-api"
    assert container["ports"] == [{"containerPort": 8000, "name": "http"}]
    assert container["resources"]["requests"] == {"cpu": "100m", "memory": "128Mi"}
    assert container["resources"]["limits"] == {"cpu": "250m", "memory": "256Mi"}
    assert container["readinessProbe"]["httpGet"]["path"] == "/health/ready"
    assert container["livenessProbe"]["httpGet"]["path"] == "/health/live"
    assert container["readinessProbe"] != container["livenessProbe"]
    assert service["spec"]["selector"] == {"app": "hospital-api"}
    assert service["spec"]["ports"] == [
        {"name": "http", "port": 8000, "targetPort": "http", "nodePort": 30080}
    ]
    assert configmap["metadata"]["namespace"] == "hospital"
    assert hpa["apiVersion"] == "autoscaling/v2"
    assert hpa["spec"]["scaleTargetRef"] == {"apiVersion": "apps/v1", "kind": "Deployment", "name": "hospital-api"}
    assert hpa["spec"]["minReplicas"] == 2
    assert hpa["spec"]["maxReplicas"] == 5


def test_kind_cluster_maps_only_the_local_lab_port():
    config = yaml.safe_load(KIND.read_text(encoding="utf-8"))
    assert config["kind"] == "Cluster"
    assert config["nodes"][0]["role"] == "control-plane"
    assert config["nodes"][0]["extraPortMappings"] == [
        {"containerPort": 30080, "hostPort": 18080, "listenAddress": "127.0.0.1", "protocol": "TCP"}
    ]


def test_deployment_runs_the_health_checked_api():
    deployment = load("deployment.yaml")
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    assert container["command"] == [
        "python", "-m", "uvicorn", "hospital.api.main:app", "--host", "0.0.0.0", "--port", "8000"
    ]
