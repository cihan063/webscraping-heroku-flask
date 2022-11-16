# Coursera's url
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import re
from time import sleep
import pandas as pd 


import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options as ChromeOptions
chromedriver_autoinstaller.install()  


#str_category = "machine learning"
#c = "machine%20learning"

def scrape_courses(str_category,pages):
    """
     This function provides you to scrape some information of courses on coursera 
     Parameters:
         str_category: (type : str) Searching Category as string 
         pages: (type : int) how many pages you want to scrape
    """
    category_name = []
    course_name = []
    #course_provider = []
    course_instructor = []
    course_description =[]
    course_enrolled = []
    course_rating = []

    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    c = str_category.replace(' ','%20')
    url = "https://www.coursera.org/search?query="+str(c)+"&page=1&index=prod_all_launched_products_term_optimization&entityTypeDescription=Courses"
    driver.get(url)

 

    driver.close()
    #  iterate through the pages
    for i in range(1,pages+1):
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        url = "https://www.coursera.org/search?query="+str(c)+"&page="+str(i)+"&index=prod_all_launched_products_term_optimization&entityTypeDescription=Courses"
        driver.get(url)
        # Getting all the courses
        courses= driver.find_elements(By.CSS_SELECTOR, '[data-click-key="search.search.click.search_card"]')
        
        links = []
        for course in courses:
            # ı will take the provider and the name of the course from the course's card
            data = course.text.split("\n")
            print(course.text)
            if data[0]!='Free':
                #course_provider.append(data[0])
                course_name.append(data[1])
            else:
                #course_provider.append(data[1])
                course_name.append(data[2])
            # get the link to the course to get the other info
            url1 = str(course.get_attribute('href'))
            links.append(url1)
            print(len(links))
            print(links)
        # iterate through the links to the courses
        for link in links:
            driver1 = webdriver.Chrome(executable_path='chromedriver.exe')
            driver1.get(link)
            # get the element with the students enrolled
            elements = driver1.find_elements(By.XPATH, "//span[contains(text(), 'enrolled')]")
            if(len(elements) > 0):
                course_enrolled.append(re.search(r"[0-9,.]+",elements[0].text)[0])
            else:
                elements = driver1.find_elements(By.XPATH, "//span[contains(text(), 'ratings')]")  
                if len(elements) > 0:
                    res = re.search(r"([0-9,.]+)( already enrolled)",elements[0].text)
                    if res:
                        course_enrolled.append(res.group(1))
                    else:
                        course_enrolled.append(0)     
                else:
                    course_enrolled.append(0)
            #  get the element with the ratings        
            elements = driver1.find_elements(By.XPATH, "//span[contains(text(), 'ratings')]")
            if(len(elements) > 0):
                res = re.search(r"^([^r]+)([r])",elements[0].text)
                if res:
                    course_rating.append(res.group(1).strip())
                else:
                    course_rating.append(0)
            else:
                course_rating.append(0) 
            #  get the element with the description of the course
            elements = driver1.find_elements(By.XPATH, '//div[contains(@class, "About")]')
            if len(elements) > 0:
                text = ""
                paragraphs= elements[0].find_elements(By.CSS_SELECTOR, 'p')
                for paragraph in paragraphs:
                    if len(paragraph.text) > 150:
                        text += "\n\n"+paragraph.text
                course_description.append(text.strip("\n"))
            
            elements = driver1.find_elements(By.XPATH, '//h3[contains(@class, "instructor-name")]')
            if len(elements) > 0:
                instructor = elements[0].text.split('\n')[0].split(',')[0]
                course_instructor.append(instructor)

            category_name.append(str_category)

            driver1.close()
    driver.close()
    # create a list with the info to be pase to the dataframe
    courses_info = [[cat_name, name, instructor, description, enrrolled, ratings] for cat_name, name, instructor, description, enrrolled, ratings in zip(category_name,course_name,course_instructor,course_description,course_enrolled,course_rating)]
    # create the dataframe
    courses_by_search = pd.DataFrame(courses_info)
    courses_by_search.columns = ["Category Name","Course Name","First Instructor Name","Course Description","# of Students Enrolled","# ratings"]
    #print(courses_by_search)

    return courses_by_search

