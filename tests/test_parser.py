import pytest
from pathlib import Path
from pydantic import ValidationError

from advisor.parser import TemplateModel, parse_template_directory

def test_template_model_validation():
    # Valid model
    model = TemplateModel(name="test", description="A test", structure={"a": "b"})
    assert model.name == "test"

    # Missing fields should raise ValidationError
    with pytest.raises(ValidationError):
        TemplateModel(name="test", description="A test")

def test_parse_template_directory(tmp_path):
    # Setup dummy templates
    valid_yaml = tmp_path / "valid.yaml"
    valid_yaml.write_text("name: Valid Template\ndescription: A valid one\nstructure:\n  root: {}")

    invalid_yaml = tmp_path / "invalid.yaml"
    invalid_yaml.write_text("name: Invalid Template\n  badindent: true")

    missing_fields_yaml = tmp_path / "missing.yaml"
    missing_fields_yaml.write_text("name: Missing Structure\ndescription: No structure here")

    not_a_yaml = tmp_path / "readme.txt"
    not_a_yaml.write_text("This is not a yaml file")

    templates = parse_template_directory(tmp_path)

    assert len(templates) == 1
    assert templates[0].name == "Valid Template"
    assert templates[0].description == "A valid one"
    assert templates[0].structure == {"root": {}}
