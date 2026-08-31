pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out by Jenkins SCM'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                dir('backend') {
                    sh 'python3 -m venv jenkins_venv'
                    sh 'jenkins_venv/bin/pip install --upgrade pip'
                    sh 'jenkins_venv/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('backend') {
                    sh 'jenkins_venv/bin/pytest -v'
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