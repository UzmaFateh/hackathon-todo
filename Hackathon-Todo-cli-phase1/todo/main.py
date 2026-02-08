import typer
from todo.services.task_service import TaskService
from todo.repositories.in_memory_repo import InMemoryTaskRepository
from todo.cli.commands import create_add_command, create_list_command, create_update_command, create_complete_command, create_delete_command

app = typer.Typer()

# Initialize the repository and service
repository = InMemoryTaskRepository()
task_service = TaskService(repository)

# Create and register the add command
add_command = create_add_command(task_service)
app.command(name="add")(add_command)

# Create and register the list command
list_command = create_list_command(task_service)
app.command(name="list")(list_command)

# Create and register the update command
update_command = create_update_command(task_service)
app.command(name="update")(update_command)

# Create and register the complete command
complete_command = create_complete_command(task_service)
app.command(name="complete")(complete_command)

# Create and register the delete command
delete_command = create_delete_command(task_service)
app.command(name="delete")(delete_command)


@app.callback()
def main():
    """
    Todo In-Memory Python Console Application
    """
    pass


if __name__ == "__main__":
    app()