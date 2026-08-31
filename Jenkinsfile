pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out by Jenkins SCM'
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('backend') {
                    sh 'python3 -m pip install --break-system-packages -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('backend') {
                    sh 'python3 -m pytest -v'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('backend') {
                    sh 'docker build -t taskflow-api .'
                }
            }
        }
    }
}
