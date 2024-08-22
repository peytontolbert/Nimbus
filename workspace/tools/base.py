import inspect
from pydantic import Field, Extra, validator
from typing import Any, Callable, Dict


class AgentToolError(Exception):
    pass


class AgentTool:
    """
    Base class for agent tools.
    """
    def __init__(self, name, description, func, args, user_permission_required):
        self._name = name
        self._description = str(description)
        self._func = func
        self._args = args
        self._user_permission_required = user_permission_required
        
    def to_dict(self):
        return {
            "name": self._name,
            "description": self._description
        }


    @property
    def description(self):
        return self._description

    @property
    def name(self):
        return self._name

    @property
    def func(self):
        return self._func

    @property
    def user_permission_required(self):
        return self._user_permission_required
    
    @property
    def args(self) -> Dict:
        """Get the argument name and argument type from the signature"""
        func_signature = inspect.signature(self.func)
        required_args = {}

        for param in func_signature.parameters.values():
            param_name = str(param.name)
            required_args[param_name] = f"<{param_name}>"

        return required_args
    
    @args.setter
    def args(self, value):
        self._args = value

    class Config:
        extra = Extra.allow

    def run(self, **kwargs: Any) -> str:
        """Run the tool."""
        try:
            result = self.func(**kwargs)
        except (Exception, KeyboardInterrupt) as e:
            raise AgentToolError(str(e))
        return result

    def get_tool_info(self, include_args=True) -> str:
        """Get the tool info."""
        args_str = ", ".join([f"{k}: <{v}>" for k, v in self.args.items()])

        if include_args:
            return f"""{self.name}: "{self.description}", args: {args_str}"""
        else:
            return f"""{self.name}: "{self.description}"""


    @validator("name")
    def name_to_snake_case(name: str):
        """Convert the name to snake case."""
        if name is None:
            raise AttributeError("NoneType object has no attribute")

        s = str(name).strip()
        if not s:
            raise IndexError("Empty string")

        # Convert all uppercase letters to lowercase.
        s = s.lower()

        # Replace spaces, dashes, and other separators with underscores.
        s = s.replace(" ", "_")
        s = s.replace("-", "_")

        # Remove all characters that are not alphanumeric or underscore.
        s = "".join(c for c in s if c.isalnum() or c == "_")

        # Replace multiple consecutive underscores with a single underscore.
        s = "_".join(filter(None, s.split("_")))

        return s
