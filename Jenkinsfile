// Jenkins Declarative Pipeline for API Testing Framework
//
// This pipeline demonstrates how to integrate the Python API testing framework
// with Jenkins for continuous regression.  It installs dependencies, runs
// pytest to execute the tests, generates an HTML report, and archives the
// results.  Integrating automated tests into CI/CD pipelines is a key
// principle of effective automation frameworks【860067245930328†L60-L67】【294264666156480†L313-L317】.

pipeline {
    agent any

    options {
        // Discard old builds to conserve disk space
        buildDiscarder(logRotator(numToKeepStr: '5'))
        // Fail the build if any stage fails
        skipStagesAfterUnstable()
    }

    stages {
        stage('Checkout') {
            steps {
                // Assume this Jenkins job is configured with SCM; otherwise specify git URL here
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest --html=report.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            // Archive test reports and logs regardless of build status
            archiveArtifacts artifacts: 'report.html, logs/**', fingerprint: true
            publishHTML (target : [reportDir: '.', reportFiles: 'report.html', reportName: 'API Test Report'])
        }
    }
}