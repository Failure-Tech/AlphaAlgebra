from selenium import webdriver
import os
import shutil
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url=f"https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Algebra_Problems&srsltid=AfmBOorruzc38Td17iwJirwFAIztsy0RAakXl8SvGqxJentsZ5c5CePo&pagefrom=2014+UNCO+Math+Contest+II+Problems%2FProblem+8#mw-pages"

# Create directory
os.makedirs("./data/USAMO", exist_ok=True)

options = Options()
options.add_argument('--headless')  # Optional headless mode
browser = webdriver.Chrome(options=options)

all_problems = {}

for i in range(1972, 2025):
    for problem in range(1, 6):
        # url = f"https://artofproblemsolving.com/wiki/index.php/{i}_AIME_I_Problems/Problem_{problem}"
        url = f"https://artofproblemsolving.com/wiki/index.php/{i}_USAMO_Problems/Problem_{problem}"
        browser.get(url)

        try:
            div = browser.find_element(By.CLASS_NAME, "mw-parser-output")
            elements = div.find_elements(By.XPATH, "./*")

            problem_content = []
            solution_content = []
            is_solution = False

            for element in elements:
                # Detect h2 tag (usually "Solution" header)
                if element.tag_name == "h2":
                    header_text = element.text.lower()
                    if "solution" in header_text:
                        is_solution = True
                        continue

                # Collect content
                if element.tag_name in ["p", "ol", "ul", "math"]:
                    content = element.get_attribute("innerHTML").strip()
                    if not is_solution:
                        problem_content.append(content)
                    else:
                        solution_content.append(content)

            key = f"{i}_Problem_{problem}"
            all_problems[key] = {
                "problem_statement": "\n".join(problem_content),
                "solution": "\n".join(solution_content)
            }

            print(f"Scraped problem {problem} from AIME {i}")

        except Exception as e:
            print(f"Error scraping AIME {i} Problem {problem}: {e}")
            key = f"{i}_Problem_{problem}"
            all_problems[key] = {
                "problem_statement": "",
                "solution": "",
                "error": str(e)
            }

# Save to JSON
with open("./data/USAMO/USAMO.json", "w", encoding='utf-8') as f:
    json.dump(all_problems, f, ensure_ascii=False, indent=2)

browser.quit()
