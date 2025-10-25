# API Testing Framework for Continuous Regression

## Overview

This project demonstrates a **reusable API‑testing framework** built in Python and designed for continuous regression.  The framework encapsulates common functionality for sending HTTP requests, reading configuration and test data, generating logs and reports, and integrating with Jenkins for automated execution.

The framework is structured around the key principles of test automation highlighted in modern QA literature:

* **Scalability and maintainability** – the framework organises test scripts and data logically so it can grow with your application.  A modular structure helps keep tests easy to maintain【294264666156480†L120-L139】.
* **Reusability** – common functions and libraries are abstracted into reusable modules.  This reduces duplication and effort across multiple tests【294264666156480†L120-L139】 and maximises reuse across projects【294264666156480†L350-L370】.
* **Robust reporting and logging** – comprehensive logging and HTML reports make it easy to diagnose failures and analyse results【294264666156480†L290-L299】.
* **CI/CD integration** – the framework is designed to run in a Jenkins pipeline, enabling continuous regression on every code change【860067245930328†L60-L67】【294264666156480†L313-L317】.

## Directory Structure

```text
api_testing_framework/
├── Jenkinsfile          # Jenkins pipeline for continuous regression
├── README.md            # This documentation file
├── requirements.txt     # Python dependencies
├── pytest.ini           # Pytest configuration
├── config.yaml          # Environment configuration (base URLs, endpoints)
├── data/                # Test data files used by the tests
│   └── test_data.yaml   # Sample test definitions
├── logs/                # Location where execution logs will be stored
├── src/                 # Source code for the framework
│   ├── api_client.py    # Reusable HTTP client class
│   └── utils/
│       ├── config.py    # Configuration loader
│       └── logger.py    # Logging setup
└── tests/               # Automated test cases using pytest
    └── test_sample_api.py
```

## Getting Started

### Prerequisites

This framework requires **Python 3.8+** and uses the packages specified in `requirements.txt`.  It has been tested on Linux/macOS and can be easily adapted for Windows.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

* `config.yaml` contains the base URL of the API under test and a mapping of logical names to endpoint paths.  You can define multiple environments (e.g. `dev`, `stage`, `prod`) and select the desired environment via the environment variable `ENVIRONMENT` or by editing the file.
* `data/test_data.yaml` holds a list of test cases.  Each test defines the HTTP method, endpoint, parameters, expected status and (optionally) expected response keys.

### Running Tests Locally

To execute the tests locally, run:

```bash
pytest --html=report.html --self-contained-html
```

The `pytest-html` plugin is used to generate an interactive HTML report stored as `report.html`.  Detailed logging is written to the `logs/` directory.

### Jenkins Integration

The `Jenkinsfile` defines a declarative pipeline that installs dependencies, runs the tests and archives the resulting report.  Integrating automated tests into a CI/CD pipeline allows regression tests to run on every build or code change and is a recommended best practice【860067245930328†L60-L67】.  The pipeline has the following stages:

1. **Checkout** – pulls the latest code from the repository.
2. **Set up Python** – creates a virtual environment and installs dependencies.
3. **Run Tests** – executes pytest with HTML reporting.
4. **Archive Artifacts** – archives the HTML report and logs for future review.

To enable continuous regression, schedule the Jenkins job to run periodically or trigger it on source‑code changes.  Integration with Jenkins ensures early detection of defects and helps maintain software quality【294264666156480†L313-L317】.

### Extending the Framework

The framework is intentionally simple to make it easy to extend:

* **Add new APIs:** Update `config.yaml` with the endpoint paths and add corresponding test cases to `data/test_data.yaml`.
* **Add utility methods:** Implement reusable functions in `src/api_client.py` or create new modules under `src/utils/`.
* **Custom assertions:** Enhance `tests/test_sample_api.py` with domain‑specific assertions.

Well‑designed frameworks promote collaboration and reuse across teams【294264666156480†L120-L139】.  By centralising configuration and test data, you can run the same tests against multiple environments without changing the test logic.

## References

The design of this framework is informed by best practices from reputable QA sources.  These sources emphasise the importance of reusability, scalability and CI/CD integration when building automation frameworks【294264666156480†L120-L139】【294264666156480†L313-L317】.  They also highlight the need for robust reporting and logging to facilitate debugging and analysis【294264666156480†L290-L299】.  Finally, continuous regression through CI pipelines ensures that tests run automatically on every build and helps maintain high software quality【860067245930328†L60-L67】.