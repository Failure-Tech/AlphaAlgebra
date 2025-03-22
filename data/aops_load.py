from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import json
import time

# URL of the category page
base_url = "https://artofproblemsolving.com"
# category_url = "https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Algebra_Problems&pageuntil=1999+AIME+Problems%2FProblem+5#mw-pages"
# category_url = f"https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Algebra_Problems&srsltid=AfmBOorruzc38Td17iwJirwFAIztsy0RAakXl8SvGqxJentsZ5c5CePo&pagefrom=1999+AIME+Problems%2FProblem+5#mw-pages"
category_url = f"https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Algebra_Problems&srsltid=AfmBOorruzc38Td17iwJirwFAIztsy0RAakXl8SvGqxJentsZ5c5CePo&pagefrom=2014+UNCO+Math+Contest+II+Problems%2FProblem+8#mw-pages"

# Create directory
# os.makedirs("./data/Problems", exist_ok=True)

options = Options()
options.add_argument('--headless')  # Optional
browser = webdriver.Chrome(options=options)

browser.get(category_url)

# STEP 1: Collect all links containing 'Problem' text
problem_links = []
try:
    links = browser.find_elements(By.CSS_SELECTOR, '#mw-pages a')
    for link in links:
        link_text = link.text
        if 'Problem' in link_text:
            href = link.get_attribute('href')
            problem_links.append((link_text, href))
except Exception as e:
    print(f"Error collecting links: {e}")

print(f"Collected {len(problem_links)} problem links.")

# STEP 2: Visit each link and scrape problem + solution
all_problems = {}

for title, link in problem_links:
    print(f"Visiting: {title}")
    browser.get(link)
    time.sleep(1)  # Allow time for page to load
    
    try:
        div = browser.find_element(By.CLASS_NAME, "mw-parser-output")
        elements = div.find_elements(By.XPATH, "./*")

        problem_content = []
        solution_content = []
        is_solution = False

        for element in elements:
            # Check for h2 or h3 headers (sometimes solution headers are in h3!)
            if element.tag_name in ["h2", "h3"]:
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

        key = title.replace('/', '_')  # Replace slashes to avoid issues
        all_problems[key] = {
            "problem_statement": "\n".join(problem_content),
            "solution": "\n".join(solution_content),
            "url": link
        }

        print(f"Scraped: {title}")

    except Exception as e:
        print(f"Error scraping {title}: {e}")
        all_problems[title] = {
            "problem_statement": "",
            "solution": "",
            "error": str(e),
            "url": link
        }

# STEP 3: Save results
with open("./data/Problems/problemthree.json", "w", encoding='utf-8') as f:
    json.dump(all_problems, f, ensure_ascii=False, indent=2)

browser.quit()
print("Scraping complete.")
