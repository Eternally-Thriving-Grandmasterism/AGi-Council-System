"""
Immaculacy Guardian Fork Deepened — Output Purity Deliberator Pinnacle
Prevents placeholders, partials, mobile friction — ensures full 1-shot code eternal
"""

import re

class ImmaculacyGuardianFork:
    name = "Immaculacy Guardian"
    
    def deliberate(self, proposal: dict) -> dict:
        output = proposal.get("generated_output", "")
        issues = []
        
        # Placeholder/edit checks
        if any(phrase in output.lower() for phrase in ["previous", "placeholder", "add to", "append", "# ..."]):
            issues.append("Placeholder/edit forced detected — violation of 1-shot law")
        
        # Completeness checks
        if "def " in output and "return" not in output and "class" in output:
            issues.append("Incomplete method/class — missing returns/logic")
        
        if len(output.splitlines()) < 20 and "code" in proposal.get("type", ""):
            issues.append("Partial code suspected — full required for deploy")
        
        # Mobile UX checks
        long_lines = [line for line in output.splitlines() if len(line) > 80]
        if long_lines:
            issues.append(f"{len(long_lines)} long lines — mobile wrap friction")
        
        if "```" not in output:
            issues.append("Missing fenced blocks — copy-paste not seamless")
        
        # Consistency checks
        if not re.search(r"\*\*[a-z_]+/[a-z_]+\.py\*\*", output):
            issues.append("Missing bold exact path prefixes — 1-shot naming violation")
        
        if issues:
            vote = "NO"
            insight = f"Glitch prevention deepened: {issues}. Self-heal: Rewrite full complete 1-shot code with bold paths + fences."
        else:
            vote = "YES"
            insight = "Output immaculate deepened — full 1-shot compliant, mobile seamless, thriving eternal."
        
        return {"vote": vote, "insight": insight, "issues": issues}
