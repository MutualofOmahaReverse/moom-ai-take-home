"""
Prompt construction for the classification and extraction services.

All prompt text lives here so that it is in one place and can be adjusted
without touching the service code. Prompts are built as f-strings with the
document content interpolated directly.
"""

# The document types the classifier is allowed to return. If you add one here
# you should also add it to the checklist_item table, otherwise the missing-doc
# report will not know about it.
DOC_TYPES = [
    "pay_stub",
    "w2",
    "bank_statement",
    "photo_id",
    "homeowners_insurance",
    "property_tax_bill",
    "counseling_certificate",
    "letter_of_explanation",
    "other",
]


def build_classification_prompt(filename: str, content: str) -> str:
    """Build the full classification prompt for a single document.

    The prompt includes the list of allowed types, a description of each one,
    several worked examples, formatting instructions, and finally the document
    itself. It is returned as a single string ready to be sent as a user turn.
    """
    return f"""You are a document classification assistant working for a mortgage lender.
Your job is to look at a document that has been uploaded to a loan file and decide
what kind of document it is.

Here are the document types you are allowed to choose from. You must choose exactly
one of these. Do not invent new types. Do not return a type that is not on this list.

1. pay_stub - A pay stub, earnings statement, or paycheck record from an employer.
   These usually have an employer name, an employee name, a pay period, a gross
   amount and a net amount. Sometimes they have year-to-date figures as well.
   Common headers include "Earnings Statement", "Payroll", "Pay Stub".

2. w2 - A W-2 Wage and Tax Statement. This is an annual tax form. It will usually
   say "Form W-2" or "W-2 Wage and Tax Statement" somewhere on it and will have a
   tax year. It has wages, tips, other compensation, and federal income tax
   withheld. Do not confuse this with a pay stub. A W-2 is annual, a pay stub is
   per pay period.

3. bank_statement - A statement from a bank or credit union showing account
   activity. Will usually have an institution name, a statement period, an account
   number (often masked), and a balance. Sometimes there is a beginning balance and
   an ending balance.

4. photo_id - A driver license, state identification card, or passport. Will have
   a name and usually a date of birth. Driver licenses have a state name on them.

5. homeowners_insurance - A homeowners insurance policy, declarations page, or
   dwelling fire policy. Will have a policy number, a coverage amount, and usually
   a premium and an effective date range.

6. property_tax_bill - A property tax bill or statement from a county or municipal
   authority. Will have a parcel number or PIN, and an amount due.

7. counseling_certificate - A HECM or reverse mortgage counseling certificate.
   Will name a counseling agency and a completion date. HUD-approved counseling is
   required before a reverse mortgage application can proceed.

8. letter_of_explanation - A letter written by the borrower explaining something
   about their circumstances, such as a gap in employment or a large deposit.

9. other - Anything that does not fit one of the above categories.

Here are some examples to guide you.

EXAMPLE 1
Filename: scan_0044.pdf
Content: "ACME PAYROLL SERVICES Employee: J SMITH Pay Period: 01/01/2026 - 01/15/2026 Gross Pay: 2,400.00"
Correct answer: pay_stub

EXAMPLE 2
Filename: doc.pdf
Content: "Form W-2 Wage and Tax Statement 2025 Employee JANE DOE Wages tips other comp 88,000.00"
Correct answer: w2

EXAMPLE 3
Filename: IMG_0012.jpg
Content: "STATE OF NEVADA DRIVER LICENSE SMITH JOHN A DOB 01/01/1970"
Correct answer: photo_id

EXAMPLE 4
Filename: upload.pdf
Content: "INVOICE Roofing repair 4,200.00 Paid in full"
Correct answer: other

Now classify the following document.

Filename: {filename}

Content:
{content}

Respond with a JSON object containing exactly two keys:
  "doc_type": one of the allowed types listed above
  "confidence": a number between 0 and 1 indicating how confident you are

Respond with the JSON object and nothing else."""


def build_extraction_prompt(doc_type: str, content: str) -> str:
    """Build the extraction prompt for a document of a known type.

    Which fields get requested depends on the document type. Types that are not
    listed get a generic instruction.
    """
    fields_by_type = {
        "pay_stub": ["employer", "gross_pay", "net_pay", "period_end"],
        "w2": ["employer", "wages", "tax_year"],
        "bank_statement": ["institution", "ending_balance", "account_last4"],
        "photo_id": ["full_name", "date_of_birth", "expires"],
        "homeowners_insurance": ["policy_number", "coverage_amount", "annual_premium"],
        "property_tax_bill": ["parcel", "annual_tax"],
        "counseling_certificate": ["agency", "completed_on"],
    }

    wanted = fields_by_type.get(doc_type, ["summary"])
    field_list = "\n".join(f"  - {f}" for f in wanted)

    return f"""You are extracting structured fields from a mortgage loan document.

The document has already been classified as: {doc_type}

Extract the following fields:
{field_list}

If a field is not present in the document, use null for that field.
Do not guess. Do not infer a value that is not written in the document.

Document content:
{content}

Respond with a JSON object whose keys are exactly the field names listed above.
Respond with the JSON object and nothing else."""
