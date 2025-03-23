# import json
# import re
# from sympy import symbols
# from sympy.parsing.latex import parse_latex

# with open("../data/Problems/problem.json", "r") as f:
#     json_data = json.loads(f)

# json_data = """
# {
#     "problem_statement": "When the ball is hit from the bottom wicket, it has a <img src=\\"//latex.artofproblemsolving.com/9/0/6/906734e2f1010e9a171ffee8050cbc0649cea37c.png\\" class=\\"latex\\" alt=\\"$50$\\" width=\\"17\\" height=\\"12\\">% chance...",
#     "solution": "Let <img src=\\"//latex.artofproblemsolving.com/6/a/4/6a47ca0fe7cb276abc022af6ac88ddae1a9d6894.png\\" class=\\"latex\\" alt=\\"$X$\\" width=\\"15\\">..."
# }
# """

# json_data = json.loads(json_data)

# def extract_parse(text):
#     latex_expressions = re.findall(r'alt=\\"(\$.*?\$)\\"')
#     sympy_expressions = [parse_latex(expr.strip("$")) for expr in latex_expressions]
#     return sympy_expressions

# problem = extract_parse(json_data["problem_statement"])
# solution = extract_parse(json.data["solution"])

# print(f"Extracted SymPy Expressions Problem: {problem}")

# import json
# import re
# from sympy.parsing.latex import parse_latex
# from bs4 import BeautifulSoup

# # try:
# #     import antlr4
# #     print("it work")
# # except ImportError:
# #     print("no work")

# # Example JSON (Replace with actual JSON)
# # json_data = """
# # {
# #     "problem_statement": "When the ball is hit from the bottom wicket, it has a <img src=\\"//latex.artofproblemsolving.com/9/0/6/906734e2f1010e9a171ffee8050cbc0649cea37c.png\\" class=\\"latex\\" alt=\\"$50$\\" width=\\"17\\" height=\\"12\\">% chance...",
# #     "solution": "Let <img src=\\"//latex.artofproblemsolving.com/6/a/4/6a47ca0fe7cb276abc022af6ac88ddae1a9d6894.png\\" class=\\"latex\\" alt=\\"$X$\\" width=\\"15\\"> be the probability..."
# # }
# # """

# with open("./data/Problems/problem.json", "r", encoding="utf-8") as f:
#     json_data = f.read()

# # Load JSON
# data = json.loads(json_data)

# # Function to extract and parse LaTeX expressions
# def extract_and_parse_latex(text):
#     # Use BeautifulSoup to parse HTML (more reliable than regex alone)
#     soup = BeautifulSoup(text, "html.parser")
    
#     # Extract all LaTeX expressions from <img> tags (inside alt attributes)
#     latex_expressions = [img["alt"].strip("$") for img in soup.find_all("img") if "alt" in img.attrs]
    
#     # Convert LaTeX to SymPy expressions
#     sympy_expressions = [parse_latex(expr) for expr in latex_expressions]

#     return sympy_expressions

# # Extract and parse LaTeX from both problem statement and solution
# problem_expressions = extract_and_parse_latex(data["problem_statement"])
# solution_expressions = extract_and_parse_latex(data["solution"])

# # Output results
# print("Extracted SymPy Expressions from Problem Statement:", problem_expressions)
# print("Extracted SymPy Expressions from Solution:", solution_expressions)

import json
from sympy.parsing.latex import parse_latex
from bs4 import BeautifulSoup

with open("./data/Problems/problem.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Function to extract and parse LaTeX expressions
def extract_and_parse_latex(text):
    soup = BeautifulSoup(text, "html.parser")
    
    # Extract LaTeX expressions from <img alt="$...$">
    latex_expressions = [img["alt"].strip("$") for img in soup.find_all("img") if "alt" in img.attrs]
    
    # Convert LaTeX to SymPy
    sympy_expressions = []
    for expr in latex_expressions:
        try:
            sympy_expr = parse_latex(expr)
            sympy_expressions.append(sympy_expr)
        except Exception as e:
            print(f"Error parsing LaTeX '{expr}': {e}")
            sympy_expressions.append(None)  # Optionally add None if parsing fails
            
    return sympy_expressions

# Loop over all problems dynamically
# for problem_name, problem_data in data.items():
#     print(f"Processing: {problem_name}")
    
#     problem_expressions = extract_and_parse_latex(problem_data.get("problem_statement", ""))
#     solution_expressions = extract_and_parse_latex(problem_data.get("solution", ""))
    
#     print("Extracted SymPy Expressions from Problem Statement:", problem_expressions)
#     print("Extracted SymPy Expressions from Solution:", solution_expressions)
#     print("-" * 50)

# Add parsed expressions back to data
for problem_name, problem_data in data.items():
    problem_data["parsed_problem_expressions"] = [
        str(expr) for expr in extract_and_parse_latex(problem_data.get("problem_statement", ""))
    ]
    problem_data["parsed_solution_expressions"] = [
        str(expr) for expr in extract_and_parse_latex(problem_data.get("solution", ""))
    ]

# Save updated JSON
with open("./data/Problems/Symbolic/parsed_problem.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
