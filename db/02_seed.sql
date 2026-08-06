-- Synthetic seed. Every name, amount, address and account number below is made
-- up. Nothing here came from a real borrower or a real file.
--
-- NOTE ON status: this column has drifted. The intake form wrote lowercase, an
-- old admin script wrote title case, a bulk import in March wrote uppercase, and
-- files created through the API get NULL. Nobody has picked one.

INSERT INTO checklist_item (product, doc_type, required) VALUES
  ('reverse', 'pay_stub',            false),
  ('reverse', 'bank_statement',      true),
  ('reverse', 'photo_id',            true),
  ('reverse', 'homeowners_insurance',true),
  ('reverse', 'property_tax_bill',   true),
  ('reverse', 'counseling_certificate', true),
  ('forward', 'pay_stub',            true),
  ('forward', 'w2',                  true),
  ('forward', 'bank_statement',      true),
  ('forward', 'photo_id',            true),
  ('forward', 'homeowners_insurance',true);

INSERT INTO loan_file (reference, borrower_name, product, opened_at, status) VALUES
  ('LF-10021', 'Marguerite Halloway',  'reverse', '2026-08-03 09:12-07', 'pending'),
  ('LF-10022', 'Desmond Okonkwo',      'reverse', '2026-08-03 14:40-07', 'Pending'),
  ('LF-10023', 'Priya Raghunathan',    'forward', '2026-08-05 08:05-07', 'PENDING'),
  ('LF-10024', 'Walter Brzezinski',    'reverse', '2026-08-06 11:33-07', 'in_review'),
  ('LF-10025', 'Yolanda Ferreira',     'forward', '2026-08-07 16:20-07', 'In Review'),
  ('LF-10026', 'Chen Wei-Lin',         'reverse', '2026-08-10 07:55-07', NULL),
  ('LF-10027', 'Augustin Delacroix',   NULL,      '2026-08-11 10:02-07', 'pending'),
  ('LF-10028', 'Rosalind Achebe',      'reverse', '2026-08-12 13:47-07', 'complete'),
  ('LF-10029', 'Tomasz Wilczynski',    'forward', '2026-08-14 09:30-07', NULL),
  ('LF-10030', 'Ingrid Sorensen',      'reverse', '2026-08-17 15:11-07', 'Complete'),
  ('LF-10031', 'Bashir Al-Rashid',     'reverse', '2026-08-19 08:44-07', 'pending'),
  ('LF-10032', 'Henrietta Oyelaran',   'forward', '2026-08-21 12:00-07', 'pending');

-- Documents. content is the text a PDF extractor would have produced.
-- confidence is TEXT and the values are inconsistent: some decimals, some
-- percentages, some empty. That is what is actually in the column today.

