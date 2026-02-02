pipeline {
    agent any
    
    environment {
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        IMAGE_REPO = "jeffreyzammit/netdash"
    }

    stages {
        stage('Build & Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'docker-hub-creds') {
                        def app = docker.build("${IMAGE_REPO}:${IMAGE_TAG}")
                        app.push()
                        app.push("latest")
                    }
                }
            }
        }
        
        stage('Kube Debug (before deploy)') {
            steps {
                withCredentials([file(credentialsId: 'microk8s', variable: 'KUBECONFIG')]) {
                // We add the shebang line to force using BASH
                sh """#!/bin/bash
                    set -euxo pipefail
                    chmod 600 \${KUBECONFIG}
                    kubectl version --client=true
                    echo "Testing connection to MicroK8s..."
                    kubectl get nodes
                """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'microk8s', variable: 'KUBECONFIG')]) {
                sh """#!/bin/bash
                    set -e
                    # chmod 600 \${KUBECONFIG}
                    kubectl set image deployment/netdash netdash=jeffreyzammit/netdash:${IMAGE_TAG}
                    
                    # 2. Wait for the rollout to finish
                    kubectl rollout status deployment/netdash --timeout=180s
                """
                }
            }
        }
    }
 
    post {
        always {
            cleanWs()
        }
    }
}