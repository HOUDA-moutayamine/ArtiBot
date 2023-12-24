# ArtiBot
# arxiv-app 

## **Get your own personal research helper chatbot**

## Inspiration
looking for new directions of research always seemed to be one of the more challenging aspects. In addition, once most of the paper was done, it took so much time to find the relevant papers to cite. It would have been extremely helpful to have a tool that I can query to get me the latest papers, and then have a chatbot interface that I can ask intelligent questions to regarding the areas of research, and get an idea of future directions of research. This also applies to writing review articles about a topic

# ARtiBot - Your Academic Research Assistant

## Inspiration
My inspiration for ARtiBot comes from a desire to simplify and streamline the academic research experience. We envisioned a solution that empowers individuals to effortlessly access and comprehend scientific articles, saving valuable time and resources. ARtiBot is my response 
to the challenges faced by the academic community. It would have been extremely helpful to have a tool that I can query to get me the latest papers, and then have a chatbot interface that I can ask intelligent questions to regarding the areas of research, and get an idea of future directions of research.

## What Drives Me

At the core of ARtiBot is a commitment to democratizing knowledge and making academic research more accessible to all. We firmly believe that everyone should have the opportunity to engage with cutting-edge research, regardless of their background or expertise.
My motivation is driven by a passion for learning and the pursuit of knowledge. We aim to break down barriers in academia, making it easier for students, researchers, and curious minds to explore the wealth of information available. ARtiBot embodies my dedication to fostering a culture of lifelong learning and discovery.

## Key Objectives

The key objectives of ARtiBot are:

1. **Simplify Research:** ARtiBot aims to simplify the process of finding, accessing, and comprehending scientific articles. I want to make research more approachable for everyone.

2. **Efficient Access:** I'm committed to providing efficient access to academic resources, helping users locate relevant articles quickly.

3. **Enhance Understanding:** ARtiBot strives to enhance the understanding of complex research papers by providing summaries and insights.

4. **Open Access Advocacy:** We promote open access initiatives and support the dissemination of knowledge without barriers.

## How It Works
ARtiBot operates as a seamless three-part pipeline:

1. **PDF Retrieval:** The first part queries the arXiv.org API based on user-provided keywords and return the PDF versions of the most recent research papers. or the user can upload their own pdfs.

2. **Document Processing:** In the second part, ARtiBot loads the PDFs, splits them into manageable chunks, and converts them into vector representations for storage using Faiss for fast retrieval.

3. **Interactive Chatbot:** The third part creates an interactive chatbot using Streamlit, leveraging OpenAI's ChatOpenAI() model to query the stored documents and provide users with research-specific answers.

## Technologies Used

- Python scripting
- arXiv API for paper downloads
- PyPDF2 for reading uploaded pdfs documents
- Langchain for document loading and chunking
- Faiss for document vectorization and storage
- Streamlit for the chatbot interface
- CSS for custom formatting

## What's Next for ARtiBot

I have ambitious plans to enhance ARtiBot's capabilities and usability further:

1. **Improved PDF loading:** Make the PDF loading process more intuitive and offer additional options for keyword selection and time of query.

2. **Scale to a Larger Corpus:** Expand the research paper corpus to provide access to a more extensive collection of papers.

3. **API Timeout Handling:** Address API call timeout issues with the arXiv API to ensure smooth performance.

4. **Explore Different LLMs:** Experiment with other Large Language Models, such as those available from HuggingFace.

5. **Conversational Memory and Agents:** Implement conversational memory and agents to enhance the chatbot's interactions and responses.

## Getting Started
To run ARtiBot, follow these steps:
1. **Install Required Libraries:** Start by installing the necessary Python libraries. You can find a list of these libraries in the `requirements.txt` file. Use the following command to install them:

    ```bash
    pip install -r requirements.txt
    ```
2. **Configure OpenAI API Key:**
   - Inside the `.env` file, add your OpenAI API key as follows:
   
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

3. **Run ARtiBot:** In your terminal, execute the ARtiBot application using Streamlit with the following command:

    ```bash
    streamlit run arxiv_bot.py
    ```

   Please note that if you encounter any issues with library dependencies, you can create a virtual environment for the project. Follow these steps:

   - **Create a Virtual Environment:** Run the following command to create a new virtual environment (replace `<virtual-environment-name>` with your desired name):

     ```bash
     python -m venv <virtual-environment-name>
     ```

   - **Activate the Virtual Environment:** Activate the virtual environment using the appropriate command for your operating system. For example, on Windows:

     ```bash
     .\<virtual-environment-name>\Scripts\activate
     ```

     And on macOS/Linux:

     ```bash
     source <virtual-environment-name>/bin/activate
     ```

   - After activating the virtual environment, proceed to install the required libraries using the `pip install -r requirements.txt` command mentioned in step 1.

By following these steps, you'll have ARtiBot up and running, ready to assist you with your research needs.

