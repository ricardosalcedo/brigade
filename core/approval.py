"""Human approval system for automated actions"""

import json
from datetime import datetime
from typing import Any, Dict, List


class ApprovalManager:
    """Manages human approval for automated actions"""

    def __init__(self):
        self.pending_approvals = {}

    def request_pr_approval(
        self, file_path: str, fixes: List[Dict[str, Any]], analysis: Dict[str, Any]
    ) -> bool:
        """Request human approval for PR creation"""

        print("\n🎖️ BRIGADE PR Approval Required")
        print("=" * 50)

        # Show analysis summary
        print(f"📁 File: {file_path}")
        print(f"📊 Quality Score: {analysis.get('quality_score', 'N/A')}/10")
        print(f"🔧 Fixes Proposed: {len(fixes)}")

        # Show proposed fixes
        if fixes:
            print("🛠️ Proposed Fixes:")
            for i, fix in enumerate(fixes[:5], 1):
                issue_desc = fix.get(
                    "issue_description", fix.get("description", "Code improvement")
                )
                print(f"   {i}. {issue_desc}")

            if len(fixes) > 5:
                print(f"   ... and {len(fixes) - 5} more fixes")

        # Show quality improvement estimate
        if "quality_improvement" in analysis:
            print(
                f"\n📈 Expected Quality Improvement: {analysis['quality_improvement']}"
            )

        # Request approval
        print("❓ Approve PR creation for these fixes?")
        print("   This will create a pull request with the proposed changes.")

        while True:
            try:
                response = (
                    input("\n   [y]es / [n]o / [d]etails / [s]ave for later: ")
                    .lower()
                    .strip()
                )

                if response in ["y", "yes"]:
                    print("✅ PR creation approved")
                    return True
                elif response in ["n", "no"]:
                    print("❌ PR creation denied")
                    return False
                elif response in ["d", "details"]:
                    self._show_detailed_fixes(fixes, analysis)
                    continue
                elif response in ["s", "save"]:
                    self._save_for_later(file_path, fixes, analysis)
                    print("💾 Approval request saved for later review")
                    return False
                else:
                    print(
                        "   Please enter 'y' (yes), 'n' (no), 'd' (details), or 's' (save)"
                    )

            except KeyboardInterrupt:
                print("\n❌ Approval cancelled")
                return False

    def _show_detailed_fixes(
        self, fixes: List[Dict[str, Any]], analysis: Dict[str, Any]
    ):
        """Show detailed information about proposed fixes"""

        print("\n🔍 Detailed Fix Analysis:")
        print("-" * 40)

        for i, fix in enumerate(fixes, 1):
            print(f"\n{i}. {fix.get('issue_description', 'Code improvement')}")

            if "severity" in fix:
                severity = fix["severity"].upper()
                emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(severity, "⚪")
                print(f"   Severity: {emoji} {severity}")

            if "explanation" in fix:
                print(f"   Fix: {fix['explanation']}")

            if "original_code" in fix and "fixed_code" in fix:
                print(f"   Before: {fix['original_code'][:50]}...")
                print(f"   After:  {fix['fixed_code'][:50]}...")

        print("-" * 40)

    def _save_for_later(
        self, file_path: str, fixes: List[Dict[str, Any]], analysis: Dict[str, Any]
    ):
        """Save approval request for later review"""

        approval_id = f"approval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        approval_data = {
            "id": approval_id,
            "file_path": file_path,
            "fixes": fixes,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
        }

        # Save to file
        approval_file = f"pending_approvals.json"
        try:
            # Load existing approvals
            try:
                with open(approval_file, "r") as f:
                    approvals = json.load(f)
            except FileNotFoundError:
                approvals = []

            # Add new approval
            approvals.append(approval_data)

            # Save back
            with open(approval_file, "w") as f:
                json.dump(approvals, f, indent=2)

        except Exception as e:
            print(f"⚠️ Could not save approval: {e}")

    def list_pending_approvals(self) -> List[Dict[str, Any]]:
        """List all pending approvals"""

        try:
            with open("pending_approvals.json", "r") as f:
                approvals = json.load(f)
            return [a for a in approvals if a.get("status") == "pending"]
        except FileNotFoundError:
            return []

    def approve_saved_request(self, approval_id: str) -> bool:
        """Approve a previously saved request"""

        try:
            with open("pending_approvals.json", "r") as f:
                approvals = json.load(f)

            for approval in approvals:
                if approval["id"] == approval_id:
                    approval["status"] = "approved"
                    approval["approved_at"] = datetime.now().isoformat()

                    with open("pending_approvals.json", "w") as f:
                        json.dump(approvals, f, indent=2)

                    return True

            return False

        except Exception:
            return False
