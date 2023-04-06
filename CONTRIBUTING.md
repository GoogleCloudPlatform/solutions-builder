# Contributing to Solutions Template

This doc explains the development workflow to get started contributing to **Solutions Template**.

If you are looking for the general development guide for the generated code from this template, please refer to [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

## Bug Reports

If you encounter any issues or bugs, please [file a new Github Issue](https://github.com/GoogleCloudPlatform/solutions-template/issues/new).

- The Google team will triage the issues and will reply to your issues shortly.

## Development

### Tool requirements:

Install the dependencies according to root [README.md](https://github.com/GoogleCloudPlatform/solutions-template#tool-requirements).

Here's the high-level steps of the development flow:
- Create a **new fork** and a **new feature branch**.
- Develop and test locally (with your own Google Cloud project)
- Create a [Pull Request](https://github.com/GoogleCloudPlatform/solutions-template/compare) to merge to `main` branch.

### Create a new Fork

- [Click this link](https://github.com/GoogleCloudPlatform/solutions-template/fork) to create a new fork.
- Check out the code from your fork.
  ```
  git clone https://github.com/<your-Github-handle>/solutions-template.git
  ```
- Make sure the `origin` points to your fork.
  ```
  $ git remote -v
  origin  https://github.com/<your-Github-handle>/solutions-template.git (fetch)
  origin  https://github.com/<your-Github-handle>/solutions-template.git (push)
  ```
- Check out a new branch. This is to make your local work clean and separated.
  ```
  git checkout -b new-feature
  ```

### Test code changes in the Template

Once you made a few code changes locally, you'd want to test with a real Google Cloud project to ensure all steps run correctly.

> We will add more details of how to run end-to-end testing with your own test project.

### Build cookiecutter template folder

The key of making this codebase as a cookiecutter template is to generate `{{cookiecutter.project_id}}` folder.

For every code change, make sure to run the following to automatically re-generate the folder:
```
bash build_tools/build_template.sh
```

- This will scan all files and folders (with selection) and re-generate the `{{cookiecutter.project_id}}`.
- In addition, if you want to include a few more files in the `{{cookiecutter.project_id}}` folder, you can add more files and path defined in the [build_tools/build_template.sh](build_tools/build_template.sh)

### Commit code changes

Once generated `{{cookiecutter.project_id}}` folder, run the following to commit the changes to **your fork**.

```
git commit -a -m 'your message about this change'.
```

### Create a Pull Request for review

Create a [Pull Request](https://github.com/GoogleCloudPlatform/solutions-template/compare) to merge to `main` branch, and tag the project owners/admins to review.

- The project owners and admins will run end-to-end tests (TBD) to ensure the change doesn't break existing functions.

