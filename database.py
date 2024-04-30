from pre_data import process_pdfs, add_documents_to_stores

def search_documents(retriever, prompt, database_choices):
    pdf_elements = process_pdfs(f"./{database_choices}")
    add_documents_to_stores(retriever, pdf_elements)

    query_results = retriever.vectorstore.similarity_search_with_score(prompt)
    if not query_results:
        return "No relevant documents found."

    res = "Related information:\n\n"
    for index, (doc, score) in enumerate(query_results[:3], start=1):
        doc_info = (
            f"第 {index} 筆資料\n\n"
            f"內容: {doc.page_content}\n\n"
            f"文件標題: {doc.metadata.get('pdf_title')}\n\n"
            f"文件 ID: {doc.metadata.get('doc_id')}\n\n"
            f"相似度分數: {score:.2f}\n\n"
            "-------------\n"
        )
        res += doc_info
    return res