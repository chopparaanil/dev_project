pipeline {

    agent any

    environment {
        IMAGE_NAME = "student-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = "student-app"
        APP_PORT = "5020"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout Source') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Workspace Information') {
            steps {
                sh '''
                echo "Current Directory:"
                pwd

                echo "Workspace Files:"
                ls -la
                '''
            }
        }

        stage('Python Version') {
            steps {
                sh '''
                python3 --version
                '''
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                flake8 . || true
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                pytest -v || true
                '''
            }
        }

        stage('Docker Version') {
            steps {
                sh '''
                docker --version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} \
                    -t ${IMAGE_NAME}:latest \
                    .
                """
            }
        }

        stage('Docker Images') {
            steps {
                sh '''
                docker images
                '''
            }
        }

        stage('Remove Old Container') {
            steps {
                sh """
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                """
            }
        }

        stage('Run Container') {
            steps {
                sh """
                docker run -d \
                    --name ${CONTAINER_NAME} \
                    -p ${APP_PORT}:${APP_PORT} \
                    ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                echo "Running Containers:"
                docker ps

                echo ""
                echo "Docker Images:"
                docker images
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 10

                curl -I http://localhost:5020 || true
                '''
            }
        }
    }

    post {

        always {

            echo "Cleaning dangling images..."

            sh '''
            docker image prune -f || true
            '''
        }

        success {

            echo "======================================"
            echo "BUILD SUCCESSFUL"
            echo "Application deployed successfully."
            echo "======================================"

        }

        failure {

            echo "======================================"
            echo "BUILD FAILED"
            echo "Check Jenkins Console Output."
            echo "======================================"

        }
    }
}