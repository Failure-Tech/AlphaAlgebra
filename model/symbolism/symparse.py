# import json
# from sympy.parsing.latex import parse_latex
# from bs4 import BeautifulSoup
# from cerebras.cloud.sdk import Cerebras
# import os

# client = Cerebras(
#     api_key=os.getenviron("CEREBRAS_API")
# )

# # with open("./data/Problems/problem.json", "r", encoding="utf-8") as f:
# #     data = json.load(f)

# # with open("./data/Problems/problemtwo.json", "r", encoding="utf-8") as f:
# #     data = json.load(f)

# with open("./data/Problems/problemthree.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# # Function to extract and parse LaTeX expressions
# def extract_and_parse_latex(text):
#     soup = BeautifulSoup(text, "html.parser")

#     chat = client.chat.completions.create(
#         messages=[{
#             "role": "User",
#             "content": f"Sort out these questions so they are proper when being parsed through SymPy: "
#         }],
#         model="llama3.1-8b",
#     )
    
#     # Extract LaTeX expressions from <img alt="$...$">
#     latex_expressions = [img["alt"].strip("$") for img in soup.find_all("img") if "alt" in img.attrs]
    
#     # Convert LaTeX to SymPy
#     sympy_expressions = []
#     for expr in latex_expressions:
#         try:
#             sympy_expr = parse_latex(expr)
#             sympy_expressions.append(sympy_expr)
#         except Exception as e:
#             print(f"Error parsing LaTeX '{expr}': {e}")
#             sympy_expressions.append(None)  # Optionally add None if parsing fails
            
#     return sympy_expressions

# # Loop over all problems dynamically
# # for problem_name, problem_data in data.items():
# #     print(f"Processing: {problem_name}")
    
# #     problem_expressions = extract_and_parse_latex(problem_data.get("problem_statement", ""))
# #     solution_expressions = extract_and_parse_latex(problem_data.get("solution", ""))
    
# #     print("Extracted SymPy Expressions from Problem Statement:", problem_expressions)
# #     print("Extracted SymPy Expressions from Solution:", solution_expressions)
# #     print("-" * 50)

# # Add parsed expressions back to data
# for problem_name, problem_data in data.items():
#     problem_data["parsed_problem_expressions"] = [
#         str(expr) for expr in extract_and_parse_latex(problem_data.get("problem_statement", ""))
#     ]
#     problem_data["parsed_solution_expressions"] = [
#         str(expr) for expr in extract_and_parse_latex(problem_data.get("solution", ""))
#     ]

# # Save updated JSON
# with open("./data/Problems/Symbolic/parsed_problem3.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=2)

import json
from sympy.parsing.latex import parse_latex
from bs4 import BeautifulSoup
from cerebras.cloud.sdk import Cerebras
import os

print(os.environ)
# Initialize Cerebras client
api_key = "csk-9hxpm328d445wpyhvj8expnhmrpvcp8rh6d32tjmvfww8n8h"

client = Cerebras(
    # api_key=os.environ.get("CEREBRAS_API_KEY")
    api_key=api_key
)

# Load the original problem data
with open("./data/Problems/problemthree.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def preprocess_with_cerebras(text):
    """Send text to Cerebras for LaTeX cleanup"""
    try:
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Please clean up and standardize all LaTeX expressions in this text for SymPy parsing. Keep the original meaning but make sure the LaTeX is properly formatted. Return the exact same text but with corrected LaTeX:\n\n{text}"
            }],
            model="llama3.1-8b",
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in Cerebras preprocessing: {e}")
        return text  # Fallback to original text if error occurs

def extract_and_parse_latex(text):
    """Extract LaTeX from text, preprocess with Cerebras, then parse with SymPy"""
    # First preprocess the entire text with Cerebras
    preprocessed_text = preprocess_with_cerebras(text)
    
    soup = BeautifulSoup(preprocessed_text, "html.parser")
    
    # Extract LaTeX expressions from <img alt="$...$">
    latex_expressions = [img["alt"].strip("$") for img in soup.find_all("img") if "alt" in img.attrs]
    
    # Convert LaTeX to SymPy
    sympy_expressions = []
    for expr in latex_expressions:
        try:
            sympy_expr = parse_latex(expr)
            sympy_expressions.append(str(sympy_expr))
        except Exception as e:
            print(f"Error parsing LaTeX '{expr}': {e}")
            sympy_expressions.append(expr)  # Keep original if parsing fails
            
    return {
        "original_text": text,
        "preprocessed_text": preprocessed_text,
        "parsed_expressions": sympy_expressions
    }

# Process all problems and restructure the output
output_data = {}
for problem_name, problem_data in data.items():
    output_data[problem_name] = {
        "problem": extract_and_parse_latex(problem_data.get("problem_statement", "")),
        "solution": extract_and_parse_latex(problem_data.get("solution", ""))
    }

# Save updated JSON
with open("./data/Problems/Symbolic/parsed_problem3_structured.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("Processing complete. Output saved with separated problem and solution sections.")