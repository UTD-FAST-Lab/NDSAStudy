# Extracting GitHub Issues and Commits

As a prerequisite, you need to create a GitHub personal access token (see [GitHub Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)) and a new project on MongoDB Atlas (see [MongoDB Documentation](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/).

Next, add your GitHub personal access token and MongoDB connection strings as environment variables to `~/.bashrc`:

```sh
export GH_TOKEN=<gh_personal_access_token>
export DB_CONNECTION_STRING=mongodb+srv://<db_username>:<db_password>@<clusterName>.mongodb.net/?retryWrites=true&w=majority
export DB_CONNECTION_STRING_EXPORT=mongodb+srv://<db_username>:<db_password>@<clusterName>.mongodb.net
```

Close `~/.bashrc` and run `source ~/.bashrc` for the changes to take effect.

Then, to extract the issues and commits from each tool's GitHub repository that are used in RQ1, follow the below steps:

Install the Python dependencies, run: 

`python -m pip install -r requirements.txt`

Run `python extractor.py` to start the issues and commits extraction. 

*Note: The extraction of issues and commits may take 1–2 hours to complete, and you may need to resume the process if it stops due to GitHub API limitations.*

`python extractor.py` will create a database named `NdGit` on MongoDB Atlas, and output the extracted results as several csv files named `<tool>_issues.csv` or `<tool>_commits.csv`.
These files will be stored in the `results/<keyword>` folder, organized by each keyword (concurrency, concurrent, determinism, deterministic, flakiness, flaky).

To export the raw data from MongoDB, run `bash export.sh`. 

It will output the raw data of each tool repository as a json file named `<tool>_issues.json` or `<tool>_commits.json` in the current directory. 