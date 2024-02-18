# request-data
App to echo out HTTP request origin and headers



# Helm Installation
```Bash
helm repo add argo https://argoproj.github.io/argo-helm

helm install argocd argo/argo-cd --namespace argocd --create-namespace \
  --set server.service.type=LoadBalancer \
  --set 'server.env[0].name=ARGOCD_USERNAME' \
  --set 'server.env[0].value=admin' \
  --set 'server.env[1].name=ARGOCD_PASSWORD' \
  --set 'server.env[1].value=admin'
```


# ArgoCD Project Installation
argocd proj create mkapps-req-data --src https://github.com/martinkaburu/request-data.git --dest https://kubernetes.default.svc,namespace=default
argocd repo add https://github.com/martinkaburu/request-data --project mkapps-req-data
argocd app create request-data \
  --repo https://github.com/martinkaburu/request-data.git\
  --path helm/ \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace req-data \
  --sync-policy automated \
  --auto-prune \
  --revision main \
  --helm-set image.repository=martinkaburu/request-data
  --helm-set image.tag=latest
