pipeline {
  agent any

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))

  }

  environment {
    PROJECT_DIR = ''
    REPORT_FILE = 'report.html'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Detect project directory') {
      steps {
        script {
          if (fileExists('requirements.txt')) {
            env.PROJECT_DIR = '.'
          } else if (fileExists('api_testing_framework/requirements.txt')) {
            env.PROJECT_DIR = 'api_testing_framework'
          } else {
            error("Could not find requirements.txt at repo root or in api_testing_framework/")
          }
          echo "Using PROJECT_DIR=${env.PROJECT_DIR}"
        }
      }
    }

    stage('Setup Python venv') {
      steps {
        script {
          if (isUnix()) {
            dir(env.PROJECT_DIR) {
              sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
              '''
            }
          } else {
            // Windows
            dir(env.PROJECT_DIR) {
              bat '''
                py -3 -m venv venv
                call venv\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
              '''
            }
          }
        }
      }
    }

    stage('Run tests') {
      steps {
        script {
          if (isUnix()) {
            dir(env.PROJECT_DIR) {
              sh '''
                . venv/bin/activate
                pytest -q --maxfail=1 --html=report.html --self-contained-html
              '''
            }
          } else {
            dir(env.PROJECT_DIR) {
              bat '''
                call venv\\Scripts\\activate
                pytest -q --maxfail=1 --html=report.html --self-contained-html
              '''
            }
          }
        }
      }
    }
  }

  post {
    always {
      script {
        publishHTML(target: [
          reportDir: env.PROJECT_DIR,
          reportFiles: env.REPORT_FILE,
          reportName: 'PyTest Report'
        ])
        archiveArtifacts artifacts: "${env.PROJECT_DIR}/${env.REPORT_FILE}, ${env.PROJECT_DIR}/logs/**", fingerprint: true
      }
    }
  }
}
