pipeline {
    agent any

    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
        REGISTRY_URL = 'https://index.docker.io/v1/'
        REGISTRY_CREDENTIALS = 'dockerhub-creds'
        DOCKER_IMAGE = 'andreademarco02/flask-app-example'
        DOCKER_TAG = "v${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Test') {
            steps {
                sh 'docker info'
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry(REGISTRY_URL, REGISTRY_CREDENTIALS) {
                        def app = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}", "-f Dockerfile .")
                        app.push()
                        app.push("latest")
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Docker image ${DOCKER_IMAGE}:${DOCKER_TAG} built and pushed successfully!"
        }
        failure {
            echo "❌ Build failed."
        }
    }
}

