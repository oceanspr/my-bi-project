import yaml

workflow = {
    "name": "CI/CD - dbt Pipeline",
    "on": {
        "pull_request": {
            "branches": ["main", "develop"],
            "paths": ["models/**", "dbt_project.yml", "profiles.yml"]
        },
        "push": {
            "branches": ["main", "develop"],
            "paths": ["models/**", "dbt_project.yml", "profiles.yml"]
        }
    },
    "jobs": {
        "build-test-db-warehouse": {
            "name": "Build and Test dbt Models",
            "runs-on": "ubuntu-latest",
            "services": {
                "postgres": {
                    "image": "postgres:16-alpine",
                    "env": {
                        "POSTGRES_DB": "my_bi_db",
                        "POSTGRES_USER": "dbt_user",
                        "POSTGRES_PASSWORD": "${{ secrets.DB_TEST_PASSWORD }}"
                    },
                    "options": "--health-cmd=pg_isready --health-interval=10s --health-timeout=5s --health-retries=5",
                    "ports": ["5432:5432"]
                }
            },
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v4"},
                {"name": "Set up dbt-core", "uses": "dbt-labs/dbt-github-action-setup@v1", "with": {"dbt-version": "1.8.x"}},
                {"name": "Install dbt-postgres adapter", "run": "pip install --upgrade dbt-postgres&lt;2"}
            ]
        }
    }
}

with open('c:/Users/USER/Documents/Cline/my-bi-project/.github/workflows/ci-cd.yml', 'w') as f:
    yaml.dump(workflow, f, default_flow_style=False)

print("CI/CD workflow file created successfully!")