import { useEffect, useState } from "react";
import LoanList from "./components/LoanList";
import DocumentList from "./components/DocumentList";
import {
  listLoans,
  getLoan,
  getMissing,
  classifyPending,
  type Loan,
  type Doc,
  type Missing,
} from "./lib/api";

export default function App() {
  const [loans, setLoans] = useState<Loan[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [docs, setDocs] = useState<Doc[]>([]);
  const [missing, setMissing] = useState<Missing | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    listLoans().then(setLoans).catch((e) => setError(String(e)));
  }, []);

  useEffect(() => {
    if (selected === null) return;
    getLoan(selected).then((l) => setDocs(l.documents)).catch(() => setDocs([]));
    getMissing(selected).then(setMissing).catch(() => setMissing(null));
  }, [selected]);

  async function runClassifier() {
    setBusy(true);
    try {
      await classifyPending();
      if (selected !== null) {
        const l = await getLoan(selected);
        setDocs(l.documents);
      }
      setLoans(await listLoans());
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="wrap">
      <h1>Loan Intake Triage</h1>
      <p className="sub">
        Documents arrive against a loan file, get classified, and the file is
        checked against a per-product checklist.
      </p>

      {error && (
        <div className="card" style={{ marginBottom: 18, padding: "12px 14px" }}>
          <code>{error}</code>
        </div>
      )}

      <div style={{ marginBottom: 14 }}>
        <button onClick={runClassifier} disabled={busy}>
          {busy ? "Classifying…" : "Classify unclassified documents"}
        </button>
      </div>

      <div className="grid">
        <LoanList loans={loans} selected={selected} onSelect={setSelected} />
        <DocumentList docs={docs} missing={missing} />
      </div>
    </div>
  );
}
