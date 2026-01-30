pipline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the image and tag it with the Jenkins Build ID
                    docker.build("netdash:${env.BUILD_ID}")
                }
        }
    }
}