INSERT INTO document (loan_file_id, filename, content, uploaded_at, doc_type, confidence, classified_at) VALUES
 (1,'scan_0001.pdf', E'ACME PAYROLL SERVICES\nEmployee: M. HALLOWAY\nPay Period: 07/01/2026 - 07/15/2026\nGross Pay: 2,180.00\nNet Pay: 1,702.44\nYTD Gross: 30,520.00', '2026-08-03 09:14-07','pay_stub','0.94','2026-08-03 09:15-07'),
 (1,'scan_0002.pdf', E'FIRST MERIDIAN BANK\nStatement Period: July 2026\nAccount ending 4417\nBeginning Balance: 12,884.10\nEnding Balance: 11,203.77', '2026-08-03 09:14-07','bank_statement','0.97','2026-08-03 09:15-07'),
 (1,'IMG_4482.jpg', E'STATE OF CALIFORNIA\nDRIVER LICENSE\nHALLOWAY, MARGUERITE A\nDOB 03/14/1954\nEXP 03/14/2029', '2026-08-03 09:16-07','photo_id','0.99','2026-08-03 09:17-07'),
 (1,'insurance.pdf', E'HOMEOWNERS POLICY DECLARATION\nPolicy No HO-882145\nDwelling Coverage: 420,000\nAnnual Premium: 1,844.00\nEffective 04/01/2026 to 04/01/2027', '2026-08-04 10:01-07','homeowners_insurance','0.91','2026-08-04 10:02-07'),
 -- resubmission: same statement, different filename, uploaded 6 days later
 (1,'first_meridian_july.pdf', E'FIRST MERIDIAN BANK\nStatement Period: July 2026\nAccount ending 4417\nBeginning Balance: 12,884.10\nEnding Balance: 11,203.77', '2026-08-09 08:20-07','bank_statement','0.96','2026-08-09 08:21-07'),

 (2,'doc1.pdf', E'CERTIFICATE OF COMPLETION\nHECM Counseling\nClient: DESMOND OKONKWO\nAgency: Prairie Housing Alliance\nCompleted: 07/22/2026\nCertificate No 2026-PHA-8813', '2026-08-03 14:42-07','counseling_certificate','0.88','2026-08-03 14:43-07'),
 (2,'doc2.pdf', E'COUNTY OF SAN BERNARDINO\nSECURED PROPERTY TAX BILL\nParcel 0264-331-09\nAssessed Value: 512,300\nAnnual Tax: 6,140.28\nFiscal Year 2026-2027', '2026-08-03 14:42-07','property_tax_bill','88%','2026-08-03 14:43-07'),
 (2,'doc3.pdf', E'Sunrise Federal Credit Union\nMonthly Statement - July 2026\nMember 77120448\nAvailable Balance 46,201.55', '2026-08-03 14:42-07','bank_statement','0.93','2026-08-03 14:43-07'),
 (2,'unknown_scan.pdf', E'[page appears blank]\n[faint handwriting, illegible]', '2026-08-05 09:00-07',NULL,NULL,NULL),

 (3,'paystub_aug.pdf', E'NORTHGATE LOGISTICS INC\nEmployee: RAGHUNATHAN, PRIYA\nPeriod Ending 08/01/2026\nGross 4,615.38\nNet 3,402.11\nYTD 96,923.00', '2026-08-05 08:07-07','pay_stub','0.95','2026-08-05 08:08-07'),
 (3,'w2_2025.pdf', E'Form W-2 Wage and Tax Statement 2025\nEmployee PRIYA RAGHUNATHAN\nWages tips other comp 112,400.00\nFederal income tax withheld 18,984.00\nEmployer NORTHGATE LOGISTICS INC', '2026-08-05 08:07-07','w2','0.98','2026-08-05 08:08-07'),
 (3,'chase_stmt.pdf', E'Statement of Account\nJuly 1 - July 31 2026\nAccount ****2201\nEnding balance 8,455.19', '2026-08-05 08:07-07','bank_statement','0.94','2026-08-05 08:08-07'),
 (3,'license_front.png', E'WASHINGTON DRIVER LICENSE\nRAGHUNATHAN PRIYA\nDOB 11/02/1987\n4d WDL RAGHUP**812K4', '2026-08-05 08:09-07','photo_id','0.97','2026-08-05 08:10-07'),

 (4,'a.pdf', E'MERIDIAN TRUST BANK\nCombined Statement August 2026\nChecking ****9034 balance 3,118.62\nSavings ****9035 balance 88,450.00', '2026-08-06 11:35-07','bank_statement','0.92','2026-08-06 11:36-07'),
 (4,'b.pdf', E'HOMEOWNERS INSURANCE\nPolicy HO-441902 CANCELLED EFFECTIVE 06/30/2026\nReason: non-payment', '2026-08-06 11:35-07','homeowners_insurance','0.79','2026-08-06 11:36-07'),
 (4,'c.pdf', E'To whom it may concern,\n\nI am writing to explain the gap in my employment between\nMarch and June of this year. I was caring for my mother.\n\nSincerely,\nWalter Brzezinski', '2026-08-06 11:35-07','letter_of_explanation','0.71','2026-08-06 11:36-07'),

 (5,'stub1.pdf', E'CASCADE HEALTH SYSTEMS\nY FERREIRA\nPay date 08/07/2026\nGross 3,250.00\nNet 2,441.88', '2026-08-07 16:22-07','pay_stub','0.96','2026-08-07 16:23-07'),
 (5,'stub2.pdf', E'CASCADE HEALTH SYSTEMS\nY FERREIRA\nPay date 07/24/2026\nGross 3,250.00\nNet 2,441.88', '2026-08-07 16:22-07','pay_stub','0.96','2026-08-07 16:23-07'),
 (5,'id.jpg', E'OREGON\nDRIVER LICENSE\nFERREIRA YOLANDA M\nDOB 06/19/1979', '2026-08-07 16:22-07','photo_id','0.98','2026-08-07 16:23-07'),

 (6,'tax.pdf', E'COUNTY OF KING\nPROPERTY TAX STATEMENT 2026\nParcel 882011-4420\nTotal Due 8,912.44', '2026-08-10 07:57-07','property_tax_bill','0.9','2026-08-10 07:58-07'),
 (6,'ins.pdf', E'DWELLING FIRE POLICY\nPolicy DF-77301\nCoverage A 610,000\nPremium 2,290.00', '2026-08-10 07:57-07','homeowners_insurance','0.87','2026-08-10 07:58-07'),
 (6,'counsel.pdf', E'HUD-APPROVED COUNSELING CERTIFICATE\nCHEN WEI-LIN\nCompleted 08/01/2026\nAgency: Puget Sound Housing Council', '2026-08-10 07:57-07','counseling_certificate','0.93','2026-08-10 07:58-07'),

 (7,'file1.pdf', E'GREENLEAF MANUFACTURING\nEarnings Statement\nA DELACROIX\nPeriod 07/26/2026\nGross 5,120.00', '2026-08-11 10:04-07','pay_stub','0.94','2026-08-11 10:05-07'),
 (7,'file2.pdf', E'Dear Applicant,\n\nEnclosed please find the documents you requested regarding\nyour account. Please contact us with any questions.\n\nCustomer Service', '2026-08-11 10:04-07',NULL,NULL,NULL),

 (8,'01.pdf', E'PIONEER SAVINGS\nStatement July 2026\nAccount ****6612\nEnding Balance 152,880.03', '2026-08-12 13:49-07','bank_statement','0.97','2026-08-12 13:50-07'),
 (8,'02.pdf', E'ILLINOIS IDENTIFICATION CARD\nACHEBE ROSALIND N\nDOB 09/30/1951', '2026-08-12 13:49-07','photo_id','0.99','2026-08-12 13:50-07'),
 (8,'03.pdf', E'HOMEOWNERS POLICY\nPolicy HO-220841\nCoverage A 385,000\nEffective 01/15/2026 - 01/15/2027', '2026-08-12 13:49-07','homeowners_insurance','0.95','2026-08-12 13:50-07'),
 (8,'04.pdf', E'COOK COUNTY TREASURER\nSecond Installment 2026\nPIN 14-33-201-018-0000\nAmount 4,203.55', '2026-08-12 13:49-07','property_tax_bill','0.94','2026-08-12 13:50-07'),
 (8,'05.pdf', E'CERTIFICATE OF HECM COUNSELING\nRosalind Achebe\nDate 07/18/2026\nCounselor ID 88-2214', '2026-08-12 13:49-07','counseling_certificate','0.92','2026-08-12 13:50-07'),

 (9,'p1.pdf', E'BLUE RIDGE CONTRACTORS\nT WILCZYNSKI\nPay Period 08/01-08/14/2026\nGross 3,840.00\nNet 2,901.22', '2026-08-14 09:32-07','pay_stub','0.95','2026-08-14 09:33-07'),
 (9,'p2.pdf', E'Form W-2 2025\nTOMASZ WILCZYNSKI\nWages 94,200.00\nBLUE RIDGE CONTRACTORS', '2026-08-14 09:32-07','w2','0.97','2026-08-14 09:33-07'),

 (10,'doc_a.pdf', E'NORDIC CREDIT UNION\nAugust 2026 Statement\nMember 44190228\nBalance 71,440.18', '2026-08-17 15:13-07','bank_statement','95%','2026-08-17 15:14-07'),
 (10,'doc_b.pdf', E'MINNESOTA DRIVER LICENSE\nSORENSEN INGRID K\nDOB 02/08/1948', '2026-08-17 15:13-07','photo_id','0.98','2026-08-17 15:14-07'),
 (10,'doc_c.pdf', E'HOMEOWNERS DECLARATIONS PAGE\nPolicy HO-991204\nDwelling 298,000\nPremium 1,102.00', '2026-08-17 15:13-07','homeowners_insurance','0.93','2026-08-17 15:14-07'),
 (10,'doc_d.pdf', E'RAMSEY COUNTY PROPERTY TAX\n2026 Statement\nParcel 20-29-22-31-0044\nTotal 3,880.12', '2026-08-17 15:13-07','property_tax_bill','0.91','2026-08-17 15:14-07'),
 (10,'doc_e.pdf', E'REVERSE MORTGAGE COUNSELING CERTIFICATE\nIngrid Sorensen\nCompleted 08/02/2026', '2026-08-17 15:13-07','counseling_certificate','0.9','2026-08-17 15:14-07'),

 (11,'upload.pdf', E'COMMERCE BANK OF THE SOUTHWEST\nStatement Period 07/2026\nAccount ****1188\nEnding 22,910.40', '2026-08-19 08:46-07','bank_statement','0.96','2026-08-19 08:47-07'),
 (11,'upload (1).pdf', E'COMMERCE BANK OF THE SOUTHWEST\nStatement Period 07/2026\nAccount ****1188\nEnding 22,910.40', '2026-08-19 08:51-07','bank_statement','0.96','2026-08-19 08:52-07'),
 (11,'upload (2).pdf', E'COMMERCE BANK OF THE SOUTHWEST\nStatement Period 07/2026\nAccount ****1188\nEnding 22,910.40', '2026-08-19 08:53-07','bank_statement','0.96','2026-08-19 08:54-07'),

 (12,'h_oyelaran_stub.pdf', E'ATLAS DISTRIBUTION\nHENRIETTA OYELARAN\nPeriod ending 08/15/2026\nGross 4,100.00\nNet 3,055.90', '2026-08-21 12:02-07','pay_stub','0.95','2026-08-21 12:03-07'),
 (12,'h_oyelaran_w2.pdf', E'W-2 2025\nHENRIETTA OYELARAN\nWages 98,750.00', '2026-08-21 12:02-07','w2','0.96','2026-08-21 12:03-07'),
 (12,'misc.pdf', E'INVOICE\nRoofing repair - 4,200.00\nPaid in full 06/2026', '2026-08-21 12:02-07',NULL,NULL,NULL);

INSERT INTO extraction (document_id, field_name, field_value) VALUES
 (1,'employer','ACME PAYROLL SERVICES'),(1,'gross_pay','2180.00'),(1,'period_end','2026-07-15'),
 (2,'institution','FIRST MERIDIAN BANK'),(2,'ending_balance','11203.77'),(2,'account_last4','4417'),
 (3,'full_name','MARGUERITE A HALLOWAY'),(3,'date_of_birth','1954-03-14'),(3,'expires','2029-03-14'),
 (4,'policy_number','HO-882145'),(4,'coverage_amount','420000'),(4,'annual_premium','1844.00'),
 (6,'agency','Prairie Housing Alliance'),(6,'completed_on','2026-07-22'),
 (7,'parcel','0264-331-09'),(7,'annual_tax','6140.28'),
 (10,'employer','NORTHGATE LOGISTICS INC'),(10,'gross_pay','4615.38'),
 (11,'wages','112400.00'),(11,'tax_year','2025'),
 (15,'policy_number','HO-441902'),(15,'status','CANCELLED');
