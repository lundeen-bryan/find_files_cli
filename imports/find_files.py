import os
import shutil
import fnmatch
import rich_click as click

# Function to search for files based on multiple lastname, firstname pairs
def search_files(directory, name_pairs):
    """Searches for files in the given directory that start with multiple 'Lastname, Firstname' pairs."""
    matching_files = []

    # Walk through the directory and find matching files for each name pair
    for lastname, firstname in name_pairs:
        pattern = f"{lastname.lower()}, {firstname.lower()}*"
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if fnmatch.fnmatch(filename.lower(), pattern):
                    full_path = os.path.join(root, filename)
                    matching_files.append(full_path)

    return matching_files

# Function to copy files to the destination directory
def copy_files(files, destination_directory):
    """Copies files to the destination directory."""
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    for file_path in files:
        filename = os.path.basename(file_path)
        destination_path = os.path.join(destination_directory, filename)
        shutil.copy(file_path, destination_path)
        print(f"Copied {file_path} to {destination_path}")

# Parse input names
def parse_name_pairs(names_input):
    """Parses the input string into a list of (lastname, firstname) pairs."""
    name_pairs = []
    names = names_input.split(";")
    for name in names:
        lastname, firstname = [n.strip() for n in name.split(",")]
        name_pairs.append((lastname, firstname))
    return name_pairs

# Click group to handle the commands
@click.group(context_settings=dict(help_option_names=['-h', '--help']), invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Main entry point for the CLI."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(search_wizard)

# Click function to handle the interactive wizard
@click.command(
    help="""
    Interactive wizard to search for files and copy them. Can enter multiple last name
    and first name pairs separated by semicolons.
    """,
    epilog="""
    Example usage:

    To search for one name:
    Smith, John

    To search for multiple names:
    Smith, John; Doe, Jane; Brown, Alice
    """
)
def search_wizard():
    """Interactive wizard to search for files and copy them."""

    # Step 1: Prompt for the search directory
    directory = click.prompt("Where do you want to search?", type=click.Path(exists=True, file_okay=False, dir_okay=True))

    # Step 2: Prompt for multiple last name and first name pairs
    names_input = click.prompt("Enter multiple 'Lastname, Firstname' pairs separated by semicolons (e.g., 'Smith, John; Doe, Jane')")
    name_pairs = parse_name_pairs(names_input)

    # Search for matching files
    matching_files = search_files(directory, name_pairs)

    # Step 4: Show found files and ask if the user wants to copy them
    if matching_files:
        click.echo(f"Found {len(matching_files)} matching files:")
        for file in matching_files:
            click.echo(f" - {file}")

        # Ask if the user wants to copy the files
        if click.confirm(f"Do you want to copy these {len(matching_files)} files?", default=True):

            # Step 5: Prompt for the destination directory
            destination_directory = click.prompt("Where do you want to copy the files?", type=click.Path(exists=True, file_okay=False, dir_okay=True))

            # Copy the files
            copy_files(matching_files, destination_directory)
            click.echo(f"Successfully copied {len(matching_files)} files.")
        else:
            click.echo("No files were copied.")
    else:
        click.echo("No matching files found.")

# Add the search wizard to the CLI group
cli.add_command(search_wizard, name="search")

if __name__ == "__main__":
    cli()
