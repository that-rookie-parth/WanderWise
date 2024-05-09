## Instructions

- we are only considering 5 states as of now, and presenting it as constraint.
    - two question about it:
        - ques1: why only 5 states?<Br>
        ans: this is because we have taken those 5 states based ont he survey of the indian gov, that these 5 states are the most visited tourist locations.
        - ques2: what is the constraint?<Br>
        ans: as we move down the list of the less visited states the information about these states decreases which hinders the model to produce the best output.
        this will be in the future scope that once we scale or deploy the model we ourself will collect the data which is missing.

- env file bana lo and openai api key daal do
- since we are scraping the data in two ways
    - native. i.e. by using selenium and getting all the content of the page
        - **in case of selenium you need to have the correct chrome driver to run the code**
        - i'll put some links here which i refered to solve this chrome dirver problem
        - https://chromedriver.chromium.org/getting-started
        - https://chromedriver.chromium.org/downloads/version-selection
        - https://youtu.be/NB8OceGZGjA?si=aoLjh_uBk77uzn33
            - this video will help you in setting up
    - by using langchain and gpt
        - code for this is availabe
        - this is a ipynb notebook from : https://youtu.be/8YWMYVn3Q98?si=MM6s04VKb3mRYTtA