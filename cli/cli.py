import typer

app = typer.Typer()


# Create a new solution
@app.command()
def new(name: str):
  print(f"Creating a new solution folder: {name}")


@app.command()
def add(component: str, name: str):
  print(f"Adding a component {component} with name {name}")


if __name__ == "__main__":
  app()
