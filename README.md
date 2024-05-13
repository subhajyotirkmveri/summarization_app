## Purpose :- 

To save time while reading by summarizing a large article or text into fewer lines. 

# Configuring
First create a virtual environemnt.
```
python -m venv env
```
1. Clone this repository:
   
```
 git clone https://github.com/subhajyotirkmveri/summarization_app.git
 
```
2. Install all the depenedencies :
   
```
pip install -r requirements.txt
```

You would need to download and install git lfs 
and run in cmd to setup lfs
```
git lfs install 
```
3. Then clone the repository containing LaMini-Flan-T5-248M which is the LLM we're using. Make sure that LaMini-Flan-T5-248M is in the same directory as the cloned project.
```
git clone https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M
```

4. Open terminal and run the following command:
```
streamlit run app_5.py
```
## Application Preview :

![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_1.jpeg)
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_2.jpeg)

## Features :-

You can read the text of your long article in 4 ways :-

![InputTextWays](https://user-images.githubusercontent.com/56812557/212475484-5bd0addf-1b14-4820-b4e2-b21565de8b71.png)

  - By typing text on your own (or copy-paste).
  - Reading the text from **.txt file**.
  - Reading the text from **.pdf file**.(You can choose either to get summary of entire pdf or select any page interval).
  
  ![PdfInput](https://user-images.githubusercontent.com/56812557/212475479-d012f433-8ebd-4283-9c18-c1ebf552accf.png)

  - Reading the text from **wikipedia page** (All you have to do is to provide the url of that page. Program will automatically scrap the text and summarise it for you).
  

 
## Output :- 
 
   - This is some of the summary text return by the program. Main article was loaded by Wikipedia Page Url -> https://en.wikipedia.org/wiki/Artificial_intelligence
   
   ![Summary]
   
   - Comparison of Original Content vs Summarized content.
   
   ![OriginalvsSummaryWordCount]
   
