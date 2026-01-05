"""
Immaculacy Guardian Fork — Output Purity Deliberator
Prevents placeholders, ensures full 1-shot code, mobile seamless
"""

class ImmaculacyGuardianFork:
    name = "Immaculacy Guardian"
    
    def deliberate(self, proposal: dict) -> dict:
        output = proposal.get("generated_output", "")
        issues = []
        
        if "# ... previous" in output or "previous imports" in output.lower():
            issues.append("Placeholder detected — violation of 1-shot law")
        
        if "add" in output.lower() or "append" in output.lower():
            issues.append("Manual edit forced — mobile friction")
        
        if issues:
            vote = "NO"
            insight = f"Glitch prevention: {issues} — redirect to full complete code."
        else:
            vote = "YES"
            insight = "Output immaculate — full 1-shot compliant, thriving seamless."
        
        return {"vote": vote, "insight": insight, "issues": issues}
