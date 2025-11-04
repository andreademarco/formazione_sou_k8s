pipeline {
    agent any

    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
        REGISTRY_URL = 'https://index.docker.io/v1/'
        REGISTRY_CREDENTIALS = 'dockerhub-creds'
        DOCKER_IMAGE = 'andreademarco02/flask-app-example'
        DOCKER_TAG = ''
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

        stage('Set Docker Tag') {
            steps {
                script {
                    // Ottieni il nome del branch o il tag
                    def gitBranch = sh(script: "git rev-parse --abbrev-ref HEAD", returnStdout: true).trim()
                    def gitTag = sh(script: "git describe --tags --exact-match 2>/dev/null || true", returnStdout: true).trim()
                    def gitCommit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()

                    echo "Git branch: ${gitBranch}"
                    echo "Git tag: ${gitTag}"
                    echo "Git commit: ${gitCommit}"

                    if (gitTag) {
                        env.DOCKER_TAG = gitTag
                    } else if (gitBranch == "main" || gitBranch == "origin/main" || gitBranch == "master") {
                        env.DOCKER_TAG = "latest"
                    } else if (gitBranch.contains("develop")) {
                        env.DOCKER_TAG = "develop-${gitCommit}"
                    } else {
                        env.DOCKER_TAG = "build-${gitCommit}"
                    }

                    echo "Docker tag selezionato: ${env.DOCKER_TAG}"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    withDockerRegistry([url: REGISTRY_URL, credentialsId: REGISTRY_CREDENTIALS]) {
                        sh """
                            echo "Building image ${DOCKER_IMAGE}:${DOCKER_TAG}"
                            docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -f Dockerfile .
                            docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Docker image ${DOCKER_IMAGE}:${DOCKER_TAG} built and pushed successfully!"
        }
        failure {
            echo " Build failed."
        }
    }
}

