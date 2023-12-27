    def compute_vectors(texts: List[str]) -> Tuple[List[List[int]], List[List[float]]]:
        """
        Computes vectors from logits and attention mask using ReLU, log, and max operations.
        """
        # TODO: compute sparse vectors in batches if max length is exceeded
        tokens = tokenizer(
            texts, truncation=True, padding=True, max_length=512, return_tensors="pt"
        )
        if torch.cuda.is_available():
            tokens = tokens.to("cuda")

        output = model(**tokens)
        logits, attention_mask = output.logits, tokens.attention_mask
        relu_log = torch.log(1 + torch.relu(logits))
        weighted_log = relu_log * attention_mask.unsqueeze(-1)
        tvecs, _ = torch.max(weighted_log, dim=1)

        # extract the vectors that are non-zero and their indices
        indices = []
        vecs = []
        for batch in tvecs:
            indices.append(batch.nonzero(as_tuple=True)[0].tolist())
            vecs.append(batch[indices[-1]].tolist())

        return indices, vecs