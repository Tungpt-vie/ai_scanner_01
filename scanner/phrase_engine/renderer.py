from scanner.event_generator.schema import TAEvent
from scanner.phrase_engine.templates import TEMPLATES
from scanner.phrase_engine.mapping import PHRASE_MAPPING
from scanner.phrase_engine.lint import PhraseLint


class PhraseRenderer:
    """
    Deterministic render-only phrase engine.

    - No CTA
    - No advisory tone
    - Must pass lint
    - Silent DROP on violation
    """

    def __init__(self):
        self.lint = PhraseLint()

    def render(self, event: TAEvent) -> str | None:
        """
        Render event into descriptive text.
        Return None if lint fails.
        """

        lines = []

        # 1️⃣ Base structure
        base_line = TEMPLATES["BASE_STRUCTURE"].format(
            symbol=event.symbol,
            regime=event.regime,
            ta_state=event.ta_state,
        )
        lines.append(base_line)

        # 2️⃣ Regime phrase
        regime_key = f"REGIME_{event.regime}"
        if regime_key in TEMPLATES:
            lines.append(TEMPLATES[regime_key])

        # 3️⃣ Pattern-driven phrases (measurement-based mapping)
        measurements = event.measurements

        rsi = measurements.get("rsi")
        volume_ratio = measurements.get("volume_ratio")
        structure_age = measurements.get("structure_age")

        if rsi is not None:
            if rsi > 70:
                lines.append(TEMPLATES["RSI_HIGH"])
            elif rsi < 30:
                lines.append(TEMPLATES["RSI_LOW"])

        if volume_ratio is not None:
            if volume_ratio > 1.5:
                lines.append(TEMPLATES["VOLUME_EXPANSION"])
            elif volume_ratio < 0.7:
                lines.append(TEMPLATES["VOLUME_CONTRACTION"])

        if structure_age is not None:
            if structure_age < 3:
                lines.append(TEMPLATES["STRUCTURE_FRESH"])
            else:
                lines.append(TEMPLATES["STRUCTURE_MATURE"])

        # 4️⃣ Footer
        lines.append(TEMPLATES["FOOTER"])

        final_text = "\n".join(lines)

        # 5️⃣ Lint validation
        if not self.lint.validate(final_text):
            return None

        return final_text
