import re


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "did",
    "do",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "the",
    "to",
    "used",
    "was",
    "were",
    "what",
    "who",
    "why",
    "with",
}


class EvidenceChecker:

    def _tokenize(self, text):

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower(),
        )

        return {
            word
            for word in words
            if word not in STOP_WORDS
            and len(word) > 2
        }


    def is_supported(self, question, context):

        question_words = self._tokenize(
            question
        )

        context_words = self._tokenize(
            context
        )

        overlapping_words = (
            question_words
            & context_words
        )

        if not question_words:

            return False


        overlap_ratio = (
            len(overlapping_words)
            / len(question_words)
        )


        # Require at least two meaningful
        # question terms to appear in context.

        if len(overlapping_words) >= 2:

            return True


        # Allow a single strong overlap only when
        # most of the question's meaningful terms
        # are represented.

        if overlap_ratio >= 0.5:

            return True


        return False