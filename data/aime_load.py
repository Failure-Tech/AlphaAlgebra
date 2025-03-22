# # from selenium import webdriver
# # import os
# # import shutil
# # import json
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.options import Options

# # if os.path.exists("./data"):
# #     shutil.rmtree("./data")

# # os.mkdir("./data")
# # os.mkdir("./data/AIME")

# # options = Options()
# # browser = webdriver.Chrome(options=options)

# # all_problems = {}
# # for i in range(2000, 2025):
# #     year_dict = {}
# #     exam_dict = {}
# #     for problem in range(1, 16):
# #         url = f"https://artofproblemsolving.com/wiki/index.php/{i}_AIME_I_Problems/Problem_{problem}"
# #         browser.get(url)

# #     try: 
# #         div = browser.find_element(By.CLASS_NAME, "mw-parser-output")

# #         elements = div.find_elements(By.XPATH, ".//*")
# #         h2_index = next(i for i, elem in enumerate(elements) if elem.tag_name == "h2")

# #         problem_content = []
# #         for element in elements[h2_index+1]:
# #             if element.tag_name == "table":
# #                 break
            
# #             if element.tag_name in ["p"]:
# #                 latex_content = element.get_attribute("innerHTML")
# #                 problem_content.append(latex_content) # add .strip() if needed

# #         modified_content = f"\n".join(problem_content)
# #         exam_dict[problem] = {
# #             "problem_statement": modified_content if len(problem_content) > 0 else "",
# #         }

# #         print(f"Scrapped problem {problem} from AIME {i}")

# #     except Exception as e:
# #         print(f"Error in scrapping AIME {i} Problem {problem}")
# #         exam_dict[problem] = {
# #             "problem_statement": "",
# #             "error": str(e)
# #         }

# #     total = problem+i
# #     all_problems[total] = exam_dict[problem]

# # with open("./data/AIME.json", "w", encoding='utf-8') as f:
# #     json.dump(all_problems, f, ensure_ascii=False, indent=2)

# from selenium import webdriver
# import os
# import shutil
# import json
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

# # Clean data folder
# # if os.path.exists("./data"):
# #     shutil.rmtree("./data")

# # os.mkdir("./data")
# os.mkdir("./data/AIME")

# options = Options()
# options.add_argument('--headless')  # Run in headless mode (optional)
# browser = webdriver.Chrome(options=options)

# all_problems = {}

# for i in range(2000, 2025):
#     for problem in range(1, 16):
#         url = f"https://artofproblemsolving.com/wiki/index.php/{i}_AIME_II_Problems/Problem_{problem}"
#         browser.get(url)

#         try:
#             div = browser.find_element(By.CLASS_NAME, "mw-parser-output")
#             elements = div.find_elements(By.XPATH, "./*")

#             # Find index of <h2> (usually the "Solution" heading)
#             h2_index = None
#             for index, elem in enumerate(elements):
#                 if elem.tag_name == "h2":
#                     h2_index = index
#                     break

#             if h2_index is None:
#                 raise Exception("No <h2> found")

#             # Collect problem content till next table
#             problem_content = []
#             for element in elements[h2_index+1:]:
#                 if element.tag_name == "table":
#                     break
#                 if element.tag_name in ["p", "ol", "ul", "math"]:
#                     latex_content = element.get_attribute("innerHTML")
#                     problem_content.append(latex_content.strip())

#             modified_content = "\n".join(problem_content)
#             key = f"{i}_Problem_{problem}"
#             all_problems[key] = {
#                 "problem_statement": modified_content if len(problem_content) > 0 else "",
#             }

#             print(f"Scraped problem {problem} from AIME {i}")

#         except Exception as e:
#             print(f"Error scraping AIME {i} Problem {problem}: {e}")
#             key = f"{i}_Problem_{problem}"
#             all_problems[key] = {
#                 "problem_statement": "",
#                 "error": str(e)
#             }

# # Save all scraped problems
# with open("./data/AIME/AIME2.json", "w", encoding='utf-8') as f:
#     json.dump(all_problems, f, ensure_ascii=False, indent=2)

# browser.quit()
from selenium import webdriver
import os
import shutil
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Create directory
os.makedirs("./data/AIME", exist_ok=True)

options = Options()
options.add_argument('--headless')  # Optional headless mode
browser = webdriver.Chrome(options=options)

all_problems = {}

for i in range(2000, 2025):
    for problem in range(1, 16):
        url = f"https://artofproblemsolving.com/wiki/index.php/{i}_AIME_I_Problems/Problem_{problem}"
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
with open("./data/AIME/AIME1.json", "w", encoding='utf-8') as f:
    json.dump(all_problems, f, ensure_ascii=False, indent=2)

browser.quit()
