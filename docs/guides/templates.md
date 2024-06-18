# Working with Template (component/module)

## Component/module template

- A component (or module) can be a Terraform module, a microservice (Python) module, or a frontend module.
- A template must have a `copier.yaml` to define variables
  and other configurations. You can still proceed if there's no
  `copier.yaml` in the template folder, but it will just copy
  entire folder without any modification.

There are three ways of adding a component:

- Add a component with built-in module template
- Add a component with a template in local folder
- Add a component with a template in remote Git repo

## Create a new template (module) from scratch

## Convert an existing module (terraform or microservice) into a template
