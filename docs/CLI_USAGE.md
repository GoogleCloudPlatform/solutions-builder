# Solution Builder CLI Usage

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
- This will find all occurance of the `sb-var:project_id` anchors in your folder, and replace with the new value "new-project-id"

The YAML file will become:

```yaml
detail:
  PROJECT_ID: new-project-id # sb-var:project_id
  OTHER: something
```

