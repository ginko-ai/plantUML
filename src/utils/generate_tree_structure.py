# exclude .venv and archive directories
# shared_tools/utils/generate_tree_structure.py
import os
from pathlib import Path
from typing import Union, List, Set, Optional, Dict
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class DirectoryFilter:
    """Handles directory and file filtering logic for tree generation."""
    exclude_dirs: Set[str] = field(default_factory=lambda: {
        '.venv',
        '.git',
        '__pycache__',
        '.pytest_cache',
        '.vscode',
        '.idea',
        'node_modules',
        'archive'  # Added archive to default exclusions
    })
    exclude_patterns: Set[str] = field(default_factory=lambda: {
        '*.pyc',
        '.env',
        '.DS_Store',
        '*.pyo',
        '*.pyd',
        '.ipynb_checkpoints'
    })

    # Track excluded items
    excluded_items: Dict[str, List[str]] = field(default_factory=lambda: {'dirs': [], 'files': []})

    def should_exclude(self, name: str, is_dir: bool = False, full_path: str = '') -> bool:
        """
        Check if a file or directory should be excluded and track excluded items.

        Args:
            name: Name of the file or directory
            is_dir: True if the item is a directory
            full_path: Full path of the item for tracking

        Returns:
            bool: True if the item should be excluded
        """
        if is_dir and (name in self.exclude_dirs or name == 'archive'):
            self.excluded_items['dirs'].append(full_path)
            return True

        pattern_match = any(
            pattern[1:] in name if pattern.startswith('*')
            else name.endswith(pattern[1:]) if pattern.startswith('*.')
            else pattern in name
            for pattern in self.exclude_patterns
        )

        if pattern_match and not is_dir:
            self.excluded_items['files'].append(full_path)
            return True

        return pattern_match

    def add_exclusions(self, dirs: Optional[List[str]] = None, patterns: Optional[List[str]] = None) -> None:
        """
        Add additional directories or patterns to exclude.

        Args:
            dirs: List of directory names to exclude
            patterns: List of file patterns to exclude
        """
        if dirs:
            self.exclude_dirs.update(dirs)
        if patterns:
            self.exclude_patterns.update(patterns)

    def get_exclusion_summary(self) -> str:
        """
        Generate a summary of excluded items.

        Returns:
            str: Formatted summary of exclusions
        """
        summary = [
            "# Generated Tree Structure",
            f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "#",
            "# Excluded Directories:",
        ]

        # Add excluded directories with their full paths
        if self.excluded_items['dirs']:
            for dir_path in sorted(set(self.excluded_items['dirs'])):
                summary.append(f"#   - {dir_path}")
        else:
            summary.append("#   None found")

        summary.extend([
            "#",
            "# Exclusion Patterns:",
            f"#   Directories: {', '.join(sorted(self.exclude_dirs))}",
            f"#   Files: {', '.join(sorted(self.exclude_patterns))}",
            "#\n"
        ])

        return '\n'.join(summary)

class ProjectTreeGenerator:
    """Generates a tree-like structure of the project directory."""

    def __init__(self, directory_filter: Optional[DirectoryFilter] = None):
        """
        Initialize the tree generator.

        Args:
            directory_filter: DirectoryFilter instance for exclusions
        """
        self.directory_filter = directory_filter or DirectoryFilter()

    def generate_tree(
        self,
        startpath: Union[str, Path],
        output_file: Union[str, Path] = 'README.md',
        include_files: bool = True
    ) -> None:
        """
        Generate a tree structure and save it to a file.

        Args:
            startpath: Starting directory path
            output_file: Output file path
            include_files: Whether to include files in the output
        """
        startpath = Path(startpath).resolve()
        output_file = Path(output_file)

        # Reset excluded items tracking
        self.directory_filter.excluded_items = {'dirs': [], 'files': []}

        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open('w', encoding='utf-8') as f:
            # Write exclusion summary
            f.write(self.directory_filter.get_exclusion_summary())

            # Write tree structure
            f.write('```tree\n')
            self._write_tree(f, startpath, startpath, include_files)
            f.write('```\n')

    def _write_tree(self, file, current_path: Path, start_path: Path, include_files: bool, level: int = 0) -> None:
        """
        Recursively write the tree structure.

        Args:
            file: Open file handle to write to
            current_path: Current directory being processed
            start_path: Root directory of the tree
            include_files: Whether to include files in the output
            level: Current directory depth
        """
        if level > 0:  # Don't print the root directory
            indent = '│   ' * (level - 1) + '├── '
            file.write(f'{indent}{current_path.name}/\n')

        # Process directories first
        dirs = sorted(d for d in current_path.iterdir()
                     if d.is_dir() and not self.directory_filter.should_exclude(d.name, True, str(d.relative_to(start_path))))

        for dir_path in dirs:
            self._write_tree(file, dir_path, start_path, include_files, level + 1)

        # Then process files if requested
        if include_files:
            files = sorted(f for f in current_path.iterdir()
                         if f.is_file() and not self.directory_filter.should_exclude(f.name, False, str(f.relative_to(start_path))))

            for file_path in files:
                indent = '│   ' * level + '├── '
                file.write(f'{indent}{file_path.name}\n')

def main():
    """Main function to run the tree generator."""
    try:
        # Initialize with custom exclusions
        dir_filter = DirectoryFilter()
        dir_filter.add_exclusions(
            dirs=['build', 'dist'],
            patterns=['*.egg-info', '*.log']
        )

        generator = ProjectTreeGenerator(dir_filter)

        # Use current directory in notebook context
        project_root = Path.cwd()
        output_path = project_root / 'docs' / 'project_structure.md'

        generator.generate_tree(project_root, output_path)
        print(f"Tree structure generated successfully at: {output_path}")

    except Exception as e:
        print(f"Error generating tree structure: {str(e)}")
        raise

if __name__ == '__main__':
    main()