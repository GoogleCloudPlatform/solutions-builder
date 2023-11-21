# Solutions Builder CLI Usage

## Global Variables

### Set and apply a global variable

You can add an anchor to specify where a variable to apply in the solution folder.

For example, in a YAML file:
```yaml
detail:
  PROJECT_ID: old-project-id # sb-var:project_id
  OTHER: something
```
- It sets a variable named "project_id" as the anchor for this "PROJECT_ID" property at the same line in the YAML file.

Then, you can run the following to replace the variable value:
```
$ sb vars set project_id new-project-id
```
- This will find all occurrence of the `sb-var:project_id` anchors in your folder, and replace with the new value "new-project-id"

The YAML file will become:

```yaml
detail:
  PROJECT_ID: new-project-id # sb-var:project_id
  OTHER: something
```

### Apply all existing global variables

You can apply all existing global variables to files with corresponding variable anchors.

For example, in a YAML file:
```yaml
detail:
  PROJECT_ID: old-project-id # sb-var:project_id
  OTHER: something
```

And in the `sb.yaml` file in your project root folder:
```yaml
global_variables:
  project_id: MY_PROJECT_ID
  project_name: core-solution-services
  project_number: MY_PROJECT_NUMBER
  gcp_region: us-central1
```

Run the following to apply all these values to existing variables in all files.
```
$ sb vars apply-all
```

All files with the corresponding anchors will be updated altogether.
