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
2. Go to the cloning folder
```
cd summarization_app
```
3. Install all the depenedencies :   
```
pip install -r requirements.txt
```

You would need to download and install git lfs 
and run in cmd to setup lfs
```
git lfs install 
```
4. Then clone the repository containing LaMini-Flan-T5-248M which is the LLM we're using. Make sure that LaMini-Flan-T5-248M is within cloned project.
```
git clone https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M
```

5. Open terminal and run the following command:
```
streamlit run app_5.py
```
## Application Preview :
You can select text from your lengthy article in four ways:-
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_1.jpeg)

  - By typing text on your own (or copy-paste).
  - Reading the text from **.txt file**.
  - Reading the text from **.pdf file**.(You can choose either to get summary of entire pdf or select any page interval).
  
  - Reading the text from **wikipedia page** (All you have to do is to provide the url of that page. Program will automatically scrap the text and summarise it for you).
  

 
## Output :- 
- This is a portion of the summary text returned by the program when selecting "typing text on your own (or copy-paste)", you can also accordingly choose minimun number of token and maximum number of tokenand press enter for taking those value-
Click the "Summarize" button for summarize the input text:-
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_2.jpeg)
summarize result of the input text given below:-
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_3.jpeg)
- This is a snippet of the summary text returned by the program if ".txt" is chosen, you can also accordingly choose minimun number of token and maximum number of token and press enter for taking those value and upload any .txt file:-

![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_4.jpeg)
Click the "Summarize" button for summarize the .txt file:
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_5.jpeg)
- This is a portion of the summary text provided by the program when selecting the ".pdf" option ,you can also accordingly choose minimun number of token and maximum number of token and press enter for taking those value and upload any .pdf file:-
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_6.jpeg)
Click the "Summarize" button and navigate to the terminal. Then, input the page number you wish to summarize by typing an integer value. If you type "Y" then it summarize whole document: one such sample given below
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_7.jpeg)
showing the whole pdf document
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_8.jpeg)
Summarize result:-
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_9.jpeg)
- This is some of the summary text return by the program. Main article was loaded by some wiki url
![image](https://github.com/subhajyotirkmveri/summarization_app/blob/main/asset/asset_10.jpeg)

## You can also utilize another Python file for summarizing the corresponding input. In the app_5.py file, only one pipeline is employed for all cases.   

   
