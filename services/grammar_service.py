import language_tool_python

tool = language_tool_python.LanguageTool('en-US',config={
            'cacheSize': 1000,
            'pipelineCaching': True
        })
tool.enable_spellchecking()

def grammar_check(text):
    matches = tool.check(text)

    corrected_text = language_tool_python.utils.correct(text, matches)

    highlighted_text = text
    offset_adjustment = 0

    for match in matches:
        start = match.offset + offset_adjustment
        end = start + match.error_length  # ✅ FIXED

        incorrect_word = highlighted_text[start:end]

        suggestion = match.replacements[0] if match.replacements else ""

        highlighted_version = (
            f'<span class="text-red-500 underline decoration-2 cursor-pointer" '
            f'title="Suggestion: {suggestion}">'
            f'{incorrect_word}</span>'
        )

        highlighted_text = (
            highlighted_text[:start] +
            highlighted_version +
            highlighted_text[end:]
        )

        offset_adjustment += len(highlighted_version) - len(incorrect_word)

    return highlighted_text, corrected_text, len(matches)