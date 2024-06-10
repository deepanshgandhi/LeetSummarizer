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

## 4. Data Pipeline Components
The data pipeline comprises a single Directed Acyclic Graph (DAG) module encompassing five distinct tasks. Here's an overview of each task:

<!-- IMAGE GOES HERE -->

1. task_load_data : Initiates the execution of the load_data.py Python script to retrieve data from the source, which in our case is Firebase.

2. task_validate_schema : Utilizes validate_schema.py to ensure the integrity of the 'Python code' data stored within the dataset by validating its schema.

3. task_handle_comments : Executes handle_comments.py to eliminate comments from the 'Python code' data stored in the dataset, streamlining its structure.

4. task_validate_code : Utilizes validate_code.py to verify the syntactical correctness of the 'Python code' data stored in the dataset, ensuring adherence to programming standards.

5. task_print_final_data : Facilitates the display of the refined and validated dataset, providing a clear view of the processed data.

```
NOTE : NOTE: SchemaGen and StatisticsGen have been omitted from our pipeline as they are not pertinent to our project's dataset structure. However, it is advised to consider utilizing these libraries to enhance data handling capabilities.
```

## 5. Docker Setup
