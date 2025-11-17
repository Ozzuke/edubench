# EduBench

EduBench is a benchmark to evaluate the teaching capabilities of Large Language Models (LLMs).

## Project Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/edubench.git
    cd edubench
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.eduenv` file in the root of the project and add your API key:
    ```
    API_KEY=your_openai_api_key
    ```
    **Note:** A valid OpenAI API key is required for the benchmark to run.


## Running the Benchmark

To run the benchmark, execute the following command:

```bash
python3 -m src.edubench run
```

The results (conversations, evaluations, and a markdown report) will be saved in the `results` directory by default. You can specify a different output directory using the `--output-dir` option:

```bash
python3 -m src.edubench run --output-dir my_results
```
