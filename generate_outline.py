import re
from pathlib import Path

def format_title_from_filename(filename_stem):
    # Remove leading number and hyphen
    name_part = re.sub(r"^[0-9]+-", "", filename_stem)
    # Replace hyphens/underscores with spaces and capitalize words
    name_part = name_part.replace('_', ' ')
    return ' '.join(word.capitalize() for word in name_part.split('-'))

def get_title_from_file(file_path: Path):
    """Reads the first H1 heading (# ) from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip() # Return text after '# '
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return None # Return None if no H1 found or error reading

def generate_outline():
    readme_path = Path("README.md")
    outline_content = []
    files_data = []

    # Find numbered markdown files in the current directory
    for item in Path(".").iterdir():
        if item.is_file() and item.suffix == ".md" and re.match(r"^[0-9]+-", item.name):
            match = re.match(r"^([0-9]+)-", item.name)
            if match:
                number = int(match.group(1))
                # Try getting title from H1 first
                title = get_title_from_file(item)
                # Fallback to filename if H1 not found
                if title is None:
                    title = format_title_from_filename(item.stem)
                files_data.append({"number": number, "title": title})

    # Sort files by number
    files_data.sort(key=lambda x: x["number"])

    # Create the markdown list
    for i, data in enumerate(files_data):
        # Use the actual number from the filename for the list item
        outline_content.append(f"{i + 1}. {data['title']}") # Using i+1 for sequential numbering

    outline_str = "\n".join(outline_content)

    # Read README.md content
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"Error: {readme_path} not found.")
        return

    # Replace the content between markers
    start_marker = "<!-- OUTLINE:START -->"
    end_marker = "<!-- OUTLINE:END -->"

    start_index = readme_content.find(start_marker)
    end_index = readme_content.find(end_marker)

    if start_index == -1 or end_index == -1 or start_index >= end_index:
        print("Error: Outline markers not found or in wrong order in README.md.")
        print("Please add '<!-- OUTLINE:START -->' and '<!-- OUTLINE:END -->' markers.")
        return

    new_readme_content = (
        readme_content[:start_index + len(start_marker)] +
        "\n" + # Add newline after start marker
        outline_str +
        "\n" + # Add newline before end marker
        readme_content[end_index:]
    )

    # Write the updated content back to README.md
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_readme_content)
        print("README.md outline updated successfully.")
    except IOError as e:
        print(f"Error writing to {readme_path}: {e}")

if __name__ == "__main__":
    generate_outline() 