#!/usr/bin/env python3
"""
IntentFlow Workflow Validator

Validates IntentFlow workflow files against the specification.
Usage: python validate.py <workflow.md>
"""

import sys
import re
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationResult:
    """Result of workflow validation"""
    valid: bool
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    info: dict = field(default_factory=dict)


@dataclass
class Step:
    """Parsed workflow step"""
    number: int
    title: str
    task: Optional[str] = None
    dependencies: list = field(default_factory=list)
    save_as: Optional[str] = None
    success_criteria: list = field(default_factory=list)
    flexibility: Optional[str] = None
    flexibility_level: str = "guided"
    constraints: list = field(default_factory=list)
    error_handling: list = field(default_factory=list)


class WorkflowValidator:
    """Validates IntentFlow workflow documents"""
    
    VALID_FLEXIBILITY_LEVELS = ["strict", "guided", "autonomous"]
    
    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
        self.errors = []
        self.warnings = []
        self.title = None
        self.meta = {}
        self.context = None
        self.steps = []
        self.finalization = None
    
    def validate(self) -> ValidationResult:
        """Run all validations and return result"""
        self._parse_document()
        self._validate_structure()
        self._validate_steps()
        self._validate_step_flow()
        
        return ValidationResult(
            valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings,
            info={
                "title": self.title,
                "step_count": len(self.steps),
                "has_meta": bool(self.meta),
                "has_context": bool(self.context),
                "has_finalization": bool(self.finalization)
            }
        )
    
    def _parse_document(self):
        """Parse the markdown document into components"""
        # Extract title (first H1)
        title_match = re.search(r'^#\s+(?:Workflow:\s*)?(.+)$', self.content, re.MULTILINE)
        if title_match:
            self.title = title_match.group(1).strip()
        
        # Extract meta section
        meta_match = re.search(r'##\s+Meta\s*\n(.*?)(?=\n##|\n---|\Z)', self.content, re.DOTALL | re.IGNORECASE)
        if meta_match:
            self.meta = self._parse_meta(meta_match.group(1))
        
        # Extract context section
        context_match = re.search(r'##\s+Context\s*\n(.*?)(?=\n##|\n---|\Z)', self.content, re.DOTALL | re.IGNORECASE)
        if context_match:
            self.context = context_match.group(1).strip()
        
        # Extract steps
        step_pattern = r'##\s+Step\s+(\d+)[:\s]+(.+?)\n(.*?)(?=\n##\s+Step|\n##\s+Finalization|\Z)'
        for match in re.finditer(step_pattern, self.content, re.DOTALL | re.IGNORECASE):
            step = self._parse_step(
                int(match.group(1)),
                match.group(2).strip(),
                match.group(3)
            )
            self.steps.append(step)
        
        # Extract finalization
        final_match = re.search(r'##\s+Finalization\s*\n(.*)$', self.content, re.DOTALL | re.IGNORECASE)
        if final_match:
            self.finalization = final_match.group(1).strip()
    
    def _parse_meta(self, content: str) -> dict:
        """Parse meta section into key-value pairs"""
        meta = {}
        for line in content.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip().lower()] = value.strip()
        return meta
    
    def _parse_step(self, number: int, title: str, content: str) -> Step:
        """Parse a step section"""
        step = Step(number=number, title=title)
        
        # Extract Task
        task_match = re.search(r'###\s+Task\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
        if task_match:
            step.task = task_match.group(1).strip()
        
        # Extract Dependencies
        deps_match = re.search(r'###\s+Dependencies\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
        if deps_match:
            # Extract code blocks
            code_blocks = re.findall(r'```(?:bash|sh)?\n(.*?)```', deps_match.group(1), re.DOTALL)
            step.dependencies = [cmd.strip() for block in code_blocks for cmd in block.strip().split('\n') if cmd.strip()]
        
        # Extract Save as
        save_match = re.search(r'###\s+Save\s+as\s*\n[`"]?([^`"\n]+)[`"]?', content, re.IGNORECASE)
        if save_match:
            step.save_as = save_match.group(1).strip().strip('`"')
        
        # Extract Success criteria
        criteria_match = re.search(r'###\s+Success\s+criteria\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
        if criteria_match:
            criteria_text = criteria_match.group(1)
            step.success_criteria = [
                line.strip().lstrip('- ').lstrip('* ')
                for line in criteria_text.split('\n')
                if line.strip() and line.strip().startswith(('-', '*'))
            ]
        
        # Extract Flexibility
        flex_match = re.search(r'###\s+Flexibility\s*(?:\[(\w+)\])?\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
        if flex_match:
            if flex_match.group(1):
                step.flexibility_level = flex_match.group(1).lower()
            step.flexibility = flex_match.group(2).strip()
        
        # Extract Constraints
        const_match = re.search(r'###\s+Constraints\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
        if const_match:
            const_text = const_match.group(1)
            step.constraints = [
                line.strip().lstrip('- ').lstrip('* ')
                for line in const_text.split('\n')
                if line.strip() and line.strip().startswith(('-', '*'))
            ]
        
        # Extract Error handling
        error_match = re.search(r'###\s+If\s+something\s+goes\s+wrong\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
        if error_match:
            error_text = error_match.group(1)
            for line in error_text.split('\n'):
                if '→' in line or '->' in line:
                    parts = re.split(r'→|->',  line.strip().lstrip('- '))
                    if len(parts) == 2:
                        step.error_handling.append({
                            'condition': parts[0].strip(),
                            'action': parts[1].strip()
                        })
        
        return step
    
    def _validate_structure(self):
        """Validate overall document structure"""
        # Must have title
        if not self.title:
            self.errors.append("Missing workflow title (first H1 heading)")
        
        # Must have at least one step
        if not self.steps:
            self.errors.append("Workflow must contain at least one step")
        
        # Warn if no meta
        if not self.meta:
            self.warnings.append("Consider adding a Meta section with version and author")
        
        # Warn if no finalization
        if not self.finalization:
            self.warnings.append("Consider adding a Finalization section")
    
    def _validate_steps(self):
        """Validate individual steps"""
        for step in self.steps:
            prefix = f"Step {step.number}"
            
            # Must have task
            if not step.task:
                self.errors.append(f"{prefix}: Missing required 'Task' section")
            elif len(step.task) < 10:
                self.warnings.append(f"{prefix}: Task description seems too brief")
            
            # Validate flexibility level
            if step.flexibility_level not in self.VALID_FLEXIBILITY_LEVELS:
                self.errors.append(
                    f"{prefix}: Invalid flexibility level '{step.flexibility_level}'. "
                    f"Must be one of: {', '.join(self.VALID_FLEXIBILITY_LEVELS)}"
                )
            
            # Warn if no save_as for steps that produce output
            if not step.save_as and step.number < len(self.steps):
                self.warnings.append(f"{prefix}: Consider adding 'Save as' to create contract for next step")
            
            # Warn if no success criteria
            if not step.success_criteria:
                self.warnings.append(f"{prefix}: Consider adding 'Success criteria' for verification")
            
            # Validate save_as path format
            if step.save_as:
                if not step.save_as.startswith('/'):
                    self.warnings.append(f"{prefix}: 'Save as' path should be absolute (start with /)")
    
    def _validate_step_flow(self):
        """Validate step numbering and flow"""
        if not self.steps:
            return
        
        numbers = [s.number for s in self.steps]
        
        # Check for duplicates
        if len(numbers) != len(set(numbers)):
            self.errors.append("Duplicate step numbers found")
        
        # Check for sequential numbering
        expected = list(range(1, len(self.steps) + 1))
        if sorted(numbers) != expected:
            self.warnings.append(
                f"Step numbers are not sequential. Found: {sorted(numbers)}, "
                f"Expected: {expected}"
            )
        
        # Check for gaps
        for i in range(len(numbers) - 1):
            if sorted(numbers)[i + 1] - sorted(numbers)[i] > 1:
                self.warnings.append("Gap in step numbering detected")
                break


def validate_file(filepath: str) -> ValidationResult:
    """Validate a workflow file"""
    path = Path(filepath)
    
    if not path.exists():
        return ValidationResult(
            valid=False,
            errors=[f"File not found: {filepath}"]
        )
    
    if not path.suffix.lower() == '.md':
        return ValidationResult(
            valid=False,
            errors=["File must be a Markdown file (.md)"]
        )
    
    content = path.read_text(encoding='utf-8')
    validator = WorkflowValidator(content)
    return validator.validate()


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python validate.py <workflow.md>")
        print("       python validate.py <workflow.md> --json")
        sys.exit(1)
    
    filepath = sys.argv[1]
    json_output = '--json' in sys.argv
    
    result = validate_file(filepath)
    
    if json_output:
        output = {
            'valid': result.valid,
            'errors': result.errors,
            'warnings': result.warnings,
            'info': result.info
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"\n{'='*60}")
        print(f"IntentFlow Workflow Validator")
        print(f"{'='*60}")
        print(f"File: {filepath}")
        print(f"Title: {result.info.get('title', 'Unknown')}")
        print(f"Steps: {result.info.get('step_count', 0)}")
        print()
        
        if result.errors:
            print("❌ ERRORS:")
            for error in result.errors:
                print(f"   • {error}")
            print()
        
        if result.warnings:
            print("⚠️  WARNINGS:")
            for warning in result.warnings:
                print(f"   • {warning}")
            print()
        
        if result.valid:
            print("✅ Workflow is valid!")
        else:
            print("❌ Workflow has errors that must be fixed.")
        
        print()
    
    sys.exit(0 if result.valid else 1)


if __name__ == '__main__':
    main()
