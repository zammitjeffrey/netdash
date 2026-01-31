pipeline {
    agent any
    
    
    environment {
        // Use one build number variable consistently for image tagging
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        IMAGE_REPO = "jeffreyzammit/netdash"
    }

    stages {
        stage('Build & Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'docker-hub-creds') {
                        // 1. Build the image
                        // We name it 'username/repo:build-number'
                        def app = docker.build("jeffreyzammit/netdash:${env.BUILD_ID}")
                        
                        // 2. Push the image with the specific build number
                        app.push()
                        
                        // 3. Also push it as 'latest' so it's easy to find
                        app.push("latest")
                    }
                }
            }
        }
        
        stage('Kube Debug (before deploy)') {
            steps {
                // Bind the *remote* kubeconfig so kubectl has a context
                withCredentials([file(credentialsId: 'microk8s', variable: 'KUBECONFIG')]) {
                sh '''
                    set -euxo pipefail
                    which kubectl
                    kubectl version --client=true
                    echo "Using KUBECONFIG=${KUBECONFIG}"
                    echo "== contexts =="
                    kubectl config get-contexts || true
                    echo "== current context =="
                    kubectl config current-context || true
                    echo "== cluster-info =="
                    kubectl cluster-info || true
                    echo "== namespaces =="
                    kubectl get ns || true
                '''
                }
            }
            }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                sh """
                    set -e
                    kubectl get ns
                    kubectl set image deployment/netdash-deployment netdash-container=jeffreyzammit/netdash:${env.BUILD_NUMBER}
                    kubectl rollout status deployment/netdash-deployment --timeout=180s
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