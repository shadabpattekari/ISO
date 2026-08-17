"""
FaizZab ISO & DPDPA Toolkit Generator — Comprehensive Backend API Test Suite

Tests all endpoints including critical TENANT ISOLATION for downloads/orders/submissions.
"""
import requests
import sys
from datetime import datetime
from typing import Optional, Dict, Any

BASE_URL = "https://doc-composer-11.preview.emergentagent.com/api"

# Test credentials from /app/memory/test_credentials.md
ADMIN_EMAIL = "admin@faizzab.com"
ADMIN_PASSWORD = "Admin@12345"
ADMIN_MFA_CODE = "123456"
CLIENT_OTP_CODE = "654321"
COUPON_CODE = "LAUNCH20"


class FaizZabAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.admin_token: Optional[str] = None
        self.client1_token: Optional[str] = None
        self.client2_token: Optional[str] = None
        self.org1_id: Optional[str] = None
        self.org2_id: Optional[str] = None
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.critical_failures = []

    def log(self, msg: str, level: str = "INFO"):
        prefix = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}.get(level, "•")
        print(f"{prefix} {msg}")

    def test(self, name: str, method: str, endpoint: str, expected_status: int,
             token: Optional[str] = None, data: Optional[Dict] = None,
             critical: bool = False) -> tuple[bool, Any]:
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        self.tests_run += 1
        self.log(f"Testing {name}...", "INFO")

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                self.log(f"PASSED - {name} (status: {response.status_code})", "PASS")
            else:
                self.tests_failed += 1
                self.log(f"FAILED - {name} (expected {expected_status}, got {response.status_code})", "FAIL")
                if critical:
                    self.critical_failures.append(f"{name}: expected {expected_status}, got {response.status_code}")
                try:
                    self.log(f"Response: {response.text[:200]}", "WARN")
                except:
                    pass

            try:
                return success, response.json() if response.text else {}
            except:
                return success, {}

        except Exception as e:
            self.tests_failed += 1
            self.log(f"FAILED - {name}: {str(e)}", "FAIL")
            if critical:
                self.critical_failures.append(f"{name}: {str(e)}")
            return False, {}

    def run_all_tests(self):
        """Execute comprehensive test suite"""
        self.log("=" * 80, "INFO")
        self.log("FaizZab Backend API Test Suite", "INFO")
        self.log("=" * 80, "INFO")

        # 1. Public Catalogue Tests
        self.log("\n[1] PUBLIC CATALOGUE TESTS", "INFO")
        success, data = self.test("GET /catalogue", "GET", "catalogue", 200)
        if success:
            toolkits = data.get("toolkits", [])
            if len(toolkits) == 3:
                self.log(f"✓ Found 3 toolkits as expected", "PASS")
                self.tests_passed += 1
            else:
                self.log(f"✗ Expected 3 toolkits, found {len(toolkits)}", "FAIL")
                self.tests_failed += 1
            if toolkits and toolkits[0].get("price") == 4999:
                self.log(f"✓ Price is ₹4999 as expected", "PASS")
                self.tests_passed += 1
            else:
                self.log(f"✗ Price mismatch", "FAIL")
                self.tests_failed += 1

        success, data = self.test("GET /catalogue/doc-composer-11 (DPDPA)", "GET", "catalogue/dpdpa", 200)
        if success:
            if data.get("legal_disclaimer"):
                self.log(f"✓ DPDPA has legal disclaimer", "PASS")
                self.tests_passed += 1
            manifest = data.get("manifest", [])
            if len(manifest) > 20:
                self.log(f"✓ Manifest has {len(manifest)} documents", "PASS")
                self.tests_passed += 1

        # 2. Admin Authentication with MFA
        self.log("\n[2] ADMIN AUTHENTICATION (MFA)", "INFO")
        success, data = self.test("Admin login - MFA required", "POST", "auth/admin/login", 200,
                                   data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        if success and data.get("mfa_required"):
            self.log(f"✓ MFA required as expected", "PASS")
            self.tests_passed += 1

        success, data = self.test("Admin login - with MFA", "POST", "auth/admin/login", 200,
                                   data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD, "mfa_code": ADMIN_MFA_CODE},
                                   critical=True)
        if success:
            self.admin_token = data.get("token")
            if self.admin_token:
                self.log(f"✓ Admin token obtained", "PASS")
                self.tests_passed += 1

        # 3. Client OTP Authentication
        self.log("\n[3] CLIENT OTP AUTHENTICATION", "INFO")
        mobile1 = f"9999{datetime.now().strftime('%H%M%S')}"
        mobile2 = f"8888{datetime.now().strftime('%H%M%S')}"

        success, data = self.test("Client OTP request", "POST", "auth/otp/request", 200,
                                   data={"mobile": mobile1, "name": "Test Client 1"})
        if success and data.get("dev_otp") == CLIENT_OTP_CODE:
            self.log(f"✓ OTP code is {CLIENT_OTP_CODE} (simulated)", "PASS")
            self.tests_passed += 1

        success, data = self.test("Client OTP verify", "POST", "auth/otp/verify", 200,
                                   data={"mobile": mobile1, "code": CLIENT_OTP_CODE, "name": "Test Client 1"},
                                   critical=True)
        if success:
            self.client1_token = data.get("token")
            if self.client1_token:
                self.log(f"✓ Client 1 token obtained", "PASS")
                self.tests_passed += 1

        # Create second client for tenant isolation tests
        success, data = self.test("Client 2 OTP request", "POST", "auth/otp/request", 200,
                                   data={"mobile": mobile2, "name": "Test Client 2"})
        success, data = self.test("Client 2 OTP verify", "POST", "auth/otp/verify", 200,
                                   data={"mobile": mobile2, "code": CLIENT_OTP_CODE, "name": "Test Client 2"})
        if success:
            self.client2_token = data.get("token")

        # 4. Organization Management
        self.log("\n[4] ORGANIZATION MANAGEMENT", "INFO")
        org1_data = {
            "legal_name": "Test Org Alpha Pvt Ltd",
            "trade_name": "Alpha",
            "website": "alpha.test",
            "industry": "SaaS",
            "employee_count": "25",
            "registered_address": "123 Test Street, Bangalore",
            "locations": "Bangalore, Mumbai",
            "primary_contact": "Alpha Admin",
            "contact_email": "admin@alpha.test",
            "contact_mobile": mobile1,
            "products_services": "SaaS analytics platform"
        }
        success, data = self.test("Create Organization 1", "POST", "org", 200,
                                   token=self.client1_token, data=org1_data, critical=True)
        if success:
            self.org1_id = data.get("id")
            self.log(f"✓ Org 1 created: {self.org1_id}", "PASS")
            self.tests_passed += 1

        success, data = self.test("GET Organization 1", "GET", "org", 200, token=self.client1_token)
        if success and data.get("legal_name") == org1_data["legal_name"]:
            self.log(f"✓ Org 1 retrieved correctly", "PASS")
            self.tests_passed += 1

        # Create org 2 for tenant isolation
        org2_data = org1_data.copy()
        org2_data["legal_name"] = "Test Org Beta Pvt Ltd"
        org2_data["trade_name"] = "Beta"
        org2_data["contact_mobile"] = mobile2
        success, data = self.test("Create Organization 2", "POST", "org", 200,
                                   token=self.client2_token, data=org2_data)
        if success:
            self.org2_id = data.get("id")

        # 5. Coupon Validation
        self.log("\n[5] COUPON VALIDATION", "INFO")
        success, data = self.test("Validate LAUNCH20 coupon", "POST", "coupons/validate", 200,
                                   data={"code": COUPON_CODE})
        if success and data.get("percent_off") == 20:
            self.log(f"✓ LAUNCH20 gives 20% off", "PASS")
            self.tests_passed += 1

        # 6. Order + Payment Flow
        self.log("\n[6] ORDER + PAYMENT FLOW", "INFO")
        success, data = self.test("Create order with coupon", "POST", "orders", 200,
                                   token=self.client1_token,
                                   data={"standard_slug": "dpdpa", "coupon": COUPON_CODE},
                                   critical=True)
        order1_id = None
        if success:
            order1_id = data.get("id")
            amount = data.get("amount")
            breakdown = data.get("price_breakdown", {})
            self.log(f"✓ Order created: {order1_id}, amount: ₹{amount}", "PASS")
            if breakdown.get("discount") > 0:
                self.log(f"✓ Discount applied: ₹{breakdown.get('discount')}", "PASS")
                self.tests_passed += 1

        if order1_id:
            success, data = self.test("Verify payment (server-side)", "POST",
                                       f"orders/{order1_id}/verify-payment", 200,
                                       token=self.client1_token,
                                       data={"razorpay_payment_id": "sim_test_payment"},
                                       critical=True)
            if success:
                if data.get("status") == "paid":
                    self.log(f"✓ Payment verified", "PASS")
                    self.tests_passed += 1
                if data.get("entitlement"):
                    self.log(f"✓ Entitlement granted", "PASS")
                    self.tests_passed += 1
                if data.get("invoice"):
                    self.log(f"✓ Invoice generated", "PASS")
                    self.tests_passed += 1

        success, data = self.test("List orders", "GET", "orders", 200, token=self.client1_token)
        if success and len(data) > 0:
            self.log(f"✓ Orders list retrieved ({len(data)} orders)", "PASS")
            self.tests_passed += 1

        success, data = self.test("List entitlements", "GET", "entitlements", 200, token=self.client1_token)
        if success and len(data) > 0:
            self.log(f"✓ Entitlements retrieved", "PASS")
            self.tests_passed += 1

        # 7. Onboarding Flow
        self.log("\n[7] ONBOARDING FLOW", "INFO")
        success, data = self.test("GET onboarding schema", "GET", "onboarding/schema/dpdpa", 200)
        if success:
            sections = data.get("sections", [])
            if len(sections) >= 9:
                self.log(f"✓ Schema has {len(sections)} sections (A-I)", "PASS")
                self.tests_passed += 1

        # Minimal answers for required fields
        answers = {
            "legal_name": "Test Org Alpha Pvt Ltd",
            "trade_name": "Alpha",
            "registered_address": "123 Test Street",
            "locations": "Bangalore",
            "employee_count": "25",
            "primary_contact": "Alpha Admin",
            "contact_email": "admin@alpha.test",
            "contact_mobile": mobile1,
            "industry": "SaaS",
            "products_services": "Analytics platform",
            "top_management": "CEO Alpha",
            "ms_coordinator": "Coordinator Alpha",
            "internal_auditor": "Auditor Alpha",
            "included_services": "Analytics platform",
            "included_locations": "Bangalore",
            "processes": ["Sales", "IT", "Support"],
            "uses_cloud": True,
            "remote_work": True,
            "jurisdiction": "India",
            "processes_personal_data": True,
            "data_categories": "Name, email, phone",
            "processes_children": False,
            "uses_processors": True,
            "brand_color": "#1F3A5F",
            "classification": "Confidential",
            "version": "1.0",
            "effective_date": "01 Feb 2026",
            "review_date": "01 Feb 2027",
            "prepared_by": "Test Preparer",
            "reviewed_by": "Test Reviewer",
            "approved_by": "Test Approver",
        }

        success, data = self.test("Save onboarding draft", "POST", "onboarding/draft", 200,
                                   token=self.client1_token,
                                   data={"standard_slug": "dpdpa", "answers": answers})
        if success:
            completion = data.get("completion", 0)
            self.log(f"✓ Draft saved, completion: {completion}%", "PASS")
            self.tests_passed += 1

        success, data = self.test("Submit onboarding", "POST", "onboarding/submit", 200,
                                   token=self.client1_token,
                                   data={"standard_slug": "dpdpa", "answers": answers, "declaration": True},
                                   critical=True)
        submission1_id = None
        if success:
            submission1_id = data.get("id")
            status = data.get("status")
            if status == "submitted":
                self.log(f"✓ Onboarding submitted: {submission1_id}", "PASS")
                self.tests_passed += 1

        # 8. Admin Verification Workflow
        self.log("\n[8] ADMIN VERIFICATION WORKFLOW", "INFO")
        success, data = self.test("Admin: list reviews", "GET", "admin/reviews", 200,
                                   token=self.admin_token, critical=True)
        if success and len(data) > 0:
            self.log(f"✓ Review queue has {len(data)} submissions", "PASS")
            self.tests_passed += 1

        if submission1_id:
            success, data = self.test("Admin: get review detail", "GET",
                                       f"admin/reviews/{submission1_id}", 200,
                                       token=self.admin_token)
            if success:
                self.log(f"✓ Review detail retrieved", "PASS")
                self.tests_passed += 1

            success, data = self.test("Admin: add comment", "POST",
                                       f"admin/reviews/{submission1_id}/comment", 200,
                                       token=self.admin_token,
                                       data={"comment": "Test comment", "section_id": "A"})

            success, data = self.test("Admin: approve submission", "POST",
                                       f"admin/reviews/{submission1_id}/approve", 200,
                                       token=self.admin_token, critical=True)
            if success and data.get("status") == "approved":
                self.log(f"✓ Submission approved", "PASS")
                self.tests_passed += 1

        # 9. Document Generation
        self.log("\n[9] DOCUMENT GENERATION", "INFO")
        if submission1_id:
            success, data = self.test("Admin: generate documents", "POST",
                                       f"admin/generate/{submission1_id}", 200,
                                       token=self.admin_token, critical=True)
            if success:
                status = data.get("status")
                count = data.get("artifact_count", 0)
                zip_id = data.get("zip_id")
                if status == "generated":
                    self.log(f"✓ Documents generated: {count} artifacts", "PASS")
                    self.tests_passed += 1
                if count >= 20:
                    self.log(f"✓ Generated {count} documents (expected ~26)", "PASS")
                    self.tests_passed += 1
                if zip_id:
                    self.log(f"✓ ZIP package created: {zip_id}", "PASS")
                    self.tests_passed += 1

            success, data = self.test("Admin: publish documents", "POST",
                                       f"admin/publish/{submission1_id}", 200,
                                       token=self.admin_token)
            if success and data.get("status") == "published":
                self.log(f"✓ Documents published", "PASS")
                self.tests_passed += 1

        # 10. Downloads (with TENANT ISOLATION test)
        self.log("\n[10] DOWNLOADS & TENANT ISOLATION (CRITICAL)", "INFO")
        success, data = self.test("Client 1: list downloads", "GET", "downloads", 200,
                                   token=self.client1_token, critical=True)
        artifact1_id = None
        if success:
            docs = data.get("documents", [])
            if len(docs) > 0:
                self.log(f"✓ Client 1 can see {len(docs)} documents", "PASS")
                self.tests_passed += 1
                artifact1_id = docs[0].get("id")
                # Check for ZIP
                zip_docs = [d for d in docs if d.get("format") == "zip"]
                if zip_docs:
                    self.log(f"✓ ZIP package present in downloads", "PASS")
                    self.tests_passed += 1

        # CRITICAL: Tenant isolation test
        if artifact1_id and self.client2_token:
            self.log("🔒 TESTING TENANT ISOLATION (Client 2 tries to access Client 1's artifact)...", "INFO")
            success, data = self.test("TENANT ISOLATION: Client 2 access Client 1 artifact", "GET",
                                       f"downloads/{artifact1_id}", 403,
                                       token=self.client2_token, critical=True)
            if success:
                self.log(f"✓ TENANT ISOLATION WORKING: Client 2 got 403 Forbidden", "PASS")
                self.tests_passed += 1
            else:
                self.log(f"✗ CRITICAL: TENANT ISOLATION BREACH! Client 2 could access Client 1's artifact", "FAIL")
                self.critical_failures.append("TENANT ISOLATION BREACH: Client 2 accessed Client 1's artifact")

        # Client 1 should be able to download their own artifact
        if artifact1_id:
            success, data = self.test("Client 1: download own artifact", "GET",
                                       f"downloads/{artifact1_id}", 200,
                                       token=self.client1_token)
            if success:
                self.log(f"✓ Client 1 can download own artifact", "PASS")
                self.tests_passed += 1

        # 11. Additional Requirements Flow
        self.log("\n[11] ADDITIONAL REQUIREMENTS FLOW", "INFO")
        success, data = self.test("Client: create additional requirement", "POST",
                                   "additional-requirements", 200,
                                   token=self.client1_token,
                                   data={"title": "Custom policy", "description": "Need custom policy",
                                         "category": "Policy"})
        req_id = None
        if success:
            req_id = data.get("id")
            self.log(f"✓ Additional requirement created: {req_id}", "PASS")
            self.tests_passed += 1

        if req_id:
            success, data = self.test("Admin: quote additional requirement", "POST",
                                       f"admin/additional-requirements/{req_id}/quote", 200,
                                       token=self.admin_token,
                                       data={"amount": 2999, "description": "Custom policy development"})
            if success and data.get("status") == "quoted":
                self.log(f"✓ Quotation created", "PASS")
                self.tests_passed += 1

            success, data = self.test("Client: accept quotation", "POST",
                                       f"additional-requirements/{req_id}/respond", 200,
                                       token=self.client1_token,
                                       data={"accept": True})
            if success and data.get("status") == "accepted":
                self.log(f"✓ Quotation accepted", "PASS")
                self.tests_passed += 1

        # 12. Admin Dashboards
        self.log("\n[12] ADMIN DASHBOARDS", "INFO")
        dashboards = [
            ("Executive", "admin/dashboard/executive"),
            ("Commerce", "admin/dashboard/commerce"),
            ("Content", "admin/dashboard/content"),
        ]
        for name, endpoint in dashboards:
            success, data = self.test(f"Admin: {name} dashboard", "GET", endpoint, 200,
                                       token=self.admin_token)
            if success:
                self.log(f"✓ {name} dashboard loaded", "PASS")
                self.tests_passed += 1

        success, data = self.test("Admin: list clients", "GET", "admin/clients", 200,
                                   token=self.admin_token)
        if success and len(data) >= 2:
            self.log(f"✓ Clients list retrieved ({len(data)} clients)", "PASS")
            self.tests_passed += 1

        success, data = self.test("Admin: audit logs", "GET", "admin/audit-logs", 200,
                                   token=self.admin_token)
        if success and len(data) > 0:
            self.log(f"✓ Audit logs retrieved ({len(data)} entries)", "PASS")
            self.tests_passed += 1

        # 13. Health Check
        self.log("\n[13] HEALTH CHECK", "INFO")
        success, data = self.test("Health check", "GET", "health", 200)
        if success and data.get("status") == "ok":
            self.log(f"✓ Health check passed", "PASS")
            self.tests_passed += 1

    def print_summary(self):
        """Print test summary"""
        self.log("\n" + "=" * 80, "INFO")
        self.log("TEST SUMMARY", "INFO")
        self.log("=" * 80, "INFO")
        self.log(f"Total tests run: {self.tests_run}", "INFO")
        self.log(f"Tests passed: {self.tests_passed}", "PASS")
        self.log(f"Tests failed: {self.tests_failed}", "FAIL")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        self.log(f"Success rate: {success_rate:.1f}%", "INFO")

        if self.critical_failures:
            self.log("\n⚠️  CRITICAL FAILURES:", "FAIL")
            for failure in self.critical_failures:
                self.log(f"  • {failure}", "FAIL")
            return 1
        elif self.tests_failed > 0:
            self.log("\n⚠️  Some tests failed but no critical failures", "WARN")
            return 1
        else:
            self.log("\n🎉 All tests passed!", "PASS")
            return 0


def main():
    tester = FaizZabAPITester()
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        tester.log("\n\nTests interrupted by user", "WARN")
    except Exception as e:
        tester.log(f"\n\nUnexpected error: {str(e)}", "FAIL")
        import traceback
        traceback.print_exc()
    finally:
        return_code = tester.print_summary()
        sys.exit(return_code)


if __name__ == "__main__":
    main()
