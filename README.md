# LeetSummarizer

This is a Chrome extension that summarizes users' code on LeetCode in plain English. It breaks down the code into simple steps, explaining the logic and functionality in clear, easy-to-understand language.

---
---

# Milestone : Data Pipeline

## 1. Data Information
The dataset provided encompasses a comprehensive compilation of LeetCode questions, coupled with their corresponding code solutions and concise summaries. Reflecting the essence of algorithmic problem-solving, each entry encapsulates a unique challenge and its resolution, offering valuable insights into various coding paradigms and techniques. This repository serves as a reservoir for developers and coding enthusiasts alike, fostering skill development and proficiency enhancement in algorithmic problem-solving. While distinct from traditional transactional datasets, this collection plays a pivotal role in honing programming aptitude and fostering a deeper understanding of algorithmic complexities.


## 2. Data Card
| Variable Name | Role | Type | Description |
|-----------------|-----------------|-----------------|-----------------|
| Question | Feature | String | A concise representation of the LeetCode problem statement. |
| Code | Feature | String | The implemented solution for the corresponding LeetCode question. |
| Plain Text | Target | String | A succinct summary providing an explanation of the implemented code. |


## 3. Data Source
The dataset utilized in this project was generated internally to suit the specific requirements and objectives of the analysis. This self-curated dataset ensures relevance and alignment with the research goals, allowing for tailored insights and interpretations. By crafting our own data, we maintain control over its quality and suitability for the intended analyses.


## 4. Pipeline Setup
Setting up pipeline starts with setting up Apache Airflow. Apache Airflow is an open-source platform used to programmatically author, schedule, and monitor workflows. It enables users to orchestrate complex data pipelines with ease and reliability.

Install apache using the below command.
```bash
pip install apache-airflow
```

Next, start airflow's scheduler and web server to manage Directed Acyclic Graphs (DAGs) via a browser-based UI, where you define tasks and their dependencies for workflow automation.


## 5. Data Pipeline Components
The data pipeline comprises a single Directed Acyclic Graph (DAG) module encompassing five distinct tasks. Here's an overview of each task:

<!-- IMAGE GOES HERE -->
![Pipeline Flow](assets/pipeline_flow.jpg)

1. task_load_data : Initiates the execution of the load_data.py Python script to retrieve data from the source, which in our case is Firebase.

2. task_validate_schema : Utilizes validate_schema.py to ensure the integrity of the 'Python code' data stored within the dataset by validating its schema.

3. task_handle_comments : Executes handle_comments.py to eliminate comments from the 'Python code' data stored in the dataset, streamlining its structure.

4. task_validate_code : Utilizes validate_code.py to verify the syntactical correctness of the 'Python code' data stored in the dataset, ensuring adherence to programming standards.

5. task_print_final_data : Facilitates the display of the refined and validated dataset, providing a clear view of the processed data.

6. task_dvc_pipeline : Executes dvc_pipeline.py to update data versioning.

The below image shows the executed DAG pipeline.
<!-- IMAGE GOES HERE -->
![Pipeline Execution](assets/pipeline_execution.jpeg)


## 6. Features
- Tracking : For this task, Git serves as a robust version control system, facilitating project tracking through its branching and tagging capabilities. It enables teams to monitor changes, collaborate efficiently, and maintain a coherent history of project evolution.

- Logging : The project incorporates comprehensive try-except blocks within functions, capturing logs of successful executions or errors. These logs can be accessed in the logs/ directory created in the local machine after running the pipeline. Logging provides visibility into the execution process and facilitating error tracking and resolution.

- DVC : DVC (Data Version Control) plays a crucial role in managing and versioning large datasets efficiently. To facilitate the use of DVC in the project, a bucket was created in Google Cloud Storage as evidenced in the image below.
<!-- IMAGE GOES HERE -->
![DVC Execution Screenshot](assets/DVC_eg.jpeg)


```
NOTE : SchemaGen and StatisticsGen have been omitted from our pipeline as they are not pertinent to our project's dataset structure since we are dealing with strings whereas the aforementioned libraries are only pertinent for categorical/numerical data types. However, it is advised to consider utilizing these libraries to enhance data handling capabilities.
```

## Running The Project
Ensure that the following prerequisites are in place before running the project:
- Docker
- Airflow

<br>

Once all requirements are satisfied, execute the following commands to run the project:

Clone the GitHub repository
```bash
% git clone https://github.com/deepanshgandhi/LeetSummarizer.git
% cd LeetSummarizer
```

<br>

Download the docker image
```bash
LeetSummarizer % docker pull deepanshgandhi/leetsummarizer
```

<br>

Run the docker container
```bash
LeetSummarizer % docker-compose up -d
```

<br>

```
NOTE : Google service key is required in order to execute the project successfully. Please contact the team to generate your personal service key.

The service key should be added in the path: dags/src/data_preprocessing
```

---
---

# Milestone : Model Pipeline

## 1. Model Pipeline Components
The model pipeline comprises a single Directed Acyclic Graph (DAG) module encompassing 9 distinct tasks. The model pipeline gets's triggered after the execution of data pipeline. Below is an overview of each task present in the model pipeline:

<!-- IMAGE GOES HERE -->
![Pipeline Flow](assets/pipeline_flow.jpg)

1. task_install_dependencies : Executes the install_dependencies() function to install necessary Python packages and dependencies using pip, including a specific package from a GitHub repository and other listed libraries.

2. task_load_packages : Executes the load_packages() function to import and make available a variety of required Python packages and modules used in model training, while handling any module import errors.

3. task_load_data : Executes the load_data(file_path) function to read data from an [Excel file](), split it into training and testing datasets, and return these datasets.

4. task_load_model : Executes the load_model() function to load a pre-trained FastLanguageModel and its tokenizer with specified parameters, returning both the model and the tokenizer.

5. task_configure_model : The function configures a FastLanguageModel with specified parameters, including target modules, LoRA parameters, and gradient checkpointing options, and returns the configured model.

6. task_preprocess_data : Executes the preprocess_data() function to preprocess a DataFrame by formatting its columns into a specific text prompt, adding an end-of-sequence token, and converting the processed data into a dataset suitable for further use.

7. task_train_model : Executes the train_model() function to preprocess the training data, create a dataset, and train the provided model using specified training arguments and configurations, returning the trainer object and training statistics.

8. task_plot_loss : Executes the plot_loss() function to extract training loss values from the trainer's log history and plot them over training steps, displaying a graph of the training loss per step.

9. task_evaluate_model : Executes the evaluate_model() function to evaluate a given model on a test dataset (test_df) using specified evaluation metrics including ROUGE-L score and cosine similarity. It generates text based on prompts and compares them with actual texts, plotting ROUGE-L and similarity scores per data point, and returns lists of ROUGE-L and similarity scores.

The below image shows the executed DAG pipeline.
<!-- IMAGE GOES HERE -->
![Pipeline Execution](assets/pipeline_execution.jpeg)