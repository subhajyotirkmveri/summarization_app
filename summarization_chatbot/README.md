# Configuring
First create a virtual environemnt.
```
python -m venv env
```
Use the requirements.txt file to pip install the necessary dependencies.

```bash
pip install -r requirements.txt
```
You would need to download and install git lfs 
and run in cmd to setup lfs
```
git lfs install 
```
Then clone the repository containing LaMini-Flan-T5-248M which is the LLM we're using.
```
git clone https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M
```
Make sure that LaMini-Flan-T5-248M is in the same directory as the cloned project.
## Running
Now to run the app , run the below code
```
streamlit run app_4.py
```

