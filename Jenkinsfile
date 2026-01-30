pipeline {
    agent any
    
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
        stage('Kube Debug') {
            steps {
                sh '''
                set -e
                which kubectl
                kubectl version --client=true
                echo "KUBECONFIG=$KUBECONFIG"
                kubectl config current-context || true
                kubectl config view --minify || true
                kubectl cluster-info || true
                kubectl get ns || true
                '''
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