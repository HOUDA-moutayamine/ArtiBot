import streamlit as st  # Importer la bibliothèque Streamlit pour la création de l'interface utilisateur.
from dotenv import load_dotenv  # Importer la bibliothèque dotenv pour charger les variables d'environnement.
from PyPDF2 import PdfReader  # Importer la bibliothèque PyPDF2 pour la manipulation de fichiers PDF.
from langchain.document_loaders import PyMuPDFLoader  # Importer un composant de Langchain pour charger des documents PDF.
from langchain.text_splitter import CharacterTextSplitter  # Importer un composant de Langchain pour diviser le texte.
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings  # Importer des composants de Langchain pour les embeddings.
from langchain.vectorstores import FAISS  # Importer un composant de Langchain pour le stockage des vecteurs.
from langchain.chat_models import ChatOpenAI  # Importer un modèle de chat de Langchain.
from langchain.memory import ConversationBufferMemory  # Importer un composant de Langchain pour la mémoire de la conversation.
from langchain.chains import ConversationalRetrievalChain  # Importer un composant de Langchain pour la chaîne de conversation.
import arxiv  # Importer la bibliothèque ArXiv pour la recherche d'articles.
import os  # Importer la bibliothèque os pour les opérations liées au système d'exploitation.
import re  # Importer la bibliothèque re pour les expressions régulières.
from streamlit_chat import message  # Importer un composant Streamlit pour les messages dans le chat.
from PIL import Image  # Importer la bibliothèque Pillow pour la manipulation d'images.

# Définir une fonction pour extraire le texte à partir de fichiers PDF.
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Définir une fonction pour récupérer les données ArXiv en fonction de la question de l'utilisateur.
def  get_arxiv_data(content):
    # Effectuer une recherche sur ArXiv en utilisant la requête 'content'.
    search = arxiv.Search(
        query= content ,
        max_results=1, # Limite les résultats à un seul document.
        sort_by=arxiv.SortCriterion.Relevance, # Trie les résultats par pertinence.
    )
    pdf_data= ''
    source= ''
    # Parcourir les résultats de la recherche.
    for result in search.results():
         # Charger le PDF à partir de l'URL du résultat en utilisant PyMuPDFLoader.
        loader = PyMuPDFLoader(result.pdf_url)
        loaded_pdf = loader.load()
        doc_data = ''
        # Parcourir les pages du PDF et extraire le contenu textuel de chaque page.
        for document in loaded_pdf:
            document.metadata["source"] = result.entry_id  # Ajouter la source au métadonnées du document.
            document.metadata["file_path"] = result.pdf_url  # Ajouter le chemin du fichier PDF au métadonnées.
            document.metadata["title"] = result.title  # Ajouter le titre au métadonnées.
            doc_data += document.page_content  # Ajouter le contenu de la page au texte du document.

        pdf_data += doc_data  # Ajouter le texte du document au texte global extrait des PDF.
        source += "\n" + result.pdf_url  # Ajouter l'URL du document à la liste des sources.

    # Retourne le texte extrait des PDF et la liste des sources.
    return pdf_data, source

# Définir une fonction pour diviser le texte en morceaux.
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Définir une fonction pour créer un vectorstore à partir des morceaux de texte.
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(disallowed_special=(),)
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Définir une fonction pour créer une chaîne de conversation.
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Fonction pour traiter les données ArXiv en fonction de la question de l'utilisateur.
def process_arxiv_data(user_question):
    content = user_question  # Utilisez la question de l'utilisateur comme requête de recherche ArXiv
    pdf_data, source = get_arxiv_data(content)
    
    text_chunks = get_text_chunks(pdf_data)
    vectorstore = get_vectorstore(text_chunks)
    st.session_state.conversation = get_conversation_chain(vectorstore)
    return source

# Fonction pour traiter les PDF téléchargés
def process_uploaded_pdfs(pdf_docs):
    with st.spinner("Processing"):
        # Obtenez le texte PDF
        raw_text = get_pdf_text(pdf_docs)

        # Obtenez les morceaux de texte
        text_chunks = get_text_chunks(raw_text)

        # Créez le vectorstore
        vectorstore = get_vectorstore(text_chunks)

        # Créez la chaîne de conversation
        st.session_state.conversation = get_conversation_chain(vectorstore)

# Fonction pour gérer l'interaction de l'utilisateur et les réponses du chatbot.
def handle_userinput(user_question, source):
    response = st.session_state.conversation({'question': user_question})  # Obtenir la réponse du chatbot.
    if "generated" not in st.session_state:  # Vérifier si la clé "generated" n'existe pas dans la session.
        st.session_state["generated"] = []  # Créer une liste vide "generated" dans la session.

    if "past" not in st.session_state:  # Vérifier si la clé "past" n'existe pas dans la session.
        st.session_state["past"] = []  # Créer une liste vide "past" dans la session.

    st.session_state.past.append(response["question"])  # Ajouter la question de l'utilisateur à la liste "past".
    st.session_state.generated.append(response["answer"] + "\n" + source)  # Ajouter la réponse du chatbot et la source à la liste "generated".


    if st.session_state["generated"]:

        for i in range(len(st.session_state["generated"]) - 1, -1, -1):

            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user", \
                    avatar_style="lorelei", seed=123)  # Afficher le message de l'utilisateur dans le chat.
            message(st.session_state["generated"][i], key=str(i), avatar_style="bottts", \
                    seed=123)  # Afficher la réponse du chatbot dans le chat.
               

def main():
    load_dotenv()
    st.set_page_config(page_title="Ask ArXiv", page_icon=":books:", layout="wide")

    app_title = '<p style="font-family:sans-serif; color:White; \
        text-align: center; font-size: 62px;">🧑‍🔬Ask ArXiv 🧑‍💻</p>'

    st.markdown(app_title, unsafe_allow_html=True)

    if "conversation" not in st.session_state:  # Vérifier si la clé "conversation" n'existe pas dans la session.
        st.session_state.conversation = None  # Initialiser "conversation" à None.

    if "chat_history" not in st.session_state:  # Vérifier si la clé "chat_history" n'existe pas dans la session.
        st.session_state.chat_history = None  # Initialiser "chat_history" à None.

    user_question = st.text_input("Ask a question:")  # Entrée utilisateur pour poser une question.
    if user_question :
        source = process_arxiv_data(user_question)  # Obtenir la source des données ArXiv en fonction de la question de l'utilisateur.


    with st.sidebar.container():
        left_co, cent_co,last_co = st.columns(3)
        with left_co:
            image = Image.open("artibot.png")
            image = image.resize((90, 70))
            st.image(image)
        with cent_co:
            st.header("ARTIBOT 🧑‍🔬")
        st.write("\n")
        pdf_docs = st.file_uploader(
            "", accept_multiple_files=True) # Téléchargement de fichiers PDF par l'utilisateur.
        if st.button("Process"):
            process_uploaded_pdfs(pdf_docs)
            source= ''
    if user_question:
        handle_userinput(user_question,source)
    
        
# Fonction principale pour exécuter l'application.
if __name__ == '__main__':
    main()