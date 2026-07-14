import streamlit as st
from rag import create_vector_store, ask_question

st.title("📚 Document Q&A Chatbot")

# Store vector database
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# Upload PDF
pdf = st.file_uploader("Upload PDF", type="pdf")

if pdf:

    # Save uploaded file
    with open("uploaded_pdf.pdf", "wb") as f:
        f.write(pdf.getbuffer())

    if st.button("Process PDF"):

        with st.spinner("Creating knowledge base..."):

            st.session_state.vector_store = create_vector_store(
                "uploaded_pdf.pdf"
            )

        st.success("PDF processed successfully!")

# Ask Question
question = st.text_input("Ask a question from your PDF")

if st.button("Ask"):

    if st.session_state.vector_store:

        with st.spinner("Searching document..."):

            answer = ask_question(
                st.session_state.vector_store,
                question
            )

        st.subheader("Answer")
        st.write(answer)

    else:
        st.warning("Please upload and process a PDF first.")