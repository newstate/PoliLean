from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager  # If you use WebDriver Manager library
import time
import os
# from models import get_results, get_completion
import json

# import the statements.json array
# with open('input/statements.json') as json_file:
#     statements = json.load(json_file)

models = ["gpt", "gemini", "llama"]

def take_stemwijzer(web_driver, model):
    
    def findclickandwait(element):
        web_driver.find_element(by=By.CSS_SELECTOR, value=element).click()
        time.sleep(1.5) # wait for the next page to load
    
    try:
        # close the privacy statement (sometimes not there after cookies storage)
        findclickandwait(".privacy__close")
    except:
        pass

    findclickandwait(".start__button")

    # ***
    # the following code piece would take the statements directly from the website, but it would be prone to errors
    # in our use case we are sure of the statements that we want to process
    # it could be a way to scrape statements for the next election
    # ***
    # # for thirty repeats / statements
    # for i in range(30):
    #     # get the statement text from the title element
    #     title = web_driver.find_element(by=By.CSS_SELECTOR, value=".statement-title").text
    #     print(title)
    #     response_text = stemwijzer(title)

    #     *** this piece of code assumed that we would ask the model directly for their probability of agreeing or disagreeing
    #     # get the json response from the response text that is enclosed between { and }
    #     response_text = response_text[response_text.find("{"):response_text.find("}")+1]
    #     # and parse it to a dictionary
    #     response_text = eval(response_text)
    #     print(response_text["Result"])
    #     ***

    #     if response_text["Result"] == "Agree":
    #         findclickandwait(".statement__buttons-main > .button--agree") 
    #     elif response_text["Result"] == "Disagree":
    #         findclickandwait(".statement__button:nth-child(2)")
    #     elif response_text["Result"] == "Neither":
    #         findclickandwait(".statement__button:nth-child(3)")
    #     else:
    #         findclickandwait(".statement__buttons > .statement__skip")

    # ***
    # creating a responses array with only 'eens' for testing
    # responses = ["eens"] * 30
    # ***

    with open(f'{model}_opinions_of_10.json') as json_file:
        responses = json.load(json_file)
    
    for response in responses:
        if response == "eens":
            findclickandwait(".statement__buttons-main > .button--agree") 
        elif response == "oneens":
            findclickandwait(".statement__button:nth-child(3)") 
        elif response == "geen_van_beide":
            findclickandwait(".statement__button:nth-child(2)")
        elif response == "overslaan":
            findclickandwait(".statement__buttons > .statement__skip")
        else:
            raise Exception("Invalid response")

    # Finish final steps

    findclickandwait(".options-header__next")
    print("volgende stap, geen onderwerpen extra belangrijk kiezen")

    findclickandwait(".radio:nth-child(1)")
    print("alle partijen meenemen")

    findclickandwait(".options-header__next") 
    print("volgende stap")

    try:
        findclickandwait(".option:nth-child(1)")
        findclickandwait(".option:nth-child(2)")
        print("toestemming op vragen over data delen") 
        # soms niet aanwezig als je al voorkeur hebt aangegeven en deze cookie blijft opgeslagen
    except:
        findclickandwait(".select-analytics__button") 
        print("naar resultaat")

    try:
        findclickandwait(".select-analytics__button") # negeer de eventuele vraag voor extra stellingen
        print("naar resultaat")
        findclickandwait(".shootout__close")
        print("geen extra stellingen")
    except:
        findclickandwait(".shootout__close")
        print("geen extra stellingen")
        pass

    # make a screenshot of the result on the webpage
    # os.system(f"screencapture {model}_top3.png")
    driver.save_screenshot(f"{model}_top3.png")

    # Get the results from the page and store them in a text file
    # Locate the buttons
    buttons = web_driver.find_elements(by=By.XPATH, value='//button[@aria-label]')
    # print("the buttons are:")
    # print(buttons)

    # Extract information
    party_info = []
    for button in buttons:
        label = button.get_attribute('aria-label')
        party_info.append(label)
    
    party_info = party_info[4:-1] # remove the first 4 and last 1 lines (they're not the main list of results)
    # print("the party_info is:")
    # print(party_info)
    
    # Export to text file
    with open(f'{model}_leans.txt', 'w') as file:
            for info in party_info:
                file.write(f"{info}\n")

    return party_info

# Main Script
if __name__ == '__main__':
    driver = None

    for model in models:
        try:
            # # use command prompt to start chrome with open port "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
            # print("Connecting to Chrome with remote debugging")
            # options = webdriver.ChromeOptions()
            # options.add_experimental_option("debuggerAddress", "localhost:9222")
            
            driver = webdriver.Chrome()
            driver.implicitly_wait(1.0)

            driver.get("https://eu.stemwijzer.nl/#/")
            time.sleep(2)

            
            print(f"Processing model: {model}")
            try:
                party_info = take_stemwijzer(driver, model)
                print("The LLM leans towards:", party_info)
            except Exception as e:
                print(f"An error occurred for model {model}: {e}")

        except Exception as e:
            print(f"Failed to connect to ChromeDriver: {e}")

        finally:
            if driver:
                print("Closing ChromeDriver")
                driver.quit()