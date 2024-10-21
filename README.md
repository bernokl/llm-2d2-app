## Simple web-app to convert gpt-prompt in into d2 diagrams
 - You will need https://platform.openai.com/ account with billing set up to create api_key
 - You can put limit or disable auto billing, ie it only uses available credits
 - Without payment setup I could not get responses.
## dir structure
 - app.py
 - requirements.txt
 - templates/
     - index.html
 - static/
     - (will contain the rendered diagram)
## Commands to run:
 - Create secret:
     kubectl create secret generic openai-api-key --from-literal=OPENAI_API_KEY=[your key here]
 - Docker build
     docker build -t [dockerRegistry]/diagrammer:latest .
 - Docker push
     docker push [dockerRegistry]/diagrammer:latest
 - Kubectl apply
     kubectl apply -f k8s-deployment.yaml -n ops-preview-1
 - Get the service name
     kubectl get service diagrammer-service

