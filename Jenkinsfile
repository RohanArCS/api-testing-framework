pipeline {
  agent any

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  environment {
    PROJECT_DIR = '.'            // default to repo root
    REPORT_FILE = 'report.html'
  }

  stages {
    stage('Detect project directory') {
      steps {
        script {
          // If the framework lives in a subfolder, switch to it
          if (fileExists('api_testing_framework/requirements.txt')) {
            env.PROJECT_DIR = 'api_testing_framework'
          } else if (fileExists('requirements.txt')) {
            env.PROJECT_DIR = '.'
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
                set -e
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
              '''
            }
          } else {
            dir(env.PROJECT_DIR) {
              bat '''
                @echo off
                rem Use py if available, else fall back to python
                where py >nul 2>nul && (py -3 -m venv venv) || (python -m venv venv)
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
                set -e
                . venv/bin/activate
                pytest -q --maxfail=1 --html=report.html --self-contained-html
              '''
            }
          } else {
            dir(env.PROJECT_DIR) {
              bat '''
                @echo off
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
      // Archive the HTML report and logs if present; no HTML Publisher needed
      script {
        def patterns = []
        patterns << "${env.PROJECT_DIR}/${env.REPORT_FILE}"
        patterns << "${env.PROJECT_DIR}/logs/**"
        archiveArtifacts artifacts: patterns.join(', '), allowEmptyArchive: true, fingerprint: true
      }
    }
  }
}
