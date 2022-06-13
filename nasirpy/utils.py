from typing import Dict, Tuple, Optional
import re

def parse_route_pattern(pattern: str) -> Tuple[str, list]:
    """
    Parse a route pattern and return a regex pattern and parameter names
    Example: "/users/{id}/posts/{post_id}" ->
        "^/users/([^/]+)/posts/([^/]+)$", ["id", "post_id"]
    """
    params = []
    regex_parts = []
    
    # Split the pattern into parts
    parts = pattern.split('/')
    
    for part in parts:
        if not part:
            continue
        
        # Check if this is a parameter
        if part.startswith('{') and part.endswith('}'):
            param_name = part[1:-1]
            params.append(param_name)
            regex_parts.append('([^/]+)')
        else:
            regex_parts.append(re.escape(part))
    
    regex_pattern = '^/' + '/'.join(regex_parts) + '$'
    return regex_pattern, params

def match_route(pattern: str, path: str) -> Optional[Dict[str, str]]:
    """
    Match a path against a route pattern and return extracted parameters
    """
    regex_pattern, param_names = parse_route_pattern(pattern)
    match = re.match(regex_pattern, path)
    
    if match:
        params = match.groups()
        return dict(zip(param_names, params))
    return None
