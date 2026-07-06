import logging
from pathlib import Path
from typing import List, Any
import yaml
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

class TemplateModel(BaseModel):
    name: str
    description: str
    structure: Any

def parse_template_directory(directory_path: Path) -> List[TemplateModel]:
    """
    Parses all .yaml and .yml files in the given directory into TemplateModel objects.
    Safely ignores non-YAML files and malformed templates, logging warnings instead of crashing.
    """
    templates = []
    if not directory_path.exists() or not directory_path.is_dir():
        logger.warning(f"Directory {directory_path} does not exist or is not a directory.")
        return templates

    for file_path in directory_path.iterdir():
        if file_path.suffix.lower() in ['.yaml', '.yml']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)
                if not isinstance(content, dict):
                    logger.warning(f"Skipping {file_path}: YAML root must be a mapping.")
                    continue
                template = TemplateModel(**content)
                templates.append(template)
            except yaml.YAMLError as e:
                logger.warning(f"Skipping {file_path}: YAML parsing error - {e}")
            except ValidationError as e:
                logger.warning(f"Skipping {file_path}: Validation error - {e}")
            except Exception as e:
                logger.warning(f"Skipping {file_path}: Unexpected error - {e}")
        else:
            logger.debug(f"Skipping {file_path}: Not a YAML file.")
            
    return templates
