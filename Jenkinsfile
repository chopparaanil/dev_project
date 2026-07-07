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

        stage('Print Workspace') {
            steps {
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Docker Version') {
            steps {
                sh 'docker --version'
                sh 'docker compose version'
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                docker build \
                -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Images') {
            steps {
                sh 'docker images'
            }
        }

        stage('Stop Existing Containers') {
            steps {
                sh '''
                docker compose down || true
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker compose up -d --build
                '''
            }
        }

        stage('Verify Containers') {
            steps {
                sh 'docker ps'
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 15
                curl -I http://localhost:8080
                '''
            }
        }
    }

    post {

        success {

            echo '==================================='
            echo 'Build Successful'
            echo 'Application Deployed Successfully'
            echo '==================================='

        }

        failure {

            echo '==================================='
            echo 'Build Failed'
            echo 'Check Console Output'
            echo '==================================='

        }

        always {

            sh 'docker images'

        }

    }

}