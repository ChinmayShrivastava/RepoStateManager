class MyMultipleNegativesRankingLoss(nn.Module):
    """Multiple negatives ranking loss.

    This loss is similar to the one in sentence_transformers,
    but optimized for our own embeddings.

    """

    def __init__(
        self,
        model: BaseAdapter,
        scale: float = 20.0,
        similarity_fct: Optional[Callable] = None,
    ):
        """Define ranking loss."""
        super().__init__()
        self.model = model
        self.scale = scale
        self.similarity_fct = cos_sim if similarity_fct is None else similarity_fct
        self.cross_entropy_loss = nn.CrossEntropyLoss()

    def forward(self, query_embeds: Tensor, context_embeds: Tensor) -> Tensor:
        """Forward pass."""
        # transform context embeds
        # context_embeds_2 = self.model.forward(context_embeds)
        query_embeds_2 = self.model.forward(query_embeds)

        scores = self.similarity_fct(query_embeds_2, context_embeds) * self.scale
        labels = torch.tensor(
            range(len(scores)), dtype=torch.long, device=scores.device
        )
        return self.cross_entropy_loss(scores, labels)
