def chat_message_to_gemini(message: ChatMessage) -> "genai.types.ContentDict":
    """Convert ChatMessages to Gemini-specific history, including ImageDocuments."""
    parts = [message.content]
    if images := message.additional_kwargs.get("images"):
        try:
            import PIL

            parts += [PIL.Image.open(doc.resolve_image()) for doc in images]
        except ImportError:
            # This should have been caught earlier, but tell the user anyway.
            raise ValueError("Multi-modal support requires PIL.")

    return {
        "role": ROLES_TO_GEMINI[message.role],
        "parts": parts,
    }
