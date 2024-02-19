# request-data
App to echo out HTTP request origin and headers.

App is running on HTTP at: http://echo.martinkaburu.me

ArgoCD Server: http://a33293180ce824994b0af573371a5ce9-1463041853.eu-central-1.elb.amazonaws.com

Github Repo: https://github.com/MartinKaburu/request-data

# Installation
### ArgoCD Installation
```Bash
helm repo add argo https://argoproj.github.io/argo-helm

helm install argocd argo/argo-cd --namespace argocd --create-namespace \
  --set server.service.type=LoadBalancer 
```


### ArgoCD Project & App Installation
```Bash
argocd proj create mkapps-req-data --src https://github.com/martinkaburu/request-data.git --dest https://kubernetes.default.svc,namespace=default
argocd repo add https://github.com/martinkaburu/request-data --project default
argocd app create request-data \
  --repo https://github.com/martinkaburu/request-data.git\
  --path helm/ \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace req-data \
  --sync-policy automated \
  --auto-prune \
  --revision HEAD \
  --helm-set image.repository=martinkaburu/request-data
  --project default
```


### Improvements
Given some more time I would have proceeded to:
1. Set up terraform configuration for the cluster, node groups and network
2. Set up an SSL certificate and configure cert-manager to auto update it
3. Add a github to ArgoCD webhook for on-time Syncs
4. Set up ArgoCD App for Apps gitops workflow for more granular control
5. Set up argocd notification webhook to slack
