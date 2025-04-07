# from bs4 import BeautifulSoup

# def extract_latex(html_str):
#     soup = BeautifulSoup(html_str, "html.parser")
#     return ''.join(img['alt'] for img in soup.find_all("img") if "alt" in img.attrs)

# html="""If <img src=\"//latex.artofproblemsolving.com/b/5/5/b55ca7a0aa88ab7d58f4fc035317fdac39b17861.png\" class=\"latex\" alt=\"$r$\" width=\"8\" height=\"8\"> and <img src=\"//latex.artofproblemsolving.com/f/3/7/f37bba504894945c07a32f5496d74299a37aa51c.png\" class=\"latex\" alt=\"$s$\" width=\"8\" height=\"8\"> are the roots of the equation <img src=\"//latex.artofproblemsolving.com/9/8/1/98172d1b54b563033d26dc22c407dad4d4802be5.png\" class=\"latex\" alt=\"$ax^2+bx+c=0$\" style=\"vertical-align: -1px\" width=\"130\" height=\"16\">, the value of <img src=\"//latex.artofproblemsolving.com/3/0/2/302784340ca1a58f526dc9f9457fe9d64c474ba9.png\" class=\"latex\" alt=\"$\\frac{1}{r^{2}}+\\frac{1}{s^{2}}$\" style=\"vertical-align: -12px\" width=\"60\" height=\"37\"> is:\n<img src=\"//latex.artofproblemsolving.com/e/f/5/ef5d817038b2f51136767743740511bf6d71574f.png\" class=\"latex\" alt=\"$\\textbf{(A)}\\ b^{2}-4ac\\qquad\\textbf{(B)}\\ \\frac{b^{2}-4ac}{2a}\\qquad\\textbf{(C)}\\ \\frac{b^{2}-4ac}{c^{2}}\\qquad\\textbf{(D)}\\ \\frac{b^{2}-2ac}{c^{2}}$\" style=\"vertical-align: -12px\" width=\"504\" height=\"39\">\n<img src=\"//latex.artofproblemsolving.com/a/4/5/a4599cf9c5dfa99b4194c4a23fab69df841f6dd3.png\" class=\"latex\" alt=\"$\\textbf{(E)}\\ \\text{none of these}$\" style=\"vertical-align: -5px\" width=\"130\" height=\"18\">"""
# latex = extract_latex(html)
# print(f"Here is latex extraction: {latex}")

import re
from html import unescape

def extract_latex_from_html(html_string):
    # Decode HTML escape sequences
    html_string = unescape(html_string)

    # Use regex to extract alt attributes from img tags with class="latex"
    latex_matches = re.findall(r'<img[^>]*class="latex"[^>]*alt="([^"]+)"', html_string)

    # Join all LaTeX snippets together
    latex_string = ''.join(latex_matches)

    return latex_string

# Example usage
html_input = '''If <img src="//latex.artofproblemsolving.com/b/5/5/b55ca7a0aa88ab7d58f4fc035317fdac39b17861.png" class="latex" alt="$r$" width="8" height="8"> and <img src="//latex.artofproblemsolving.com/f/3/7/f37bba504894945c07a32f5496d74299a37aa51c.png" class="latex" alt="$s$" width="8" height="8"> are the roots of the equation <img src="//latex.artofproblemsolving.com/9/8/1/98172d1b54b563033d26dc22c407dad4d4802be5.png" class="latex" alt="$ax^2+bx+c=0$" style="vertical-align: -1px" width="130" height="16">, the value of <img src="//latex.artofproblemsolving.com/3/0/2/302784340ca1a58f526dc9f9457fe9d64c474ba9.png" class="latex" alt="$\\frac{1}{r^{2}}+\\frac{1}{s^{2}}$" style="vertical-align: -12px" width="60" height="37"> is:\n<img src="//latex.artofproblemsolving.com/e/f/5/ef5d817038b2f51136767743740511bf6d71574f.png" class="latex" alt="$\\textbf{(A)}\\ b^{2}-4ac\\qquad\\textbf{(B)}\\ \\frac{b^{2}-4ac}{2a}\\qquad\\textbf{(C)}\\ \\frac{b^{2}-4ac}{c^{2}}\\qquad\\textbf{(D)}\\ \\frac{b^{2}-2ac}{c^{2}}$" style="vertical-align: -12px" width="504" height="39">\n<img src="//latex.artofproblemsolving.com/a/4/5/a4599cf9c5dfa99b4194c4a23fab69df841f6dd3.png" class="latex" alt="$\\textbf{(E)}\\ \\text{none of these}$" style="vertical-align: -5px" width="130" height="18">'''

output = extract_latex_from_html(html_input)
print("Here is latex extraction:", output)
