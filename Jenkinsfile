pipeline {
    agent any
    
    environment {
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        IMAGE_REPO = "jeffreyzammit/netdash"
    }

    stages {
        stage('Build & Test') {
            steps {
                script {
                    docker.withRegistry('', 'docker-hub-creds') {
                        // 1. Build the image
                        def app = docker.build("${IMAGE_REPO}:${IMAGE_TAG}")
                        
                        // 2. RUN THE TEST INSIDE THE CONTAINER
                        // This spins up the container we just built and runs the python test command
                        sh "docker run --rm ${IMAGE_REPO}:${IMAGE_TAG} python -m unittest test_app.py"
                        
                        // 3. If the step above didn't fail, we proceed to push
                        app.push()
                        app.push("latest")
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'microk8s', variable: 'KUBECONFIG')]) {
                sh """#!/bin/bash
                    set -e
                    kubectl set image deployment/netdash netdash=jeffreyzammit/netdash:${IMAGE_TAG}
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