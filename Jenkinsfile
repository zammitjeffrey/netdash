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
    }
    post {
        always {
            cleanWs()
        }
    }
}