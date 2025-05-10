pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/HasanKhadd0ur/SAS.ScapingAgent.git', branch: 'main'
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python -m venv $VENV_DIR'
                bat '. $VENV_DIR/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '. $VENV_DIR/bin/activate && pytest tests/'
            }
        }
    }

    post {
        always {
            echo done
        }
    }
}
