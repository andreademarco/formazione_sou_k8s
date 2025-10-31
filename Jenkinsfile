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
                    buildAndPushTag(
                        registryUrl: REGISTRY_URL,
                        registryCredentials: REGISTRY_CREDENTIALS,
                        image: DOCKER_IMAGE,
                        buildTag: DOCKER_TAG,
                        dockerfileDir: './',
                        dockerfileName: 'Dockerfile',
                        pushLatest: true
                    )
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

