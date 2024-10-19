import rich_click as click
import importlib.metadata

@click.command(
    context_settings=dict(help_option_names=['-h', '--help']),
    help="""List all registered console_scripts from the current package.

    This command scans the installed packages and lists all commands registered
    under the 'console_scripts' entry point group for the current package.
    It helps users discover available CLI tools from this package.

    Examples:

        $ list-scripts --help

    Output:

        - Command: add
          Module: imports.add:add

        - Command: subtract
          Module: imports.subtract:subtract

    If no console_scripts are found, the command will display a message indicating
    that no commands are registered.
    """
)
def list_console_scripts():
    """
    Lists all console_scripts registered in the current environment for this package.
    """
    # Set your package name here
    package_name = 'cli_tools'

    # Fetch all entry points in the 'console_scripts' group
    entry_points = importlib.metadata.entry_points(group='console_scripts')

    if not entry_points:
        click.echo("No console_scripts found.")
        return

    # Filter entry points to only include those that belong to the current package
    package_entry_points = [ep for ep in entry_points if ep.dist.name == package_name]

    if not package_entry_points:
        click.echo(f"No console_scripts found for package: {package_name}")
        return

    click.echo(f"Registered console_scripts for package '{package_name}':")
    for entry_point in package_entry_points:
        click.echo(f"- Command: {entry_point.name}")
        click.echo(f"  Module: {entry_point.value}")
        click.echo()

if __name__ == "__main__":
    # Invoke the command and show the list directly when called with --help
    list_console_scripts()
