import os
import uuid
from unstructured.partition.pdf import partition_pdf
from langchain.schema.document import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore

def process_pdfs_brian(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    all_elements = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        raw_pdf_elements = partition_pdf(
            filename=pdf_path,
            extract_images_in_pdf=False,
            chunking_strategy="by_title",
            max_characters=500,
            new_after_n_chars=450,
            combine_text_under_n_chars=400,
            image_output_dir_path="."
        )
        all_elements.extend([{'title': pdf_file, 'contents': elements} for elements in raw_pdf_elements])
    return all_elements

def process_pdfs_gary(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    all_elements = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        raw_pdf_elements = partition_pdf(
            filename=pdf_path,
            extract_images_in_pdf=False,
            # infer_table_structure=True,
            #chunking_strategy="by_title",
            max_characters=500,
            new_after_n_chars=450,
            combine_text_under_n_chars=400,
            image_output_dir_path="."
        )

        all_elements.extend([{'title': pdf_file, 'contents': elements} for elements in raw_pdf_elements])
    return all_elements

def setup_vector_store(collection_name, model_name, id_key):
    embed_model = HuggingFaceEmbeddings(model_name=model_name)
    vectorstore = Chroma(collection_name=collection_name, embedding_function=embed_model)
    docstore = InMemoryStore()
    retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=docstore, id_key=id_key)
    return retriever

def add_documents_to_stores(retriever, elements):
    doc_ids = [str(uuid.uuid4()) for _ in elements]
    summary_elements = [
        Document(page_content=str(element['contents']), metadata={"doc_id": doc_ids[i], 'pdf_title': element['title']})
        for i, element in enumerate(elements)
    ]
    retriever.vectorstore.add_documents(summary_elements)
    retriever.docstore.mset(list(zip(doc_ids, elements)))
