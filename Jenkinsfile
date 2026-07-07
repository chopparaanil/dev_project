pipeline {

    agent any

    environment {
        IMAGE_NAME = "student-app"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Version') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Remove Old Container') {
            steps {
                sh '''
                docker stop student-app || true
                docker rm student-app || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                    --name student-app \
                    -p 5020:5020 \
                    student-app:latest
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                docker ps
                '''
            }
        }

    }

    post {

        success {
            echo 'Deployment Successful'
        }

        failure {
            echo 'Deployment Failed'
        }
    }
}