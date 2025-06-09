#!/bin/bash

set -e

echo "🔧 Setting up monitoring stack..."

# Add Helm repos
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Create monitoring namespace
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Install Prometheus
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.retention=30d

# Install Grafana (if not included in prometheus stack)
# helm upgrade --install grafana grafana/grafana \
#   --namespace monitoring \
#   --set persistence.enabled=true \
#   --set persistence.size=10Gi

echo "📊 Monitoring stack installed successfully!"
echo "🔍 Access Grafana with:"
echo "kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80"
echo "Default credentials: admin/prom-operator"
