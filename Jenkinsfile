// --- Funzione helper (presa dall’esercizio, leggermente adattata) ---
def buildAndPushTag(Map args) {
    def defaults = [
        registryUrl: 'https://index.docker.io/v1/',
        dockerfileDir: "./",
        dockerfileName: "Dockerfile",
        buildArgs: "",
        pushLatest: true
    ]
    args = defaults + args

    docker.withRegistry(args.registryUrl, args.registryCredentials) {
        def image = docker.build(args.image, "${args.dockerfileDir} -f ${args.dockerfileName} ${args.buildArgs}")
        image.push(args.buildTag)
        if (args.pushLatest) {
            image.push("latest")
            sh "docker rmi --force ${args.image}:latest"
        }
        sh "docker rmi --force ${args.image}:${args.buildTag}"
        return "${args.image}:${args.buildTag}"
    }
}

// --- Pipeline dichiarativa principale ---
pipeline {
    agent any

    environment {
        REGISTRY_URL = 'https://index.docker.io/v1/'
        REGISTRY_CREDENTIALS = 'dockerhub-creds'  // ID delle credenziali salvate in Jenkins
        DOCKER_IMAGE = 'your-dockerhub-username/flask-app-example'
        DOCKER_TAG = "v${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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

